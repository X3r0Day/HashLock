import json
from pathlib import Path
from cryptography.fernet import Fernet
from .save import user_data_path

from PIL import (
    Image,
    ImageTk
)


import tkinter as tk

from tkinter import (
    ttk,
    messagebox
)


DATA_FILE = user_data_path("stor/data.json")

def load_icon(filename, size=(20, 20)):
    img = Image.open(Path(__file__).parent.parent / "icon" / filename)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

class OpenEditFileUI:
    def __init__(self, master, fernet: Fernet, callback):
        self.master = master
        self.fernet = fernet
        self.callback = callback
        self.frame = ttk.Frame(master, padding=20)
        self.frame.pack(fill="both", expand=True)

        self.data = self.load_encrypted_data()
        self.filenames = list(self.data.keys())

        self.icons = {
            "add": load_icon("add.png"),
            "big_folder": load_icon("big_folder.png"),
            "key": load_icon("key.png"),
            "lock": load_icon("lock.png"),
            "pencil": load_icon("white_pencil.png"),
            "view": load_icon("white_view.png"),
            "bin": load_icon("bin.png"),
            "back": load_icon("white_LArrow.png"),
        }

        self.build_ui()
        

    def load_encrypted_data(self):
        if not DATA_FILE.exists():
            return {}
        with open(DATA_FILE, 'rb') as f:
            encrypted = f.read()
        try:
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except Exception as e:
            messagebox.showerror("Decryption Failed", f"Error: {e}")
            return {}

    def save_encrypted_data(self):
        encrypted = self.fernet.encrypt(json.dumps(self.data, indent=4).encode())
        with open(DATA_FILE, 'wb') as f:
            f.write(encrypted)

    def build_ui(self):
        ttk.Label(self.frame, image=self.icons["big_folder"], text="Stored Files", compound="left", width=10, font=("Segoe UI", 16)).pack(pady=10)

        if not self.filenames:
            ttk.Label(self.frame, text="No files found.", foreground="gray").pack(pady=10)
            ttk.Button(self.frame, text="← Go Back", command=self.go_back).pack(pady=15)
            return

        self.listbox = tk.Listbox(self.frame, height=10, width=50)
        self.listbox.pack(pady=10)
        for filename in self.filenames:
            self.listbox.insert(tk.END, filename)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, image=self.icons["view"], text="View", compound="left", command=self.view_selected, width=10).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, image=self.icons["pencil"], text="Edit", compound="left", command=self.edit_selected, width=10).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="← Go Back", command=self.go_back).grid(row=0, column=2, padx=10)

    def get_selected_filename(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file.")
            return None
        return self.filenames[selection[0]]

    def view_selected(self):
        filename = self.get_selected_filename()
        if not filename:
            return

        entry = self.data.get(filename)
        if not entry:
            messagebox.showerror("Error", "File data missing.")
            return

        info_text = (
            f"{filename}\n\n"
            f"Email: {entry.get('email', '')}\n"
            f"Username: {entry.get('username', '')}\n"
            f"Password: {entry.get('password', '')}\n"
            f"Notes:\n{entry.get('notes', '')}\n"
        )
        self.show_info_popup("File Info", info_text)
    

    # The old messagebox wasn't looking very fine on hyprland(tho it was okay on windows... but I use arch, btw with hyprland. so yes.)

    def show_info_popup(self, title, text):
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.resizable(True, True)

        width, height = 500, 350
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")

        padding = 15
        popup_frame = ttk.Frame(popup, padding=padding)
        popup_frame.pack(fill="both", expand=True)

        text_widget = tk.Text(
            popup_frame,
            wrap="word",
            font=("Segoe UI", 12),
            bg=popup.cget("bg"),
            fg="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )

        text_widget.pack(side="left", fill="both", expand=True)
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")

        scrollbar = ttk.Scrollbar(popup_frame, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

        close_btn = ttk.Button(popup, text="Close", command=popup.destroy)
        close_btn.pack(pady=(5, 10))

        popup.transient(self.master)
        popup.grab_set()
        popup.focus_force()

    def edit_selected(self):
        filename = self.get_selected_filename()
        if not filename:
            return

        entry = self.data.get(filename, {})
        self.frame.destroy()

        EditFormUI(self.master, self.fernet, filename, entry, self.data, self.save_encrypted_data, self.callback)

    def go_back(self):
        self.frame.destroy()
        self.callback()


class EditFormUI:
    def __init__(self, master, fernet, filename, entry, data, save_func, callback):
        self.master = master
        self.filename = filename
        self.entry = entry
        self.data = data
        self.save_func = save_func
        self.callback = callback

        self.icons = {
            "save": load_icon("save.png"),
            "pencil": load_icon("white_pencil.png"),
        }

        self.frame = ttk.Frame(master, padding=20)
        self.frame.pack(fill="both", expand=True)

        ttk.Label(self.frame, image=self.icons["pencil"], text=f"Edit File: {filename}", compound="left", font=("Segoe UI", 16)).pack(pady=10)

        self.fields = {}
        for field in ["email", "username", "password", "notes"]:
            ttk.Label(self.frame, text=field.capitalize() + ":").pack(anchor="w")
            entry_box = ttk.Entry(self.frame, width=50)
            entry_box.insert(0, self.entry.get(field, ""))
            entry_box.pack(pady=5)
            self.fields[field] = entry_box

        ttk.Button(self.frame, image=self.icons["save"], text="Save", compound="left", command=self.save).pack(pady=10)
        ttk.Button(self.frame, text="← Cancel", command=self.cancel).pack(pady=5)

    def save(self):
        for field, widget in self.fields.items():
            value = widget.get().strip()
            if value:
                self.entry[field] = value

        self.data[self.filename] = self.entry
        self.save_func()
        messagebox.showinfo("Success", f"{self.filename} updated.")
        self.frame.destroy()
        self.callback()

    def cancel(self):
        self.frame.destroy()
        self.callback()
