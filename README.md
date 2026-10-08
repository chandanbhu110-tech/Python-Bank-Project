# Bank Management System 🏦

A modern, secure, full-featured Python-based **Bank Management System** featuring **Desktop GUI (Tkinter)**, **Responsive Web Dashboard (Flask)**, and an **Interactive CLI**.

---

## 🌟 Key Features & Enhancements

- **Modern User Interfaces (UI)**:
  - 🖥️ **Desktop GUI App (`gui_app.py`)**: Built with Python Tkinter/ttk, featuring a sleek dark-slate theme, tabbed navigation, live balance card, quick deposit/withdrawal/transfer forms, and interactive transaction tables.
  - 🌐 **Web Dashboard (`app.py`)**: Built with Flask, HTML5, CSS3, and FontAwesome. Features gradient balance cards, smooth tab switches, modal notifications, responsive mobile/desktop layout, and transaction history badges.
  - 💻 **Interactive CLI (`main.py`)**: Enhanced command-line interface with input validation, menu options, and UI quick-launchers.

- **Zero-Setup Database Architecture**:
  - Out-of-the-box support for **SQLite (`bank.db`)** so the app runs instantly without needing external database servers.
  - Optional support for **MySQL** via environment variables (`MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`).

- **Security & Integrity**:
  - **SQL Injection Prevention**: All queries use parameterized statements (`?` / `%s`).
  - **Password Hashing**: Passwords stored securely using PBKDF2 with SHA-256 and unique salt.
  - **Atomic Transactions**: Money transfers update sender and receiver balances safely with complete transaction log records.
  - **Validation**: Enforces numeric checks, positive transaction bounds, valid age ranges, and unique 8-digit account number generation.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ installed on your system.

### Quick Start

1. **Install Dependencies** (Flask for Web UI):
   ```bash
   pip install flask
   ```

2. **Run Desktop GUI App**:
   ```bash
   python gui_app.py
   ```

3. **Run Web UI Dashboard**:
   ```bash
   python app.py
   ```
   *This automatically opens `http://127.0.0.1:5000` in your web browser.*

4. **Run Terminal / CLI App**:
   ```bash
   python main.py
   ```

5. **Run Automated Test Suite**:
   ```bash
   python temp.py
   ```

---

## 📁 Project Structure

```
Python-Bank-Project/
├── app.py              # Flask Web Application Server
├── bank.py             # Core Banking Logic (Deposit, Withdraw, Transfer, History)
├── customer.py         # Customer Domain Model
├── database.py         # Database Engine (SQLite / MySQL) & Password Security
├── gui_app.py          # Desktop GUI Application (Tkinter / ttk)
├── main.py             # Command Line Interface (CLI) Entry Point
├── register.py         # Authentication & User Registration Service
├── temp.py             # Automated Verification Test Runner
├── bank.db             # SQLite Database (Auto-created)
├── static/
│   └── css/
│       └── style.css   # Web UI Stylesheet (Dark Slate Glassmorphism Theme)
└── templates/
    ├── base.html       # Base HTML Layout & Navigation
    ├── login.html      # Web Login & Registration Page
    └── dashboard.html  # Web Dashboard & Transaction Activity
```

---

## 📊 Banking Operations

- **Account Registration**: Generates a unique 8-digit account number with hashed credentials.
- **Sign In**: Authenticates username and password against PBKDF2 salted hash.
- **Balance Enquiry**: Displays live account balance.
- **Cash Deposit**: Credits funds into the account and logs the transaction.
- **Cash Withdrawal**: Debits funds after checking for sufficient balance.
- **Fund Transfer**: Transfers money directly to another user's 8-digit account number atomically.
- **Transaction History**: Displays detailed logs with timestamp, type, target account, and amount.

---

## 🔒 Security Fixes Applied

- Standardized on parameterized queries across all database operations.
- Replaced dynamic table-per-user design with a unified `transactions` schema.
- Replaced plain text password storage with salted SHA-256 key derivation.
