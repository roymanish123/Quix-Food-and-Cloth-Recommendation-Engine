import os
import hashlib
from config import LOCATIONS

def get_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def remove_duplicates(folder):
    hashes = {}
    removed = 0
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if not os.path.isfile(path):
            continue
        file_hash = get_hash(path)
        if file_hash in hashes:
            os.remove(path)
            removed += 1
            print(f"🗑️ Removed duplicate: {file}")
        else:
            hashes[file_hash] = file
    print(f"✅ Removed {removed} duplicates from {folder}")

if __name__ == "__main__":
    BASE = "dataset/clothes/images"
    for location in LOCATIONS:
        folder = os.path.join(BASE, location)
        if os.path.exists(folder):
            remove_duplicates(folder)