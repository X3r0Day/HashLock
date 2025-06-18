import os
import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
import file_perm

CONFIG_PATH = Path(__file__).parent / "stor" / "config.json"
SALT_SIZE = 16  # 128-bit salt

def load_or_create_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        salt = base64.b64decode(config["salt"])
        #file_perm.root_only_permission(CONFIG_PATH)
    else:
        salt = os.urandom(SALT_SIZE)
        config = {
            "salt": base64.b64encode(salt).decode("utf-8")
        }
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
        #file_perm.root_only_permission(CONFIG_PATH)
    return salt

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def get_fernet(password: str):
    salt = load_or_create_config()
    key = derive_key(password, salt)
    return Fernet(key)
