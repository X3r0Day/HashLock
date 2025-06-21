import tkinter as tk

from tkinter import(
    ttk,
    messagebox
)



from pathlib import Path
from cryptography.fernet import Fernet
import json


from PIL import(
    Image,
    ImageTk
)

from .save import user_data_path

DATA_FILE = user_data_path("stor/data.json")

def load_icon(filename, size=(20, 20)):
    img_path = Path(__file__).parent.parent / "icon" / filename
    img = Image.open(img_path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

class NewFileUI:
    def __init__(self, master, fernet: Fernet, callback=None):
        self.master = master
        self.fernet = fernet
        self.callback = callback

        self.frame = ttk.Frame(master, padding=20)
        self.frame.pack(fill="both", expand=True)

        self.icons = {
            "add": load_icon("add.png", (24, 24)),
            "save": load_icon("save.png", (24, 24)),
            "cancel": load_icon("cancel.png", (24, 24)),
        }

        ttk.Label(self.frame, text="Create New Secure File", image=self.icons["add"], compound="left",
                  font=("Segoe UI", 16)).pack(pady=(0, 15))

        self.fields = {}

        labels = ["File Name", "Email", "Username", "Password", "Notes"]
        for i, label in enumerate(labels):
            ttk.Label(self.frame, text=label + ":").pack(anchor="w", pady=(5, 0))
            entry = ttk.Entry(self.frame, width=50)
            entry.pack(pady=(0, 10))
            self.fields[label.lower().replace(" ", "_")] = entry

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Create", image=self.icons["save"], compound="left",
                   command=self.new_file).grid(row=0, column=0, padx=5)

        ttk.Button(btn_frame, text="Cancel", image=self.icons.get("cancel"), compound="left",
                   command=self.cancel).grid(row=0, column=1, padx=5)

        self.status_label = ttk.Label(self.frame, text="", foreground="red")
        self.status_label.pack()

    def load_data(self):
        if not DATA_FILE.exists():
            return {}
        with open(DATA_FILE, "rb") as f:
            encrypted = f.read()
        try:
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode("utf-8"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt data: {e}")
            return {}

    def save_data(self, data):
        json_bytes = json.dumps(data).encode("utf-8")
        encrypted = self.fernet.encrypt(json_bytes)
        with open(DATA_FILE, "wb") as f:
            f.write(encrypted)

    def new_file(self):
        data = self.load_data()

        f_name = self.fields["file_name"].get().strip()
        if not f_name:
            self.status_label.config(text="File name cannot be empty!")
            return

        if f_name in data:
            self.status_label.config(text=f"File '{f_name}' already exists. Choose another name or open it.")
            return

        email = self.fields["email"].get().strip()
        username = self.fields["username"].get().strip()
        password = self.fields["password"].get().strip()
        notes = self.fields["notes"].get().strip()

        data[f_name] = {
            "email": email,
            "username": username,
            "password": password,
            "notes": notes,
        }

        self.save_data(data)

        self.clear_fields()

        if self.callback:
            self.frame.destroy()
            self.callback(True)

    def clear_fields(self):
        for entry in self.fields.values():
            entry.delete(0, tk.END)

    def cancel(self):
        self.frame.destroy()
        if self.callback:
            self.callback(False)