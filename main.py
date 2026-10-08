# Bank Management System - Main Entry Point
import register
import bank
from database import db_query
import sys
import subprocess
import os

blocked = [
    "union", "select", "insert", "update", "delete",
    "drop", "alter", "create", "truncate",
    "--", ";", "'", '"'
]

def launch_desktop_gui():
    """Launch Tkinter Desktop Application."""
    try:
        gui_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui_app.py")
        print("Starting Banking Desktop GUI...")
        subprocess.Popen([sys.executable, gui_script])
    except Exception as e:
        print(f"Error launching GUI: {e}")

def launch_web_ui():
    """Launch Flask Web UI Application."""
    try:
        web_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
        print("Starting Banking Web Server at http://127.0.0.1:5000 ...")
        subprocess.Popen([sys.executable, web_script])
    except Exception as e:
        print(f"Error launching Web UI: {e}")

def main_cli():
    print("==========================================")
    print("      WELCOME TO BANK MANAGEMENT SYSTEM   ")
    print("==========================================")

    user = None
    account_number = None

    while True:
        try:
            print("\n--- MAIN MENU ---")
            print("1. SignUp (Create New Account)")
            print("2. SignIn (Access Your Account)")
            print("3. Launch Desktop UI App 🖥️")
            print("4. Launch Web UI App 🌐")
            print("5. Exit")
            
            choice = input("\nChoose an option (1-5): ").strip()

            if choice == "1":
                register.SignUp()

            elif choice == "2":
                user = register.SignIn()
                if not user:
                    continue

                if any(word in user.lower() for word in blocked):
                    print("Invalid username pattern detected.")
                    user = None
                    continue

                res = db_query("SELECT account_number FROM customers WHERE username = %s", (user,))
                if not res:
                    print("Could not find account details.")
                    user = None
                    continue

                account_number = res[0][0]
                break

            elif choice == "3":
                launch_desktop_gui()

            elif choice == "4":
                launch_web_ui()

            elif choice == "5":
                print("Thank you for using Bank Management System! Goodbye.")
                sys.exit(0)

            else:
                print("Please enter a valid option between 1 and 5.")

        except ValueError:
            print("Invalid input format.")
        except KeyboardInterrupt:
            print("\nExiting application...")
            sys.exit(0)

    # Banking Services Loop
    bobj = bank.Bank(user, account_number)

    while True:
        try:
            print(f"\n==========================================")
            print(f" Welcome {user.capitalize()} | Account: {account_number}")
            print(f"==========================================")
            print("1. Balance Enquiry")
            print("2. Cash Deposit")
            print("3. Cash Withdraw")
            print("4. Fund Transfer")
            print("5. Transaction History")
            print("6. Logout / Exit")
            
            facility = input("\nChoose an option (1-6): ").strip()

            if facility == "1":
                bobj.balanceequiry()

            elif facility == "2":
                try:
                    amt_str = input("Enter amount to deposit: ").strip()
                    amount = float(amt_str)
                    bobj.deposit(amount)
                except ValueError:
                    print("Please enter a valid numeric amount.")

            elif facility == "3":
                try:
                    amt_str = input("Enter amount to withdraw: ").strip()
                    amount = float(amt_str)
                    bobj.withdraw(amount)
                except ValueError:
                    print("Please enter a valid numeric amount.")

            elif facility == "4":
                try:
                    receiver_str = input("Enter receiver account number: ").strip()
                    amt_str = input("Enter amount to transfer: ").strip()
                    receive = int(receiver_str)
                    amount = float(amt_str)
                    bobj.fundtransfer(receive, amount)
                except ValueError:
                    print("Please enter valid numeric values for account number and amount.")

            elif facility == "5":
                history = bobj.get_transaction_history()
                print(f"\n--- TRANSACTION HISTORY ({len(history)} records) ---")
                if not history:
                    print("No transactions found.")
                else:
                    print(f"{'Date/Time':<22} | {'Account':<10} | {'Type/Remarks':<30} | {'Amount':<10}")
                    print("-" * 80)
                    for item in history:
                        print(f"{item['timedate']:<22} | {item['account_number']:<10} | {item['remarks']:<30} | ${item['amount']:<10.2f}")

            elif facility == "6":
                print(f"Thank you for using Bank Management System, {user.capitalize()}! Goodbye.")
                break

            else:
                print("Please choose an option between 1 and 6.")

        except ValueError:
            print("Please enter a valid choice.")
        except KeyboardInterrupt:
            print("\nLogging out...")
            break

if __name__ == "__main__":
    main_cli()
