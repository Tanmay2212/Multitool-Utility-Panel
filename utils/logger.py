import json
from datetime import datetime
import os

LOG_FILE = "activity_log.json"

def log_event(tool, description):
    entry = {
        "tool": tool,
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    logs.insert(0, entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs[:50], f, indent=2)


def get_recent_logs(limit=10):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    return [(log["timestamp"], f"{log['tool']}: {log['description']}") for log in logs[:limit]]

