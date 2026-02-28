from datetime import datetime, timedelta

class BorrowRecord:
    """records a book borrowing activity."""
    def __init__(self, book_title, user_name, borrow_date, return_date, isbn):
        self.user_name = user_name
        self.book_title = book_title
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.isbn = isbn

    def to_dict(self):
        """convert borrow record to a dictionary for easy storage in JSON"""
        return self.__dict__
        
    def is_overdue(self):
        """check if the book is overdue."""
        return datetime.now() > self.return_date
    def extend_return_date(self, days=7):
        """extend the return date by a given number of days."""
        if self.return_date:
            self.return_date = self.return_date + timedelta(days=days)
