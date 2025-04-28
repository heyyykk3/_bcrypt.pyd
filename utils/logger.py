import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, log_file="budget_manager.log"):
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def log_info(self, message):
        """Log an info message."""
        logging.info(message)
        print(f"INFO: {message}")

    def log_error(self, message):
        """Log an error message."""
        logging.error(message)
        print(f"ERROR: {message}")

    def log_warning(self, message):
        """Log a warning message."""
        logging.warning(message)
        print(f"WARNING: {message}")
