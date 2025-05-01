import os
import hashlib
import json

HASH_FILE = "file_hashes.json"

def calculate_hash(file_path, algo='sha256'):
    hasher = hashlib.new(algo)
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def scan_directory(directory):
    hash_dict = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = calculate_hash(filepath)
            if file_hash:
                hash_dict[filepath] = file_hash
    return hash_dict

def save_hashes(hashes, filename=HASH_FILE):
    with open(filename, 'w') as f:
        json.dump(hashes, f, indent=4)

def load_hashes(filename=HASH_FILE):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def check_integrity(old_hashes, new_hashes):
    changed = []
    deleted = []
    added = []

    for filepath, old_hash in old_hashes.items():
        if filepath not in new_hashes:
            deleted.append(filepath)
        elif old_hash != new_hashes[filepath]:
            changed.append(filepath)

    for filepath in new_hashes:
        if filepath not in old_hashes:
            added.append(filepath)

    return changed, deleted, added

def main():
    print("=== File Integrity Checker ===")
    directory = input("Enter the directory to scan: ")

    print("[1] Initialize (store hashes)")
    print("[2] Verify (check changes)")
    choice = input("Enter your choice: ")

    if choice == '1':
        hashes = scan_directory(directory)
        save_hashes(hashes)
        print(f"Hashes saved to {HASH_FILE}")
    elif choice == '2':
        old_hashes = load_hashes()
        new_hashes = scan_directory(directory)
        changed, deleted, added = check_integrity(old_hashes, new_hashes)

        print("\n--- Integrity Report ---")
        print("Changed Files:", changed)
        print("Deleted Files:", deleted)
        print("Added Files:", added)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
