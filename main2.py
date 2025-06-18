# CLI - Old Version


import os
import json
import getpass
import bcrypt

from actions import (
    lf,
    nf,
    dl
)


from colorama import (
    Style,
    Fore
)

import key_mngr

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    return

CONFIG_FILE = "config.json"


intro = f'''

    {Style.BRIGHT}{Fore.CYAN}X3R0DAY PASSWORD MANAGER
        {Fore.YELLOW}V 0.01

    {Fore.BLUE}By: {Fore.RED}X3r0Day
'''


def setup_pw_manager():
    print("First time setup: Enter your password (Please use SECURE password): ")
    while True:
        password = getpass.getpass("> ")
        confirm = getpass.getpass("Confirm your password\n> ")
        if confirm == password:
            break
        print("Passwords do not match! Please enter again.")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    hashed_str = hashed.decode()

    config = {
        "master_password": hashed_str
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print("Master password set and config saved.")

    main()

def check_if_first_time():
    return not os.path.exists(CONFIG_FILE)

def pwd_verify():
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    stored_hash = config["master_password"]

    for attempt in range(3):
        password = getpass.getpass("Enter Master Password: ")
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            clear_screen()
            print(f"{Style.BRIGHT}{Fore.GREEN}Access granted.{Style.RESET_ALL}")
            return password
        else:
            print("Incorrect Password!")
    print("Too many failed attempts. Exiting")
    exit()

def menu(fernet):
    while True:
        print(intro)
        print(f"{Style.RESET_ALL}{Fore.BLUE}1. New File")
        print("2. Open Existing File")
        print("3. Delete File")
        print("4. Edit File")
        print(f"99. Exit{Style.BRIGHT}{Fore.YELLOW}")

        sel_menu = input(f"> {Style.RESET_ALL}")
        if sel_menu == "1":
            print(f"{Style.RESET_ALL}Creating New File")
            clear_screen()
            nf.new_file(fernet)

        elif sel_menu == "2":
            print("Opening Existing File")
            clear_screen()
            lf.load_data(fernet)

        elif sel_menu == "3":
            clear_screen()
            dl.delete_entry(fernet)
        
        elif sel_menu == "4":
            clear_screen()
            lf.edit_data(fernet)

        elif sel_menu == "99":
            print("Exiting...")
            exit()

def main():
    if check_if_first_time():
        setup_pw_manager()
    else:
        verified_password = pwd_verify()
        fernet = key_mngr.get_fernet(verified_password)
        menu(fernet)

#if __name__ == "__main__":
#    main()
