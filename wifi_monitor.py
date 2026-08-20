import subprocess
import tkinter as tk
from tkinter import ttk
from datetime import datetime


# Store all scanned networks
all_networks = []


# ---------------- SIGNAL STATUS ----------------

def get_signal_status(signal):
    try:
        value = int(signal.replace("%", ""))

        if value >= 80:
            return "Excellent"
        elif value >= 60:
            return "Good"
        elif value >= 40:
            return "Fair"
        else:
            return "Weak"

    except ValueError:
        return "Unknown"


# ---------------- SECURITY STATUS ----------------

def get_security_status(security):
    security = security.lower()

    if "wpa3" in security:
        return "Strong"
    elif "wpa2" in security:
        return "Secure"
    elif "wpa" in security:
        return "Moderate"
    elif "wep" in security:
        return "Weak"
    elif "open" in security:
        return "Unsecured"
    else:
        return "Unknown"


# ---------------- WIFI SCANNER ----------------

def scan_wifi():

    result = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    output = result.stdout

    networks = []
    current = {}

    for line in output.splitlines():

        line = line.strip()

        if line.startswith("SSID ") and ":" in line:

            if current.get("SSID"):
                networks.append(current)

            current = {
                "SSID": line.split(":", 1)[1].strip()
            }

        elif line.startswith("Authentication") and ":" in line:

            current["Security"] = line.split(":", 1)[1].strip()

        elif line.startswith("Signal") and ":" in line:

            current["Signal"] = line.split(":", 1)[1].strip()

        elif line.startswith("Channel") and ":" in line:

            current["Channel"] = line.split(":", 1)[1].strip()

        elif line.startswith("Band") and ":" in line:

            current["Band"] = line.split(":", 1)[1].strip()

    if current.get("SSID"):
        networks.append(current)

    return networks


# ---------------- DISPLAY NETWORKS ----------------

