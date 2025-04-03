# WorkTabWizard

A silent, fast tab manager for Microsoft Edge — built with Python, and sockets.

## Requirements

- Python installed
- A separate user directory to launch Microsoft Edge

## Features

- Focus or open URLs in Edge instantly
- Works silently in the background
- Stream Deck & AHK compatible
- Uses Edge’s remote debugging protocol

## Setup

1. Clone the repo
2. Create a `.env` file (see `.env.example`)
3. Set up a Python virtual environment
    `python -m venv venv`

4. Install dependencies:
    `pip install -r requirements.txt`

5. Rename `commands.json` to `commands.local.json`

The way i use it is have an AHK script in my startup folder that runs `"e:/Path/to/the/script/rootdir/venv/Scripts/python.exe" "e:/Path/to/script/rootdir/wizard_server.py", , Hide`. This is to start the virtual environment and server on startup.

## AHK Use
Have a hotkey run `Run, "e:/Path/to/the/script/rootdir/venv/Scripts/pythonw.exe" "e:/Path/to/the/script/rootdir/socket_client.py" -command-, , Hide`

## Stream Deck Use
I like to use BarRaider's Advanced Launcher, and it works pretty much the same as with AHK; the program to run is `e:/Path/to/the/script/rootdir/venv/Scripts/pythonw.exe`, and the arguments are `"e:/Path/to/the/script/rootdir/socket_client.py" -command-`
