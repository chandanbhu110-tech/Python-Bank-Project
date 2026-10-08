# Database Management Banking System
import sqlite3
import os
import hashlib
import binascii

# Global database configuration
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bank.db")
USE_MYSQL = False
mydb = None
cursor = None

def get_connection():
    """Get a database connection (SQLite by default, fallback from MySQL if unavailable)."""
    global USE_MYSQL, mydb, cursor
    
    # Try MySQL if explicitly configured in environment variables
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_db = os.getenv("MYSQL_DB", "bank")
    
    if mysql_host and mysql_user:
        try:
            import mysql.connector as sql
            conn = sql.connect(
                host=mysql_host,
                user=mysql_user,
                passwd=mysql_password,
                database=mysql_db
            )
            USE_MYSQL = True
            return conn
        except Exception:
            pass
            
    # Default to SQLite (Zero configuration required)
    USE_MYSQL = False
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize default connection
mydb = get_connection()

class DatabaseCursorProxy:
    """Compatibility proxy for raw cursor calls."""
    def execute(self, query, params=()):
        conn = get_connection()
        c = conn.cursor()
        if USE_MYSQL:
            formatted_query = query.replace('?', '%s')
            c.execute(formatted_query, params)
        else:
            formatted_query = query.replace('%s', '?')
            c.execute(formatted_query, params)
        return c

    def fetchall(self):
        return []

cursor = DatabaseCursorProxy()

def hash_password(password: str, salt: str = None) -> str:
    """Hash password using SHA-256 with salt."""
    if not salt:
        salt = binascii.hexlify(os.urandom(16)).decode('utf-8')
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    pwd_hash_hex = binascii.hexlify(pwd_hash).decode('utf-8')
    return f"{salt}${pwd_hash_hex}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a password against stored hash or plaintext fallback for legacy entries."""
    if '$' in stored_password:
        try:
            salt, stored_hash = stored_password.split('$', 1)
            pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt.encode('utf-8'), 100000)
            pwd_hash_hex = binascii.hexlify(pwd_hash).decode('utf-8')
            return pwd_hash_hex == stored_hash
        except Exception:
            return False
    # Direct comparison for legacy plaintext passwords
    return stored_password == provided_password

def db_query(query, params=()):
    """Execute a SELECT query with parameters safely."""
    conn = get_connection()
    try:
        c = conn.cursor()
        if USE_MYSQL:
            formatted_query = query.replace('?', '%s')
            c.execute(formatted_query, params)
            res = c.fetchall()
            conn.close()
            return res
        else:
            formatted_query = query.replace('%s', '?')
            c.execute(formatted_query, params)
            res = c.fetchall()
            # Convert sqlite3.Row objects to tuple list for backward compatibility
            tuple_res = [tuple(row) for row in res]
            conn.close()
            return tuple_res
    except Exception as e:
        conn.close()
        raise e

def db_execute(query, params=()):
    """Execute INSERT, UPDATE, DELETE query with parameters safely."""
    conn = get_connection()
    try:
        c = conn.cursor()
        if USE_MYSQL:
            formatted_query = query.replace('?', '%s')
            c.execute(formatted_query, params)
        else:
            formatted_query = query.replace('%s', '?')
            c.execute(formatted_query, params)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        raise e

def createcustomertable():
    """Create all required tables for banking application."""
    conn = get_connection()
    c = conn.cursor()
    
    # Table for customers
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(100) NOT NULL,
            age INTEGER NOT NULL,
            city VARCHAR(100) NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            account_number INTEGER UNIQUE NOT NULL,
            status INTEGER NOT NULL DEFAULT 1
        )
    ''')
    
    # Table for transactions
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL,
            account_number INTEGER NOT NULL,
            remarks VARCHAR(100) NOT NULL,
            amount REAL NOT NULL,
            timedate VARCHAR(50) NOT NULL,
            target_account INTEGER DEFAULT NULL,
            FOREIGN KEY (username) REFERENCES customers(username)
        )
    ''')
    
    conn.commit()
    conn.close()

# Auto-initialize database tables when module is loaded
createcustomertable()

if __name__ == "__main__":
    createcustomertable()
    print("Database tables initialized successfully.")