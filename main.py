import os
import json
import bcrypt
import tkinter as tk
from PIL import Image, ImageTk

from tkinter import (
    messagebox,
    ttk
)

from colorama import Style, Fore
from pathlib import Path
import sv_ttk


from actions import (
    lf,
    nf,
    dl,
    randpass,
    save
)


import key_mngr



def load_icon(filename, size=(20, 20)):
    img = Image.open(Path(__file__).parent / "icon" / filename)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)


CONFIG_FILE = save.user_data_path("config.json")
STOR_CONFIG_FILE = save.user_data_path("stor/config.json")
DATA_FILE = save.user_data_path("stor/data.json")


class PasswordManagerGUI:
    def __init__(self, root, frame):
        self.root = root
        self.root.title("HashLock Password Manager")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.password = None
        self.frame = frame
        self.frame.pack(expand=True)

        self.icons = {
            "add": load_icon("add.png"),
            "folder": load_icon("folder.png"),
            "key": load_icon("key.png"),
            "lock": load_icon("lock.png"),
            "pencil": load_icon("pencil.png"),
            "view": load_icon("view.png"),
            "bin": load_icon("bin.png"),
        }

        sv_ttk.use_dark_theme()
        
        if not CONFIG_FILE.exists():
            self.setup_ui()
        else:
            self.login_ui()

    def clear_window(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    
    def show_password_generator(self):
        popup = tk.Toplevel(self.root)
        popup.title("Generate Random Password")
        popup.geometry("300x150")
        popup.transient(self.root)
        popup.grab_set()

        ttk.Label(popup, text="Enter the length:").pack(pady=10)
        length_entry = ttk.Entry(popup)
        length_entry.pack(pady=5)

        def generate_and_fill():
            try:
                length = int(length_entry.get())
                if length <= 0:
                    raise ValueError
                from actions import randpass
                password = randpass.genRanPass(length)

                self.setup_pwd_entry.delete(0, tk.END)
                self.setup_pwd_entry.insert(0, password)
                self.setup_pwd_confirm.delete(0, tk.END)
                self.setup_pwd_confirm.insert(0, password)

                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")

        ttk.Button(popup, text="Generate", command=generate_and_fill).pack(pady=10)

    
    def toggle_password_visibility(self):
        show = "" if self.show_pwd_var.get() else "*"
        self.setup_pwd_entry.config(show=show)
        self.setup_pwd_confirm.config(show=show)



    def setup_ui(self):
        self.clear_window()

        ttk.Label(self.frame, text="First Time Setup", font=("Segoe UI", 16)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        ttk.Label(self.frame, text="Enter Master Password:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.setup_pwd_entry = ttk.Entry(self.frame, show="*")
        self.setup_pwd_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Confirm Password:").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.setup_pwd_confirm = ttk.Entry(self.frame, show="*")
        self.setup_pwd_confirm.grid(row=2, column=1, padx=10, pady=10)

        self.show_pwd_var = tk.BooleanVar()
        show_checkbox = ttk.Checkbutton(
            self.frame, text="Show Password",
            variable=self.show_pwd_var,
            command=self.toggle_password_visibility
        )
        show_checkbox.grid(row=3, column=1, sticky="w", padx=10)

        ttk.Button(self.frame, text="Generate Random Password", command=self.show_password_generator).grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(self.frame, text="Set Password", command=self.save_master_password).grid(row=5, column=0, columnspan=2, pady=20)



    def save_master_password(self):
        pwd = self.setup_pwd_entry.get()
        pwdConf = self.setup_pwd_confirm.get()

        if pwd != pwdConf:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        
        pwd_bytes = pwd.encode('utf-8')
        # print(type(pwd_bytes)) # DEBUG

        hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode('utf-8')
        with open(CONFIG_FILE, "w") as f:
            json.dump({"master_password": hashed}, f, indent=4)

        messagebox.showinfo("Success", "Password set successfully.")
        self.login_ui()

    def toggle_login_password_visibility(self):
        show = "" if self.show_login_pwd_var.get() else "*"
        self.login_pwd_entry.config(show=show)


    def login_ui(self):
        self.clear_window()

        ttk.Label(self.frame, text="Login", font=("Segoe UI", 16)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        ttk.Label(self.frame, text="Enter Master Password:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        
        self.login_pwd_entry = ttk.Entry(self.frame, show="*")
        self.login_pwd_entry.grid(row=1, column=1, padx=10, pady=10)

        self.show_login_pwd_var = tk.BooleanVar()
        login_show_checkbox = ttk.Checkbutton(
            self.frame, text="Show Password",
            variable=self.show_login_pwd_var,
            command=self.toggle_login_password_visibility
        )
        login_show_checkbox.grid(row=2, column=1, sticky="w", padx=10)

        ttk.Button(self.frame, text="Login", command=self.verify_password).grid(row=3, column=0, columnspan=2, padx=10, pady=10)


    def verify_password(self):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        stored_hash = config["master_password"]

        entered_pwd = self.login_pwd_entry.get()
        if bcrypt.checkpw(entered_pwd.encode(), stored_hash.encode()):
            self.password = entered_pwd
            self.fernet = key_mngr.get_fernet(self.password)
            self.menu_ui()
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def menu_ui(self):
        self.clear_window()

        ttk.Label(self.frame, text="HashLock Password", font=("Segoe UI", 16)).grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        ttk.Button(self.frame, image=self.icons["add"], text="New File", command=self.create_file, compound="left", width=10).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.frame, image=self.icons["bin"], text="Delete File", command=self.delete_file, compound="left", width=10).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self.frame, image=self.icons["pencil"], text=" Edit File", command=self.edit_file, compound="left", width=10).grid(row=4, column=0, padx=10, pady=10)
        ttk.Button(self.frame, image=self.icons["lock"], text="   Exit", command=self.root.quit, compound="left", width=10).grid(row=5, column=0, padx=10, pady=10)

    def create_file(self):
        self.clear_window()
        nf.new_file(self.fernet)
        messagebox.showinfo("Success", "New file created.")
        self.menu_ui()

    def open_file(self):
        self.clear_window()
        lf.OpenEditFileUI(self.frame, self.fernet, self.menu_ui)

    def delete_file(self):
        self.clear_window()
        dl.DeleteFileUI(self.frame, self.fernet, self.menu_ui)

    def edit_file(self):
        self.clear_window()
        lf.OpenEditFileUI(self.frame, self.fernet, self.menu_ui)


def main():
    root = tk.Tk()
    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True)
    app = PasswordManagerGUI(root, frame)
    root.mainloop()

if __name__ == "__main__":
    main()