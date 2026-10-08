# User Registration and Authentication Service
from database import db_query, db_execute, mydb, verify_password
from customer import Customer
from bank import Bank
import random
import re

def register_user(username, password, name, age, city):
    """Programmatic user registration helper for UI and CLI."""
    username = username.strip()
    name = name.strip()
    city = city.strip()

    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username):
        return False, "Username must be 3-20 characters long and contain only letters, numbers, and underscores.", None

    if len(password.strip()) < 4:
        return False, "Password must be at least 4 characters long.", None

    if not name:
        return False, "Name cannot be empty.", None

    try:
        age_int = int(age)
        if age_int < 10 or age_int > 120:
            return False, "Please enter a valid age (10-120).", None
    except ValueError:
        return False, "Age must be a valid number.", None

    if not city:
        return False, "City cannot be empty.", None

    # Check if username exists
    existing = db_query("SELECT username FROM customers WHERE username = %s", (username,))
    if existing:
        return False, f"Username '{username}' already exists. Please choose a different username.", None

    # Generate unique 8-digit account number
    while True:
        acc_num = random.randint(10000000, 99999999)
        check_acc = db_query("SELECT account_number FROM customers WHERE account_number = %s", (acc_num,))
        if not check_acc:
            break

    # Create customer
    customer = Customer(username, password, name, age_int, city, acc_num, balance=0, status=1)
    customer.createuser()

    return True, f"Registration successful! Your Account Number is {acc_num}.", acc_num

def authenticate_user(username, password):
    """Programmatic user authentication helper for UI and CLI."""
    username = username.strip()
    if not username or not password:
        return False, "Username and password cannot be empty.", None

    res = db_query("SELECT username, password, account_number, name, age, city, balance FROM customers WHERE username = %s", (username,))
    if not res:
        return False, "Account does not exist. Please check username or Sign Up.", None

    stored_username, stored_password, acc_num, name, age, city, balance = res[0]

    if verify_password(stored_password, password):
        user_info = {
            "username": stored_username,
            "account_number": acc_num,
            "name": name,
            "age": age,
            "city": city,
            "balance": float(balance)
        }
        return True, "Authentication successful!", user_info

    return False, "Invalid password. Please try again.", None

def SignUp():
    """Interactive CLI SignUp handler."""
    print("\n--- NEW USER REGISTRATION ---")
    username = input("Create Username (3-20 characters): ")
    password = input("Enter Password: ")
    name = input("Enter Full Name: ")
    age = input("Enter Age: ")
    city = input("Enter City: ")

    success, msg, acc_num = register_user(username, password, name, age, city)
    print(f"\n{msg}")
    return success

def SignIn():
    """Interactive CLI SignIn handler."""
    print("\n--- USER LOGIN ---")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    success, msg, user_info = authenticate_user(username, password)
    if success:
        print(f"\nWelcome back, {user_info['name']}!")
        return user_info['username']
    else:
        print(f"\nLogin Failed: {msg}")
        return None
