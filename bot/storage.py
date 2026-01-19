import os
import json

def ensure_dir(path):
    d = os.path.dirname(path)

    if d:
        os.makedirs(d, exist_ok=True)

def load_json(path, default):
    ensure_dir(path)

    if not os.path.exists(path):
        return default
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default

def save_json(path, data):
    ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    