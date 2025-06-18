from cryptography.fernet import Fernet
from pathlib import Path
import json

# SECURITY_KEY = Path(__file__).parent.parent / "stor" / "security.key"
DATA_FILE = Path(__file__).parent.parent / "stor" / "data.json"

#def load_key():
#    with open(SECURITY_KEY, "rb") as f:
#        return f.read()

def load_data(fernet: Fernet):
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "rb") as f:
        encrypted = f.read()
    decrypted = fernet.decrypt(encrypted)
    data = json.loads(decrypted.decode("utf-8"))
    return data

def save_data(data, fernet: Fernet):
    json_bytes = json.dumps(data).encode("utf-8")
    encrypted = fernet.encrypt(json_bytes)
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted)

def new_file(fernet: Fernet):
    data = load_data(fernet)
    
    f_name = input("Enter File Name: ").strip()
    if not f_name:
        print("File name cannot be empty!")
        return
    
    if f_name in data:
        print(f"File '{f_name}' already exists. Choose another name or open it instead.")
        return
    
    email = input("Enter Email: ").strip()
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    notes = input("Enter Notes (optional): ").strip()
    
    data[f_name] = {
        "email": email,
        "username": username,
        "password": password,
        "notes": notes
    }
    
    save_data(data, fernet)
    print(f"New file '{f_name}' created and saved successfully.")