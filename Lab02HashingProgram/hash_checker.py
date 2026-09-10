import os
import json
import hashlib


def hash_file(filepath): # Creates a SHA-256 hash for one file
    sha256 = hashlib.sha256()

# Read the file in small pieces
    with open(filepath, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()

# Goes through all files in the folder
def traverse_directory(directory):
    hashes = {}

    for root, folders, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Skip the hash table itself
            if filename == "hash_table.json":
                continue

            hashes[filepath] = hash_file(filepath)

    return hashes

# Creates and saves the hash table
def generate_table():
    directory = input("Enter directory path: ")

# Make sure the folder exists
    if not os.path.isdir(directory):
        print("Directory does not exist.")
        return

    hashes = traverse_directory(directory)

    table = {
        "directory": directory,
        "files": []
    }

 # Add each file and hash to the table
    for filepath, hash_value in hashes.items():
        table["files"].append({
            "filepath": filepath,
            "hash": hash_value
        })

    # Save the results to a JSON file
    with open("hash_table.json", "w") as file:
        json.dump(table, file, indent=4)

    print("Hash table generated")

# Checks if the files have changed
def validate_hash():
    if not os.path.exists("hash_table.json"):
        print("Hash table does not exist.")
        return

    # Read the saved hash table
    with open("hash_table.json", "r") as file:
        table = json.load(file)

    directory = table["directory"]

    stored_hashes = {}

    # Store old file paths and hashes
    for item in table["files"]:
        stored_hashes[item["filepath"]] = item["hash"]

    # Hash the files again
    current_hashes = traverse_directory(directory)

    updated = False

    # Check each old file
    for old_path, old_hash in list(stored_hashes.items()):

        # File is still in the same place
        if old_path in current_hashes:

            if current_hashes[old_path] == old_hash:
                print(old_path, "hash is valid")

            else:
                print(old_path, "hash is invalid")

        else:
            # Check if the file was renamed
            renamed_file = None

            for new_path, new_hash in current_hashes.items():
                if new_hash == old_hash and new_path not in stored_hashes:
                    renamed_file = new_path
                    break

            if renamed_file:
                print(old_path, "was renamed to", renamed_file)

                # Update the filepath in the table
                for item in table["files"]:
                    if item["filepath"] == old_path:
                        item["filepath"] = renamed_file

                updated = True

            else:
                print(old_path, "has been deleted")

    # Check for completely new files
    for filepath in current_hashes:
        if filepath not in stored_hashes:

            already_added = False

            # Make sure it was not just renamed
            for item in table["files"]:
                if item["filepath"] == filepath:
                    already_added = True

            if not already_added:
                print(filepath, "is a new file")

    # Save the updated table if a file was renamed
    if updated:
        with open("hash_table.json", "w") as file:
            json.dump(table, file, indent=4)

        print("Hash table updated")

# Handles the menu options
def main():
    print("1. Generate new hash table")
    print("2. Verify hashes")

    choice = input("Enter your choice: ")

    if choice == "1":
        generate_table()

    elif choice == "2":
        validate_hash()

    else:
        print("Invalid choice")


main()