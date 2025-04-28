class Category:
    def __init__(self, id, name, user_id=None):
        self.id = id
        self.name = name
        self.user_id = user_id  # None for default categories
