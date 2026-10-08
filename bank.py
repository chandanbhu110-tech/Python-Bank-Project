# Bank Services Model
from database import db_query, db_execute
import datetime

class Bank:
    def __init__(self, username, account_number):
        self.__username = username
        self.__account_number = int(account_number)

    @property
    def username(self):
        return self.__username

    @property
    def account_number(self):
        return self.__account_number

    def create_transaction_table(self):
        """Maintained for backward compatibility."""
        pass

    def get_balance(self):
        """Retrieve current balance for user."""
        res = db_query("SELECT balance FROM customers WHERE username = %s", (self.__username,))
        if res:
            return float(res[0][0])
        return 0.0

    def balanceequiry(self):
        """Legacy method for balance enquiry."""
        balance = self.get_balance()
        print(f"{self.__username} Balance is ${balance:,.2f}")
        return balance

    def deposit(self, amount):
        """Deposit specified amount into user account."""
        amount = float(amount)
        if amount <= 0:
            msg = "Deposit amount must be greater than 0."
            print(msg)
            return False, msg, self.get_balance()

        current_balance = self.get_balance()
        new_balance = current_balance + amount

        # Update customer balance
        db_execute("UPDATE customers SET balance = %s WHERE username = %s", (new_balance, self.__username))

        # Log transaction
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_execute(
            "INSERT INTO transactions (username, account_number, remarks, amount, timedate) "
            "VALUES (%s, %s, %s, %s, %s)",
            (self.__username, self.__account_number, "Amount Deposit", amount, now_str)
        )

        msg = f"Successfully deposited ${amount:,.2f} into Account {self.__account_number}."
        print(msg)
        return True, msg, new_balance

    def withdraw(self, amount):
        """Withdraw specified amount from user account."""
        amount = float(amount)
        if amount <= 0:
            msg = "Withdrawal amount must be greater than 0."
            print(msg)
            return False, msg, self.get_balance()

        current_balance = self.get_balance()
        if amount > current_balance:
            msg = f"Insufficient balance (${current_balance:,.2f}). Please deposit money first."
            print(msg)
            return False, msg, current_balance

        new_balance = current_balance - amount

        # Update customer balance
        db_execute("UPDATE customers SET balance = %s WHERE username = %s", (new_balance, self.__username))

        # Log transaction
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_execute(
            "INSERT INTO transactions (username, account_number, remarks, amount, timedate) "
            "VALUES (%s, %s, %s, %s, %s)",
            (self.__username, self.__account_number, "Amount Withdraw", amount, now_str)
        )

        msg = f"Successfully withdrew ${amount:,.2f} from Account {self.__account_number}."
        print(msg)
        return True, msg, new_balance

    def fundtransfer(self, receive, amount):
        """Transfer funds from current account to receiver account number."""
        amount = float(amount)
        receive = int(receive)

        if amount <= 0:
            msg = "Transfer amount must be greater than 0."
            print(msg)
            return False, msg, self.get_balance()

        if receive == self.__account_number:
            msg = "Cannot transfer funds to your own account."
            print(msg)
            return False, msg, self.get_balance()

        current_balance = self.get_balance()
        if amount > current_balance:
            msg = f"Insufficient balance (${current_balance:,.2f}) for transfer."
            print(msg)
            return False, msg, current_balance

        # Verify receiver account exists
        receiver_res = db_query("SELECT username, balance FROM customers WHERE account_number = %s", (receive,))
        if not receiver_res:
            msg = f"Receiver Account Number {receive} does not exist."
            print(msg)
            return False, msg, current_balance

        receiver_username = receiver_res[0][0]
        receiver_balance = float(receiver_res[0][1])

        # Perform atomic transfer
        new_sender_balance = current_balance - amount
        new_receiver_balance = receiver_balance + amount

        # Update balances
        db_execute("UPDATE customers SET balance = %s WHERE username = %s", (new_sender_balance, self.__username))
        db_execute("UPDATE customers SET balance = %s WHERE account_number = %s", (new_receiver_balance, receive))

        # Record transaction for sender
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_execute(
            "INSERT INTO transactions (username, account_number, remarks, amount, timedate, target_account) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (self.__username, self.__account_number, f"Fund Transfer to {receive}", amount, now_str, receive)
        )

        # Record transaction for receiver
        db_execute(
            "INSERT INTO transactions (username, account_number, remarks, amount, timedate, target_account) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (receiver_username, receive, f"Fund Received from {self.__account_number}", amount, now_str, self.__account_number)
        )

        msg = f"Successfully transferred ${amount:,.2f} to Account {receive}."
        print(msg)
        return True, msg, new_sender_balance

    def get_transaction_history(self):
        """Fetch all transaction logs for user."""
        res = db_query(
            "SELECT timedate, account_number, remarks, amount, target_account "
            "FROM transactions WHERE username = %s OR account_number = %s ORDER BY id DESC",
            (self.__username, self.__account_number)
        )
        transactions = []
        for row in res:
            transactions.append({
                "timedate": row[0],
                "account_number": row[1],
                "remarks": row[2],
                "amount": float(row[3]),
                "target_account": row[4]
            })
        return transactions
