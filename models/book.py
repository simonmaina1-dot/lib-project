from datetime import datetime, timedelta

class Book:
    """represents a book in the library."""
    def __init__(self, title, author, isbn, total_copies):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.borrowed_copies = 0
        self.borrowed_by = []
        self.due_date = None
        self.is_available = True
        self.is_borrowed = False
        self.is_overdue = False
        self.is_reserved = False
        self.is_renewed = False
        self.is_lost = False
        self.is_damaged = False
        
    def to_dict(self):
        """convert book object to a dictionary for easy storage in JSON"""
        return self.__dict__
    def borrow(self, user):
        """borrow a book from the library."""
        if self.is_available and self.available_copies > 0:
            self.is_available = False
            self.is_borrowed = True
            self.available_copies -= 1
            self.borrowed_copies += 1
            self.borrowed_by.append(user)
            self.due_date = datetime.now() + timedelta(days=14)
            return True
        return False
