# Flask Web UI Application for Bank Management System
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import register
from bank import Bank
import webbrowser
from threading import Timer
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_current_bank_service():
    """Helper to instantiate Bank service for logged-in user."""
    if "username" in session and "account_number" in session:
        return Bank(session["username"], session["account_number"])
    return None

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        success, msg, user_data = register.authenticate_user(username, password)
        if success:
            session["username"] = user_data["username"]
            session["account_number"] = user_data["account_number"]
            session["name"] = user_data["name"]
            session["city"] = user_data["city"]
            session["age"] = user_data["age"]
            flash(f"Welcome back, {user_data['name']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash(msg, "error")

    return render_template("login.html")

@app.route("/register", methods=["POST"])
def handle_register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    name = request.form.get("name", "").strip()
    age = request.form.get("age", "").strip()
    city = request.form.get("city", "").strip()

    success, msg, acc_num = register.register_user(username, password, name, age, city)
    if success:
        flash(msg, "success")
    else:
        flash(msg, "error")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    bank_service = get_current_bank_service()
    if not bank_service:
        flash("Please log in to access your dashboard.", "error")
        return redirect(url_for("login"))

    balance = bank_service.get_balance()
    transactions = bank_service.get_transaction_history()

    return render_template("dashboard.html", balance=balance, transactions=transactions)

@app.route("/deposit", methods=["POST"])
def deposit():
    bank_service = get_current_bank_service()
    if not bank_service:
        return redirect(url_for("login"))

    try:
        amount = float(request.form.get("amount", 0))
        success, msg, _ = bank_service.deposit(amount)
        if success:
            flash(msg, "success")
        else:
            flash(msg, "error")
    except ValueError:
        flash("Please enter a valid numeric deposit amount.", "error")

    return redirect(url_for("dashboard"))

@app.route("/withdraw", methods=["POST"])
def withdraw():
    bank_service = get_current_bank_service()
    if not bank_service:
        return redirect(url_for("login"))

    try:
        amount = float(request.form.get("amount", 0))
        success, msg, _ = bank_service.withdraw(amount)
        if success:
            flash(msg, "success")
        else:
            flash(msg, "error")
    except ValueError:
        flash("Please enter a valid numeric withdrawal amount.", "error")

    return redirect(url_for("dashboard"))

@app.route("/transfer", methods=["POST"])
def transfer():
    bank_service = get_current_bank_service()
    if not bank_service:
        return redirect(url_for("login"))

    try:
        receiver = int(request.form.get("receiver_account", 0))
        amount = float(request.form.get("amount", 0))
        success, msg, _ = bank_service.fundtransfer(receiver, amount)
        if success:
            flash(msg, "success")
        else:
            flash(msg, "error")
    except ValueError:
        flash("Please enter valid numbers for receiver account and amount.", "error")

    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out safely.", "info")
    return redirect(url_for("login"))

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
