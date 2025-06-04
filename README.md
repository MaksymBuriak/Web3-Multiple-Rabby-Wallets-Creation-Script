# ✅ Rabby Wallet Auto-Creator (Chrome Extension Automation)

📜 Python + Selenium script to automatically create multiple Rabby Wallets using the Rabby Chrome Extension.

---

## 🚀 Features

- 🧠 Automatically creates Rabby wallets in Chrome
- 🧾 Imports seed phrase and sets password
- 🧠 Randomized Chrome user-agents and sandboxed sessions
- 📥 Generates addresses and seed phrases saved in `result.txt`
- 💡 Supports Chrome Extension (unpacked mode)
- 🪟 Cross-platform: Windows + macOS
- 🐞 Error handling and session fallback logic

---

## 📂 Project Structure

| File              | Description                                         |
|-------------------|-----------------------------------------------------|
| `main.py`         | 👨‍💻 Main automation script for wallet creation       |
| `config.py`       | ⚙️ Settings (number of wallets, password)           |
| `requirements.txt`| 📦 All Python dependencies                          |
| `setup.bat`       | 🪟 Windows one-click setup script                   |
| `setup.sh`        | 🍎 macOS/Linux one-click setup script               |
| `result.txt`      | 📄 Output: addresses and seed phrases (auto-created)|

---

## ⚙️ Setup

### 🔧 Windows

1. Make sure Python 3.11+ is installed.
2. Run:
```bat
setup.bat
```

### 🍎 macOS/Linux

1. Make sure Python 3.11+ is installed.
2. Run:
```bash
chmod +x setup.sh
./setup.sh
```

This creates a `.venv` environment and installs all dependencies from `requirements.txt`.

📦 Dependencies:
```
beautifulsoup4
fake-useragent
python-dotenv
randomuser
requests
selenium
webdriver-manager
```

---

## ▶️ Run

To start creating wallets:

```bash
python main.py
```

💡 The script will:
- Create isolated Chrome profiles
- Load Rabby Wallet extension
- Generate wallets with random sessions
- Save the seed phrase + address to `result.txt`

---

## ⚙️ Configuration

Edit `config.py`:

```python
amount = 50  # Number of wallets to create
password = 'YourStrongPassword123'
```

---

## 📝 Output

Wallet addresses and their seed phrases are saved line-by-line in:

```
result.txt
```

Format:
```
0xYourWalletAddress, word1 word2 word3 ... word12
```

---

## 📌 Notes

- This script will NOT interrupt with your personal Google Chrome opened in parallel
- The Chrome UI will be visible unless `--headless=new` is uncommented in the script.
- Each wallet uses a **temporary Chrome profile** (clean session).

---

## 📄 License

For educational and automation demonstration purposes only. Not intended for malicious use.
