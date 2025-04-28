import sqlite3
from datetime import datetime
import os
from utils.logger import Logger


class Database:
    def __init__(self, db_path="budget_manager.db"):
        self.db_path = db_path
        self.logger = Logger()

    def initialize(self):
        """Initialize the database with required tables."""
        try:
            # Create database directory if it doesn't exist
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check if users table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            table_exists = cursor.fetchone()

            if table_exists:
                # Check if email column exists in users table
                cursor.execute("PRAGMA table_info(users)")
                columns = cursor.fetchall()
                column_names = [column[1] for column in columns]

                if 'email' not in column_names:
                    # Add email column to existing users table
                    cursor.execute("ALTER TABLE users ADD COLUMN email TEXT DEFAULT ''")
                    self.logger.log_info("Added email column to users table")
            else:
                # Create users table with email column
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT DEFAULT '',
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                self.logger.log_info("Created users table")

            # Create transactions table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')

            # Create categories table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')

            # Insert default categories
            default_categories = [
                "Food", "Transportation", "Housing", "Entertainment",
                "Utilities", "Healthcare", "Education", "Shopping",
                "Personal", "Debt", "Savings", "Income", "Other"
            ]

            for category in default_categories:
                cursor.execute(
                    "INSERT OR IGNORE INTO categories (name, user_id) VALUES (?, NULL)",
                    (category,)
                )

            conn.commit()
            conn.close()

            self.logger.log_info("Database initialized successfully")
            return True
        except Exception as e:
            self.logger.log_error(f"Database initialization error: {str(e)}")
            return False

    def create_user(self, username, email, password):
        """Create a new user in the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )

            user_id = cursor.lastrowid

            conn.commit()
            conn.close()

            return user_id
        except Exception as e:
            self.logger.log_error(f"Error creating user: {str(e)}")
            return None

    def get_user_by_username(self, username):
        """Get user data by username."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )

            user = cursor.fetchone()

            conn.close()

            if user:
                return dict(user)
            else:
                return None
        except Exception as e:
            self.logger.log_error(f"Error getting user: {str(e)}")
            return None

    def create_transaction(self, user_id, description, amount, category, date):
        """Create a new transaction in the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Convert date to string if it's a datetime object
            if isinstance(date, datetime):
                date = date.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "INSERT INTO transactions (user_id, description, amount, category, date) VALUES (?, ?, ?, ?, ?)",
                (user_id, description, amount, category, date)
            )

            transaction_id = cursor.lastrowid

            conn.commit()
            conn.close()

            return transaction_id
        except Exception as e:
            self.logger.log_error(f"Error creating transaction: {str(e)}")
            return None

    def get_transactions_by_user(self, user_id):
        """Get all transactions for a user."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC",
                (user_id,)
            )

            transactions = cursor.fetchall()

            conn.close()

            # Convert to list of dictionaries and parse dates
            result = []
            for t in transactions:
                t_dict = dict(t)
                # Convert date string to datetime object
                t_dict["date"] = datetime.strptime(t_dict["date"], "%Y-%m-%d %H:%M:%S")
                result.append(t_dict)

            return result
        except Exception as e:
            self.logger.log_error(f"Error getting transactions: {str(e)}")
            return []

    def get_transaction_by_id(self, transaction_id):
        """Get transaction data by ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM transactions WHERE id = ?",
                (transaction_id,)
            )

            transaction = cursor.fetchone()

            conn.close()

            if transaction:
                t_dict = dict(transaction)
                # Convert date string to datetime object
                t_dict["date"] = datetime.strptime(t_dict["date"], "%Y-%m-%d %H:%M:%S")
                return t_dict
            else:
                return None
        except Exception as e:
            self.logger.log_error(f"Error getting transaction: {str(e)}")
            return None

    def update_transaction(self, transaction_id, description, amount, category, date):
        """Update an existing transaction."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Convert date to string if it's a datetime object
            if isinstance(date, datetime):
                date = date.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "UPDATE transactions SET description = ?, amount = ?, category = ?, date = ? WHERE id = ?",
                (description, amount, category, date, transaction_id)
            )

            conn.commit()
            conn.close()

            return cursor.rowcount > 0
        except Exception as e:
            self.logger.log_error(f"Error updating transaction: {str(e)}")
            return False

    def delete_transaction(self, transaction_id):
        """Delete a transaction."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM transactions WHERE id = ?",
                (transaction_id,)
            )

            conn.commit()
            conn.close()

            return cursor.rowcount > 0
        except Exception as e:
            self.logger.log_error(f"Error deleting transaction: {str(e)}")
            return False
