import os
import json
from datetime import datetime

BLACKLIST_FILE = "data/blacklist.txt"
BLACKLIST_JSON = "data/blacklist_log.json"

def _normalize(text: str) -> str:
    return text.lower().strip()

def add_to_blacklist(name: str, age: int, background: str, reason: str) -> None:
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    txt_entry = f"[{timestamp}] Name: {name} | Age: {age} | Reason: {reason} | Background: {background[:120]}\n"
    with open(BLACKLIST_FILE, "a", encoding="utf-8") as f:
        f.write(txt_entry)

    log_entry = {
        "timestamp": timestamp,
        "name": name,
        "age": age,
        "reason": reason,
        "background_excerpt": background[:200]
    }
    existing = []
    if os.path.exists(BLACKLIST_JSON):
        try:
            with open(BLACKLIST_JSON, "r", encoding="utf-8") as jf:
                existing = json.load(jf)
        except Exception:
            existing = []
    existing.append(log_entry)
    with open(BLACKLIST_JSON, "w", encoding="utf-8") as jf:
        json.dump(existing, jf, ensure_ascii=False, indent=2)

def is_blacklisted(name: str) -> bool:
    if not name:
        return False
    normalized_name = _normalize(name)
    
    if os.path.exists(BLACKLIST_JSON):
        try:
            with open(BLACKLIST_JSON, "r", encoding="utf-8") as jf:
                entries = json.load(jf)
                for entry in entries:
                    if _normalize(entry.get("name", "")) == normalized_name:
                        return True
        except Exception:
            pass
    
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split("|")
                for part in parts:
                    if "Name:" in part:
                        stored_name = _normalize(part.replace("Name:", "").strip())
                        if stored_name == normalized_name:
                            return True
    return False
