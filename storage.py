# ==========================================================
# storage.py
# Saves and loads the accounts and borrowing records using a
# JSON file (borrowise_data.json) next to the program files.
# No UI code lives here.
# ==========================================================

import json
import os
import tempfile

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "borrowise_data.json"
)


def load_data(default_accounts):
    # MAIN COMMENT: it Reads accounts and records from the JSON file.
    # Returns (accounts, records). 
    # If the file is missing, empty or
    # damaged, the default accounts and an empty record list are used.
    accounts = None
    records = []

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            accounts = data.get("accounts")
            records = data.get("records", [])

            if not isinstance(accounts, dict) or not isinstance(records, list):
                raise ValueError("Unexpected data format")
        except (OSError, ValueError, AttributeError):
            # Keep the bad file as a backup and start fresh
            try:
                os.replace(DATA_FILE, DATA_FILE + ".bak")
            except OSError:
                pass
            accounts = None
            records = []

    # For the first run we can use the built-in admin account.
    if not accounts:
        accounts = default_accounts

    return accounts, records


def write_data(accounts, records):
    # MAIN COMMENT: Saves accounts and records to the JSON file. Writes to
    # a temporary file first, then replaces the real file, so a crash in
    # the middle of saving cannot corrupt your data. Raises OSError on failure.
    data = {"accounts": accounts, "records": records}
    folder = os.path.dirname(DATA_FILE)

    fd, temp_path = tempfile.mkstemp(dir=folder, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        os.replace(temp_path, DATA_FILE)
    except OSError:
        try:
            os.remove(temp_path)
        except OSError:
            pass
        raise
