"""
Book Service for the Library Management System.

This module handles all book-related operations including:
- Adding, deleting, and updating books
- Listing and searching books
- Borrowing and returning books
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Optional
from datetime import datetime
from utils.file_handler import load_data, save_data
from models.book import Book
from utils.validators import validate_book_data, validate_isbn

# File path
BOOK_FILE = "data/books.json"


def add_book(title: str, author: str, isbn: str, copies: int) -> Dict:
    """
    Add a book to the library system.
    
    Args:
        title: Book title
        author: Book author
        isbn: ISBN (10 or 13 digits)
        copies: Number of copies
        
    Returns:
        Dictionary with success status and message
    """
    # Validate book data
    valid, msg = validate_book_data(title, author, isbn, copies)
    if not valid:
        return {'success': False, 'message': msg}
    
    # Load existing books
    books = load_data(BOOK_FILE)
    
    # Check if ISBN already exists
    for book in books:
        if book.get('isbn') == isbn:
            return {'success': False, 'message': 'Book with this ISBN already exists'}
    
    # Create Book object
    book = Book.create_book(title, author, isbn, copies)
    
    # Add book to list
    books.append(book.to_dict())
    
    # Save to file
    save_data(BOOK_FILE, books)
    
    return {'success': True, 'message': 'Book added successfully'}


def list_books() -> List[Dict]:
    """
    Return all books in the library system.
    
    Returns:
        List of book dictionaries
    """
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return []
    return books


def get_book_by_isbn(isbn: str) -> Optional[Dict]:
    """
    Get a book by ISBN.
    
    Args:
        isbn: ISBN to search for
        
    Returns:
        Book dictionary if found, None otherwise
    """
    books = load_data(BOOK_FILE)
    
    for book in books:
        if book.get('isbn') == isbn:
            return book
    
    return None


def delete_book(isbn: str) -> Dict:
    """
    Delete a book from the library system.
    
    Args:
        isbn: ISBN of the book to delete
        
    Returns:
        Dictionary with success status and message
    """
    books = load_data(BOOK_FILE)
    initial_count = len(books)
    
    # Remove book with matching ISBN
    books = [book for book in books if book.get('isbn') != isbn]
    
    if len(books) < initial_count:
        save_data(BOOK_FILE, books)
        return {'success': True, 'message': f'Book {isbn} deleted successfully'}
    
    return {'success': False, 'message': 'Book not found'}


def search_book(query: str) -> List[Dict]:
    """
    Search for books by title (case-insensitive partial match).
    
    Args:
        query: Search query
        
    Returns:
        List of matching book dictionaries
    """
    books = load_data(BOOK_FILE)
    if not isinstance(books, list):
        return []
    
    query_lower = query.lower()
    return [book for book in books if query_lower in book.get('title', '').lower()]


def update_book(isbn: str, updates: Dict) -> Dict:
    """
    Update book information.
    
    Args:
        isbn: ISBN of the book to update
        updates: Dictionary with fields to update
        
    Returns:
        Dictionary with success status and message
    """
    books = load_data(BOOK_FILE)
    
    for book in books:
        if book.get('isbn') == isbn:
            # Update allowed fields
            if 'title' in updates and updates['title']:
                book['title'] = updates['title']
            if 'author' in updates and updates['author']:
                book['author'] = updates['author']
            if 'total_copies' in updates:
                book['total_copies'] = updates['total_copies']
                # Adjust available_copies if needed
                if 'available_copies' not in updates:
                    borrowed = book.get('borrowed_copies', 0)
                    book['available_copies'] = max(0, updates['total_copies'] - borrowed)
            if 'available_copies' in updates:
                book['available_copies'] = updates['available_copies']
            
            save_data(BOOK_FILE, books)
            return {'success': True, 'message': 'Book updated successfully'}
    
    return {'success': False, 'message': 'Book not found'}


def borrow_book(username: str, isbn: str) -> Dict:
    """
    Borrow a book from the library system.
    
    Args:
        username: Username of the borrower
        isbn: ISBN of the book
        
    Returns:
        Dictionary with success status and message
    """
    books = load_data(BOOK_FILE)
    
    for book in books:
        if book.get('isbn') == isbn:
            available = book.get('available_copies', 0)
            
            if available > 0:
                # Update book
                book['available_copies'] = available - 1
                book['borrowed_copies'] = book.get('borrowed_copies', 0) + 1
                
                # Add to borrowed_by list
                borrowed_by = book.get('borrowed_by', [])
                from datetime import timedelta
                due_date = datetime.now() + timedelta(days=14)
                borrowed_by.append({
                    'user': username,
                    'borrow_date': datetime.now().isoformat(),
                    'due_date': due_date.isoformat()
                })
                book['borrowed_by'] = borrowed_by
                
                # Update availability status
                if book['available_copies'] == 0:
                    book['is_available'] = False
                    book['is_borrowed'] = True
                
                save_data(BOOK_FILE, books)
                return {'success': True, 'message': 'Book borrowed successfully'}
            else:
                return {'success': False, 'message': 'Book not available'}
    
    return {'success': False, 'message': 'Book not found'}


def return_book(username: str, isbn: str) -> Dict:
    """
    Return a borrowed book.
    
    Args:
        username: Username of the borrower
        isbn: ISBN of the book
        
    Returns:
        Dictionary with success status and message
    """
    books = load_data(BOOK_FILE)
    
    for book in books:
        if book.get('isbn') == isbn:
            borrowed_by = book.get('borrowed_by', [])
            
            # Find and remove user from borrowed_by
            found = False
            for record in borrowed_by:
                if record.get('user') == username:
                    borrowed_by.remove(record)
                    found = True
                    break
            
            if found:
                book['borrowed_by'] = borrowed_by
                book['available_copies'] = book.get('available_copies', 0) + 1
                book['borrowed_copies'] = max(0, book.get('borrowed_copies', 1) - 1)
                
                # Update availability status
                if book['borrowed_copies'] == 0:
                    book['is_available'] = True
                    book['is_borrowed'] = False
                
                save_data(BOOK_FILE, books)
                return {'success': True, 'message': 'Book returned successfully'}
            else:
                return {'success': False, 'message': 'User did not borrow this book'}
    
    return {'success': False, 'message': 'Book not found'}


def get_borrowed_books(username: str) -> List[Dict]:
    """
    Get all books borrowed by a user.
    
    Args:
        username: Username
        
    Returns:
        List of borrowed book dictionaries
    """
    books = load_data(BOOK_FILE)
    borrowed = []
    
    for book in books:
        borrowed_by = book.get('borrowed_by', [])
        for record in borrowed_by:
            if record.get('user') == username:
                borrowed.append(book)
                break
    
    return borrowed


def get_overdue_books() -> List[Dict]:
    """
    Get all overdue books.
    
    Returns:
        List of overdue book dictionaries
    """
    books = load_data(BOOK_FILE)
    overdue = []
    now = datetime.now()
    
    for book in books:
        borrowed_by = book.get('borrowed_by', [])
        for record in borrowed_by:
            due_date_str = record.get('due_date')
            if due_date_str:
                due_date = datetime.fromisoformat(due_date_str)
                if now > due_date:
                    overdue.append(book)
                    break
    
    return overdue

