from models.user import User
from database.db import Database
from utils.security import hash_password, verify_password
from utils.logger import Logger


class AuthController:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()

    def register(self, username, email, password):
        """Register a new user."""
        try:
            # Check if username already exists
            if self.db.get_user_by_username(username):
                self.logger.log_info(f"Registration failed: Username {username} already exists")
                return None

            # Hash password
            hashed_password = hash_password(password)

            # Create user
            user_id = self.db.create_user(username, email, hashed_password)

            if user_id:
                user = User(user_id, username, email)
                self.logger.log_info(f"User registered: {username}")
                return user
            else:
                self.logger.log_error(f"Failed to create user: {username}")
                return None
        except Exception as e:
            self.logger.log_error(f"Registration error: {str(e)}")
            return None

    def login(self, username, password):
        """Authenticate a user."""
        try:
            # Get user from database
            user_data = self.db.get_user_by_username(username)

            if not user_data:
                self.logger.log_info(f"Login failed: Username {username} not found")
                return None

            # Verify password
            if verify_password(password, user_data["password"]):
                user = User(user_data["id"], user_data["username"], user_data["email"])
                self.logger.log_info(f"User logged in: {username}")
                return user
            else:
                self.logger.log_info(f"Login failed: Invalid password for {username}")
                return None
        except Exception as e:
            self.logger.log_error(f"Login error: {str(e)}")
            return None
