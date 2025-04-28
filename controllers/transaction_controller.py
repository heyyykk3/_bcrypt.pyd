from models.transaction import Transaction
from database.db import Database
from utils.logger import Logger
from datetime import datetime


class TransactionController:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()

    def add_transaction(self, user_id, description, amount, category, date=None):
        """Add a new transaction."""
        try:
            if date is None:
                date = datetime.now()

            transaction_id = self.db.create_transaction(
                user_id=user_id,
                description=description,
                amount=amount,
                category=category,
                date=date
            )

            if transaction_id:
                self.logger.log_info(f"Transaction added: {description} (${amount:.2f})")
                return Transaction(
                    id=transaction_id,
                    user_id=user_id,
                    description=description,
                    amount=amount,
                    category=category,
                    date=date
                )
            else:
                self.logger.log_error(f"Failed to add transaction: {description}")
                return None
        except Exception as e:
            self.logger.log_error(f"Error adding transaction: {str(e)}")
            return None

    def get_user_transactions(self, user_id):
        """Get all transactions for a user."""
        try:
            transactions_data = self.db.get_transactions_by_user(user_id)

            transactions = []
            for t_data in transactions_data:
                transaction = Transaction(
                    id=t_data["id"],
                    user_id=t_data["user_id"],
                    description=t_data["description"],
                    amount=t_data["amount"],
                    category=t_data["category"],
                    date=t_data["date"]
                )
                transactions.append(transaction)

            return transactions
        except Exception as e:
            self.logger.log_error(f"Error getting transactions: {str(e)}")
            return []

    def update_transaction(self, transaction_id, description=None, amount=None, category=None, date=None):
        """Update an existing transaction."""
        try:
            # Get current transaction data
            transaction_data = self.db.get_transaction_by_id(transaction_id)

            if not transaction_data:
                self.logger.log_error(f"Transaction not found: {transaction_id}")
                return False

            # Update with new values or keep existing ones
            updated_description = description if description is not None else transaction_data["description"]
            updated_amount = amount if amount is not None else transaction_data["amount"]
            updated_category = category if category is not None else transaction_data["category"]
            updated_date = date if date is not None else transaction_data["date"]

            # Update in database
            success = self.db.update_transaction(
                transaction_id=transaction_id,
                description=updated_description,
                amount=updated_amount,
                category=updated_category,
                date=updated_date
            )

            if success:
                self.logger.log_info(f"Transaction updated: {transaction_id}")
                return True
            else:
                self.logger.log_error(f"Failed to update transaction: {transaction_id}")
                return False
        except Exception as e:
            self.logger.log_error(f"Error updating transaction: {str(e)}")
            return False

    def delete_transaction(self, transaction_id):
        """Delete a transaction."""
        try:
            success = self.db.delete_transaction(transaction_id)

            if success:
                self.logger.log_info(f"Transaction deleted: {transaction_id}")
                return True
            else:
                self.logger.log_error(f"Failed to delete transaction: {transaction_id}")
                return False
        except Exception as e:
            self.logger.log_error(f"Error deleting transaction: {str(e)}")
            return False
