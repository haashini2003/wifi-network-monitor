# Wi-Fi Network Monitor

A Python-based desktop application that scans and monitors nearby Wi-Fi networks using Windows wireless network information.

## Features

- Scan nearby Wi-Fi networks
- Display SSID names
- Show signal strength percentage
- Display visual signal strength bars
- Classify signal quality as Excellent, Good, Fair, or Weak
- Display Wi-Fi channel and band
- Detect Wi-Fi security type
- Classify security as Strong, Secure, Moderate, Weak, or Unsecured
- Search and filter networks by SSID
- Sort networks by signal strength
- Sort networks by SSID
- Sort networks by channel
- Automatically refresh network information every 10 seconds
- Display total number of detected networks
- Display last scan time

## Technologies Used

- Python
- Tkinter
- Windows Netsh WLAN
- Subprocess
- ttk Treeview

## Requirements

- Windows operating system
- Python 3.x
- Wi-Fi adapter
- Tkinter

## How to Run

1. Download or clone this repository.
2. Open the project folder in Visual Studio Code.
3. Open the terminal.
4. Run the following command:

```bash
python wifi_monitor.py