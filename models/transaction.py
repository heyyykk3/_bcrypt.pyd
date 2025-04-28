from datetime import datetime

class Transaction:
    def __init__(self, id, user_id, description, amount, category, date=None):
        self.id = id
        self.user_id = user_id
        self.description = description
        self.amount = amount  # Positive for income, negative for expense
        self.category = category
        self.date = date if date else datetime.now()
