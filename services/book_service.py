import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.file_handler import load_data, save_data
from models.book import Book

BOOK_FILE = "data/books.json"

def add_book(title, author, isbn, copies):
    """add a book to the library system."""
    books = load_data(BOOK_FILE)
    # Ensure we have a list
    if not isinstance(books, list):
        books = []
    book = Book(title, author, isbn, copies)
    books.append(book.to_dict())
    save_data(BOOK_FILE, books)

def list_books():
    """
    return all books in the library system.
    """
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return []
    return books

def delete_book(isbn):
    """
    delete a book from the library system.
    """
    books = load_data(BOOK_FILE)
    # Ensure we have a list
    if not isinstance(books, list):
        books = []
    #to remove matching isbn from the list
    books = [book for book in books if book.get("isbn") != isbn]
    save_data(BOOK_FILE, books)
    print(f"Book {isbn} deleted successfully.")

def search_book(title):
    """
    search for a book by title (case-insensitive partial match).
    """
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return []
    title_lower = title.lower()
    return [book for book in books if title_lower in book.get("title", "").lower()]

def borrow_book(isbn, user_id):
    """
    borrow a book from the library system.
    """
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return "No books available."
    
    for book in books:
        if book.get("isbn") == isbn and book.get("available_copies", 0) > 0:
            book["available_copies"] -= 1
            save_data(BOOK_FILE, books)
            return "Book borrowed successfully."
    
    return "Book not available."

