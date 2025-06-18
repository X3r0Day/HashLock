# HashLock Password Manager

[![License](https://img.shields.io/github/license/X3r0Day/HashLock)](https://github.com/X3r0Day/HashLock/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-early--development-orange)](https://github.com/X3r0Day/HashLock)
[![CodeFactor](https://www.codefactor.io/repository/github/x3r0day/hashlock/badge)](https://www.codefactor.io/repository/github/x3r0day/hashlock/issues)

> A secure and easy-to-use password manager with a clean Tkinter GUI.  
> Master password authentication with bcrypt and encrypted file storage using Fernet.

---

## Overview

Keep all your secrets safe with HashLock in fully offline and secure environment.

- **Cross-Platform Compatibility** - Works the same in Linux, Windows, Mac!
- **Fully offline** - No network requests are made! It's totally offline!!
- **Master Password Protection** - With bcrypt hashing, your secrets are kept secret!
- **Data Encryption** - Your secrets can only be accessed with Master Password.


HashLock Password Manager is designed to keep your credentials safe with encryption and really simple GUI usability.

Set up a master password, securely storing encrypted password files, and managing them via an intuitive interface.

## How Does It Work?
When you enter details, your secrets are stored in a `data.json` file with **Fernet** cryptographic encryption where key is generated directly from your **Master  Password**!

---

## Installation


### Windows/Linux/MacOS
```
git clone https://github.com/X3r0Day/HashLock.git && cd HashLock
pip install -r requirements.txt
python3 main.py
```

---

## To-Do 

- Port the entire CLI application to a full-featured GUI
- Make text more readable and nice
- Add random password generator
- Add Backup/Import feature


---

## Contributing

Contributions are welcome!  
If you want to help improve HashLock, please:

- Open issues to report bugs or request features
- Fork the repository and submit pull requests
- Follow the existing code style for consistency
- Be respectful and clear in communication

For major changes, please open a discussion issue first.



---

## License

HashLock Password Manager is licensed under the MIT License.  
See the [`LICENSE`](https://github.com/X3r0Day/HashLock/blob/main/LICENSE) file for details.

---