def display_networks(networks):

    # Clear table
    for item in table.get_children():
        table.delete(item)

    # Display each network
    for network in networks:

        signal = network.get("Signal", "Unknown")
        security = network.get("Security", "Unknown")

        signal_status = get_signal_status(signal)
        security_status = get_security_status(security)

        # Signal bar
        try:

            signal_value = int(signal.replace("%", ""))

            bars = "█" * (signal_value // 10)

            signal_bar = bars + "░" * (10 - len(bars))

        except ValueError:

            signal_bar = "Unknown"

        # Security color tag
        if security_status == "Strong":
            tag = "strong"

        elif security_status == "Secure":
            tag = "secure"

        elif security_status == "Moderate":
            tag = "moderate"

        elif security_status == "Weak":
            tag = "weak"

        elif security_status == "Unsecured":
            tag = "unsecured"

        else:
            tag = "unknown"

        # Insert into table
        table.insert(
            "",
            "end",
            values=(
                network.get("SSID", "Unknown"),
                signal,
                signal_bar,
                signal_status,
                network.get("Channel", "Unknown"),
                network.get("Band", "Unknown"),
                security,
                security_status
            ),
            tags=(tag,)
        )

    # Update network count
    count_label.config(
        text=f"Networks Found: {len(networks)}"
    )


# ---------------- UPDATE NETWORKS ----------------

def update_networks():

    global all_networks

    # Scan networks
    all_networks = scan_wifi()

    # Check search box
    search_text = search_entry.get().lower().strip()

    if search_text == "":

        display_networks(all_networks)

    else:

        filter_networks()

    # Update last scan time
    time_label.config(
        text=f"Last Scan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Automatic refresh every 10 seconds
    root.after(10000, update_networks)


# ---------------- SEARCH / FILTER ----------------

def filter_networks():

    search_text = search_entry.get().lower().strip()

    if search_text == "":

        display_networks(all_networks)

        return

    filtered_networks = []

    for network in all_networks:

        ssid = network.get("SSID", "Unknown")

        if search_text in ssid.lower():

            filtered_networks.append(network)

    display_networks(filtered_networks)


# ---------------- CLEAR SEARCH ----------------

def clear_search():

    search_entry.delete(0, tk.END)

    display_networks(all_networks)


# ---------------- SORT BY SIGNAL ----------------

def sort_by_signal():

    sorted_networks = sorted(
        all_networks,
        key=lambda network: int(
            network.get("Signal", "0").replace("%", "")
        )
        if network.get("Signal", "0").replace("%", "").isdigit()
        else 0,
        reverse=True
    )

    display_networks(sorted_networks)


# ---------------- SORT BY SSID ----------------

def sort_by_ssid():

    sorted_networks = sorted(
        all_networks,
        key=lambda network:
        network.get("SSID", "").lower()
    )

    display_networks(sorted_networks)


# ---------------- SORT BY CHANNEL ----------------

def sort_by_channel():

    sorted_networks = sorted(
        all_networks,
        key=lambda network: int(
            network.get("Channel", "0")
        )
        if network.get("Channel", "0").isdigit()
        else 0
    )

    display_networks(sorted_networks)


# ---------------- GUI ----------------

root = tk.Tk()

root.title("Wi-Fi Network Monitor")

root.geometry("1150x650")


# ---------------- TITLE ----------------

title = tk.Label(
    root,
    text="Wi-Fi Network Monitor",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)


# ---------------- DESCRIPTION ----------------

description = tk.Label(
    root,
    text="Scan and monitor nearby wireless networks",
    font=("Arial", 11)
)

description.pack()


# ---------------- SCAN BUTTON ----------------

scan_button = tk.Button(
    root,
    text="🔄 Scan Networks",
    command=update_networks,
    font=("Arial", 12, "bold"),
    padx=15,
    pady=8
)

scan_button.pack(pady=15)


# ---------------- SEARCH ----------------

search_frame = tk.Frame(root)

search_frame.pack(pady=5)


search_label = tk.Label(
    search_frame,
    text="Search Network:",
    font=("Arial", 10, "bold")
)

search_label.pack(
    side="left",
    padx=5
)


search_entry = tk.Entry(
    search_frame,
    width=30,
    font=("Arial", 11)
)

search_entry.pack(
    side="left",
    padx=5
)


search_button = tk.Button(
    search_frame,
    text="🔎 Search",
    command=filter_networks
)

search_button.pack(
    side="left",
    padx=5
)


clear_button = tk.Button(
    search_frame,
    text="Clear",
    command=clear_search
)

clear_button.pack(
    side="left",
    padx=5
)


# ---------------- SORTING ----------------

sort_frame = tk.Frame(root)

sort_frame.pack(pady=8)


sort_signal_button = tk.Button(
    sort_frame,
    text="Sort by Signal ↓",
    command=sort_by_signal
)

sort_signal_button.pack(
    side="left",
    padx=5
)


sort_ssid_button = tk.Button(
    sort_frame,
    text="Sort by SSID",
    command=sort_by_ssid
)

sort_ssid_button.pack(
    side="left",
    padx=5
)


sort_channel_button = tk.Button(
    sort_frame,
    text="Sort by Channel",
    command=sort_by_channel
)

sort_channel_button.pack(
    side="left",
    padx=5
)


# ---------------- TABLE ----------------

columns = (
    "SSID",
    "Signal",
    "Signal Bar",
    "Signal Status",
    "Channel",
    "Band",
    "Security",
    "Security Status"
)


table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=12
)


# ---------------- TABLE COLORS ----------------

table.tag_configure(
    "strong",
    foreground="green"
)

table.tag_configure(
    "secure",
    foreground="green"
)

table.tag_configure(
    "moderate",
    foreground="orange"
)

table.tag_configure(
    "weak",
    foreground="red"
)

table.tag_configure(
    "unsecured",
    foreground="red"
)

table.tag_configure(
    "unknown",
    foreground="gray"
)


# ---------------- TABLE HEADINGS ----------------

for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=135
    )


table.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)


# ---------------- NETWORK COUNT ----------------

count_label = tk.Label(
    root,
    text="Networks Found: 0",
    font=("Arial", 11, "bold")
)

count_label.pack(pady=5)


# ---------------- LAST SCAN ----------------

time_label = tk.Label(
    root,
    text="Last Scan: -",
    font=("Arial", 10)
)

time_label.pack(pady=5)


# ---------------- START APPLICATION ----------------

root.mainloop()