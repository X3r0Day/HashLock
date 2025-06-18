import json
from pathlib import Path
from cryptography.fernet import Fernet
import os

from colorama import (
    Style,
    Fore
)



DATA_FILE = Path(__file__).parent.parent / "stor" / "data.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    return


def load_encrypted_data(fernet: Fernet):
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, 'rb') as f:
        encrypted = f.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except Exception as e:
        print(f"[!] Failed to decrypt data: {e}")
        return {}

def save_encrypted_data(data: dict, fernet: Fernet):
    encrypted = fernet.encrypt(json.dumps(data, indent=4).encode())
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted)

def file_list(fernet: Fernet):
    data = load_encrypted_data(fernet)
    return list(data.keys())

def load_data(fernet: Fernet):
    print(f"\n{Style.BRIGHT}{Fore.CYAN}====== Available Files ======{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{file_list(fernet)}{Style.RESET_ALL}")
    f_name = input(f"\n{Style.BRIGHT}{Fore.MAGENTA}>> Enter filename you want to open: {Fore.YELLOW}")
    print(Style.RESET_ALL, end="")

    data = load_encrypted_data(fernet)
    if f_name in data:
        entry = data[f_name]
        data_prt = f'''
\n{Style.BRIGHT}{Fore.GREEN}{f_name} {Style.RESET_ALL}{Fore.CYAN}Details:
{Style.BRIGHT}{Fore.BLUE}Email: {Fore.YELLOW}{entry['email']}
{Style.BRIGHT}{Fore.BLUE}Username: {Fore.YELLOW}{entry['username']}
{Style.BRIGHT}{Fore.BLUE}Password: {Fore.YELLOW}{entry['password']}
{Style.BRIGHT}{Fore.BLUE}Notes: {Fore.YELLOW}{entry['notes']}    

'''

        print(data_prt)
        while True:
            opt = input(f"{Fore.LIGHTGREEN_EX}Press {Fore.RED}ENTER{Fore.LIGHTGREEN_EX} to continue{Style.RESET_ALL}")
            clear_screen()
            break
            
        #print(f"\n{f_name} Details:")
        #print(f"Email: {entry['email']}")
        #print(f"Username: {entry['username']}")
        #print(f"Password: {entry['password']}")
        #print(f"Notes: {entry['notes']}")
    else:
        print("File not found!")

def edit_data(fernet: Fernet):
    data = load_encrypted_data(fernet)
    filenames = list(data.keys())
    if not filenames:
        print("No files to edit.")
        return

    print("\nAvailable Files:")
    for i, name in enumerate(filenames):
        print(f"{i + 1}. {name}")

    choice = input("Select file number to edit: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(filenames):
        print("Invalid selection.")
        return

    f_name = filenames[int(choice) - 1]
    entry = data[f_name]

    print(f"\nEditing: {f_name}")
    print("Leave blank to keep current value.\n")

    for field in ["email", "username", "password", "notes"]:
        current = entry.get(field, "")
        new_val = input(f"{field.capitalize()} [{current}]: ")
        if new_val.strip():
            entry[field] = new_val.strip()

    data[f_name] = entry
    save_encrypted_data(data, fernet)
    print(f"{f_name} updated successfully.")