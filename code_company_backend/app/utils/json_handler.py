import json
import os
from config import Config

# 🔹 Read data from memory.json
def read_memory():
    """Reads data from the JSON memory file."""
    try:
        if not os.path.exists(Config.MEMORY_FILE):
            return {}
        with open(Config.MEMORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

# 🔹 Write or update data to memory.json
def write_memory(data):
    """Writes or updates data to the JSON memory file."""
    with open(Config.MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return {"status": "success", "message": "Data written successfully."}

# 🔹 (Optional) For /save and /read routes compatibility
def save_to_json(data):
    """Alias for write_memory, used in routes.py"""
    return write_memory(data)

def read_json():
    """Alias for read_memory, used in routes.py"""
    return read_memory()
