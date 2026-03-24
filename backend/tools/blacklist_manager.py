import os

BLACKLIST_FILE = "data/blacklist.txt"

def add_to_blacklist(name: str, age: int, background: str, reason: str) -> None:
    os.makedirs(os.path.dirname(BLACKLIST_FILE), exist_ok=True)
    entry = f"Name: {name} | Age: {age} | Background: {background} | Reason: {reason}\n"
    with open(BLACKLIST_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def is_blacklisted(name: str) -> bool:
    if not os.path.exists(BLACKLIST_FILE):
        return False
    with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if f"Name: {name} " in line or f"Name: {name} |" in line:
                return True
    return False
