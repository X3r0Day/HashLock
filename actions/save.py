from pathlib import Path
import platform
import os

def get_user_data_base_dir(appname="HashLock"):
    system = platform.system()

    if system == "Windows": # obv
        return Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming")) / appname
    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / appname
    else:  # Linux or wtv
        return Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / appname

def user_data_path(relative_path):
    base_dir = get_user_data_base_dir()
    full_path = base_dir / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path

