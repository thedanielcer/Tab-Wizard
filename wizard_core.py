import requests
import subprocess
import time
from dotenv import load_dotenv
import os
import pygetwindow as gw
import datetime

def log(message):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {message}")

# === CONFIGURATION ===
load_dotenv()
EDGE_PATH = os.getenv("EDGE_PATH")
USER_DATA_DIR = os.getenv("USER_DATA_DIR")
DEBUG_PORT = int(os.getenv("DEBUG_PORT"))


def launch_edge_on_selected_tab(desired_url):
    subprocess.Popen([
        EDGE_PATH,
        f'--user-data-dir={USER_DATA_DIR}',
        f'--remote-debugging-port={DEBUG_PORT}',
        f'{desired_url}',
    ])
    time.sleep(2)

# === FOCUS EDGE WINDOW ===
def focus_edge_window():
    log("Looking for edge window")
    edge_window = [w for w in gw.getWindowsWithTitle('work debug - microsoft\u200b edge') if w.title.lower() and not w.isMinimized]
    if not edge_window:
        print("No edge window found")
        edge_window = [w for w in gw.getWindowsWithTitle('work debug - microsoft\u200b edge')]
    
    if edge_window:
        edge_window = edge_window[0]
        log(f"Edge window found: {edge_window.title}")
        if edge_window.isMinimized:
            log("Edge was minimized, restoring")
            edge_window.restore()
        log("Activating edge window")
        edge_window.activate()

# === ACTIVATE DESIRED TAB ===
def activate_tab(tab_id):
    log(f"Activating tab {tab_id}")
    requests.get(f"http://127.0.0.1:{DEBUG_PORT}/json/activate/{tab_id}", proxies={"http": None, "https": None})
    log(f"Tab {tab_id} activated")

# === IF DESIRED TAB DOESN'T EXIST, OPEN IT ===
def open_url_on_new_tab(desired_url):
    subprocess.Popen([
        EDGE_PATH,
        f'--user-data-dir={USER_DATA_DIR}',
        f'{desired_url}'
    ])

# === CONNECT TO TABS ===
def get_tabs():
    log("Getting tabs")
    try:
        log("getting response")
        response = requests.get(f"http://127.0.0.1:{DEBUG_PORT}/json", proxies={"http": None, "https": None})
        log("response received")
        all_targets = response.json()
        # Only keep real tabs
        log("Tabs received")
        return [tab for tab in all_targets if tab.get("type") == "page"]
    except requests.exceptions.ConnectionError:
        return None
    
# === NORMALIZE URL ===
def normalize_url(url):
    return url.split("?")[0].rstrip("/").lower()

# === MAIN LOGIC ===
def focus_or_open_tab(desired_url):
    log(f"Focusing or opening tab: {desired_url}")
    tabs = get_tabs()

    if tabs is None:
        print("Edge not running or not in debug mode. Launching...")
        launch_edge_on_selected_tab(desired_url)
        tabs = get_tabs()
    else:
        log("Edge is running, and got tabs")

    if tabs is None:
        print("Still couldn't connect to Edge after launching.")
        return

    for tab in tabs:
        log(f"Comparing: {desired_url} vs {tab.get('url')}")
        if normalize_url(desired_url) in normalize_url(tab.get("url", "")):
            focus_edge_window()
            activate_tab(tab.get("id"))
            log(f"Focused Tab: {desired_url}")
            return
    
    open_url_on_new_tab(desired_url)