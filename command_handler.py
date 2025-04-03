from wizard_core import focus_or_open_tab
import json
import os

# Command -> URL mapping
# === Load command mappings from JSON file ===
def load_commands():
    try:
        path = "commands.local.json" if os.path.exists("commands.local.json") else "commands.json"
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load command mapping: {e}")
        return {}


COMMANDS = load_commands()

def handle_command(command: str):
    target = command.strip().lower()

    if target in COMMANDS:
        url = COMMANDS[target]
        focus_or_open_tab(url)
    else:
        print(f"Unknown command: {command}")
        
