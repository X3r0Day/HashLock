from pathlib import Path
import json
from cryptography.fernet import Fernet
import sys


from colorama import (
    Style,
    Fore
)


# sys.path.append(str(Path(__file__).parent.parent)) # To import key_mngr from root directory (Not needed anymore)

DATA_FILE = Path(__file__).parent.parent / "stor" / "data.json"

def load_data(fernet: Fernet):
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, 'rb') as f:
        encrypted = f.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except Exception as e:
        print(f"{Style.BRIGHT}{Fore.RED}[x]{Style.RESET_ALL} reading encrypted data:", e)
        return {}

def save_data(data: dict, fernet: Fernet):
    serialized = json.dumps(data, indent=4).encode()
    encrypted = fernet.encrypt(serialized)
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted)

def delete_entry(fernet: Fernet):
    data = load_data(fernet)
    filenames = list(data.keys())
    
    if not filenames:
        print("No entries to delete.")
        return

    print("\nAvailable Files:")
    for i, name in enumerate(filenames):
        print(f"{i + 1}. {name}")
    
    choice = input("Select file number to delete: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(filenames):
        print("Invalid selection.")
        return

    f_name = filenames[int(choice) - 1]

    confirm = input(f"Are you sure you want to delete '{f_name}'? (y/N): ").lower()
    if confirm == 'y':
        del data[f_name]
        save_data(data, fernet)
        print(f"'{f_name}' has been deleted.")
    else:
        print("Deletion cancelled.")