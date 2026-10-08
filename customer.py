# Customer Details Model
from database import db_query, db_execute, hash_password

class Customer:
    def __init__(self, username, password, name, age, city, account_number, balance=0, status=1):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__age = int(age) if isinstance(age, (int, str)) and str(age).isdigit() else 18
        self.__city = city
        self.__account_number = int(account_number)
        self.__balance = float(balance)
        self.__status = int(status)

    @property
    def username(self):
        return self.__username

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def city(self):
        return self.__city

    @property
    def account_number(self):
        return self.__account_number

    @property
    def balance(self):
        return self.__balance

    def createuser(self):
        """Save new customer to database with hashed password and parameterized query."""
        hashed_pwd = hash_password(self.__password)
        db_execute(
            "INSERT INTO customers (username, password, name, age, city, balance, account_number, status) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (self.__username, hashed_pwd, self.__name, self.__age, self.__city, self.__balance, self.__account_number, self.__status)
        )
        return True

    @staticmethod
    def get_by_username(username):
        """Fetch customer details by username."""
        res = db_query("SELECT username, name, age, city, balance, account_number, status FROM customers WHERE username = %s", (username,))
        if res:
            row = res[0]
            return {
                "username": row[0],
                "name": row[1],
                "age": row[2],
                "city": row[3],
                "balance": float(row[4]),
                "account_number": row[5],
                "status": row[6]
            }
        return None

    @staticmethod
    def get_by_account_number(account_number):
        """Fetch customer details by account number."""
        res = db_query("SELECT username, name, age, city, balance, account_number, status FROM customers WHERE account_number = %s", (account_number,))
        if res:
            row = res[0]
            return {
                "username": row[0],
                "name": row[1],
                "age": row[2],
                "city": row[3],
                "balance": float(row[4]),
                "account_number": row[5],
                "status": row[6]
            }
        return None