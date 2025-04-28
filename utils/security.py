import bcrypt
from utils.logger import Logger


def hash_password(password):
    """Hash a password using bcrypt."""
    try:
        # Convert password to bytes
        password_bytes = password.encode('utf-8')

        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)

        # Return hash as string
        return hashed.decode('utf-8')
    except Exception as e:
        logger = Logger()
        logger.log_error(f"Password hashing error: {str(e)}")
        return None


def verify_password(password, hashed_password):
    """Verify a password against a hash."""
    try:
        # Convert password and hash to bytes
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')

        # Verify
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logger = Logger()
        logger.log_error(f"Password verification error: {str(e)}")
        return False
