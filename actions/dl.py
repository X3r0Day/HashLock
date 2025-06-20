from pathlib import Path
import json
from cryptography.fernet import Fernet
import sys
from .save import user_data_path

from tkinter import (
    ttk,
    messagebox
)

import tkinter as tk


import sv_ttk

from colorama import (
    Style,
    Fore
)


# sys.path.append(str(Path(__file__).parent.parent)) # To import key_mngr from root directory (Not needed anymore)

DATA_FILE = user_data_path("stor/data.json")

class DeleteFileUI:
    def __init__(self, root, fernet: Fernet, callback):
        self.root = root
        self.fernet = fernet
        self.callback = callback
        self.frame = ttk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.build_ui()

    def load_data(self):
        if not DATA_FILE.exists():
            return {}
        with open(DATA_FILE, 'rb') as f:
            encrypted = f.read()
        try:
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except Exception:
            messagebox.showerror("Error", "Cannot read encrypted data, Master Password seems to be inccorect")
            return {}

    def save_data(self, data):
        serialized = json.dumps(data, indent=4).encode()
        encrypted = self.fernet.encrypt(serialized)
        with open(DATA_FILE, 'wb') as f:
            f.write(encrypted)

    def build_ui(self):
        ttk.Label(self.frame, text="Select a file to delete:", font=("Segoe UI", 14)).pack(pady=10)

        self.file_listbox = tk.Listbox(self.frame, height=10, width=50)
        self.file_listbox.pack(pady=10)

        self.data = self.load_data()
        self.filenames = list(self.data.keys())

        if not self.filenames:
            ttk.Label(self.frame, text="No entries available to delete.").pack(pady=10)
            ttk.Button(self.frame, text="← Go Back", command=self.go_back).pack(pady=15)
            return

        for filename in self.filenames:
            self.file_listbox.insert(tk.END, filename)

        delete_btn = ttk.Button(self.frame, text="Delete Selected File", command=self.confirm_delete)
        delete_btn.pack(pady=10)

        back_btn = ttk.Button(self.frame, text="Back", command=self.go_back)
        back_btn.pack(pady=5)

    def confirm_delete(self):
        selected = self.file_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No file selected.")
            return

        index = selected[0]
        filename = self.filenames[index]

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{filename}'?")
        if confirm:
            del self.data[filename]
            self.save_data(self.data)
            messagebox.showinfo("Success", f"'{filename}' has been deleted.")
            self.frame.destroy()
            self.callback()
        else:
            messagebox.showinfo("Cancelled", "Deletion cancelled.")

    def go_back(self):
        self.frame.destroy()
        self.callback()