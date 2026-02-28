#!/usr/bin/env python3
"""
Library Management System - CLI Entry Point

A fully functional Python CLI application for managing a library system.
Features:
- User authentication with role-based access
- Book management (add, delete, list, search)
- Borrow/return functionality
- Persistent JSON storage
"""

import sys
import os
import argparse
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import register, login, get_user_by_username
from services.book_service import (
    add_book, list_books, delete_book, search_book,
    borrow_book as br_borrow_book, return_book as br_return_book
)


# Try to import rich for better CLI output
try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


# Global state
current_user: Optional[dict] = None


def print_success(message: str):
    """Print success message."""
    if RICH_AVAILABLE:
        rprint(f"[green]✓[/green] {message}")
    else:
        print(f"✓ {message}")


def print_error(message: str):
    """Print error message."""
    if RICH_AVAILABLE:
        rprint(f"[red]✗[/red] {message}")
    else:
        print(f"✗ {message}")


def print_info(message: str):
    """Print info message."""
    if RICH_AVAILABLE:
        rprint(f"[blue]ℹ[/blue] {message}")
    else:
        print(f"ℹ {message}")


def display_books(books: list, title: str = "Book List"):
    """Display books in a formatted table."""
    if not books:
        print_info("No books found.")
        return
    
    if RICH_AVAILABLE:
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Title", style="cyan")
        table.add_column("Author", style="green")
        table.add_column("ISBN", style="yellow")
        table.add_column("Available", justify="center")
        table.add_column("Total", justify="center")
        
        for book in books:
            table.add_row(
                book.get('title', 'N/A'),
                book.get('author', 'N/A'),
                book.get('isbn', 'N/A'),
                str(book.get('available_copies', 0)),
                str(book.get('total_copies', 0))
            )
        
        console.print(table)
    else:
        print(f"\n--- {title} ---")
        for book in books:
            print(f"Title: {book.get('title', 'N/A')}, "
                  f"Author: {book.get('author', 'N/A')}, "
                  f"ISBN: {book.get('isbn', 'N/A')}, "
                  f"Available: {book.get('available_copies', 0)}")


def handle_register(args):
    """Handle user registration."""
    result = register(args.username, args.password, args.role)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_login(args):
    """Handle user login."""
    global current_user
    user = login(args.username, args.password)
    if user:
        current_user = user
        print_success(f"Welcome, {user['username']} ({user['role']})")
    else:
        print_error("Invalid username or password.")


def handle_add_book(args):
    """Handle adding a book."""
    result = add_book(args.title, args.author, args.isbn, args.copies)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_list_books(args):
    """Handle listing books."""
    books = list_books()
    display_books(books, "All Books in Library")


def handle_delete_book(args):
    """Handle deleting a book."""
    result = delete_book(args.isbn)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_search_book(args):
    """Handle searching for a book."""
    books = search_book(args.query)
    if books:
        display_books(books, f"Search Results for '{args.query}'")
    else:
        print_info(f"No books found matching '{args.query}'")


def handle_borrow_book(args):
    """Handle borrowing a book."""
    result = br_borrow_book(args.username, args.isbn)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_return_book(args):
    """Handle returning a book."""
    result = br_return_book(args.username, args.isbn)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def interactive_mode():
    """Run the CLI in interactive menu mode."""
    global current_user
    
    while True:
        print("\n" + "="*50)
        print("Library Management System")
        print("="*50)
        
        if current_user:
            print(f"Logged in as: {current_user['username']} ({current_user['role']})")
        else:
            print("Not logged in")
        
        print("-"*50)
        print("1. Register")
        print("2. Login")
        print("3. Add Book")
        print("4. List Books")
        print("5. Delete Book")
        print("6. Search Book")
        print("7. Borrow Book")
        print("8. Return Book")
        print("9. Logout")
        print("10. Exit")
        print("-"*50)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            role = input("Enter role (admin/librarian/student): ").strip().lower()
            handle_register(argparse.Namespace(username=username, password=password, role=role))
        
        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            handle_login(argparse.Namespace(username=username, password=password))
        
        elif choice == "3":
            if not current_user:
                print_error("Please login first.")
                continue
            title = input("Enter book title: ").strip()
            author = input("Enter author: ").strip()
            isbn = input("Enter ISBN: ").strip()
            copies = input("Enter number of copies: ").strip()
            try:
                copies = int(copies)
                handle_add_book(argparse.Namespace(title=title, author=author, isbn=isbn, copies=copies))
            except ValueError:
                print_error("Invalid number of copies.")
        
        elif choice == "4":
            handle_list_books(argparse.Namespace())
        
        elif choice == "5":
            if not current_user:
                print_error("Please login first.")
                continue
            isbn = input("Enter ISBN to delete: ").strip()
            handle_delete_book(argparse.Namespace(isbn=isbn))
        
        elif choice == "6":
            query = input("Enter book title to search: ").strip()
            handle_search_book(argparse.Namespace(query=query))
        
        elif choice == "7":
            if not current_user:
                print_error("Please login first.")
                continue
            isbn = input("Enter ISBN to borrow: ").strip()
            username = current_user['username']
            handle_borrow_book(argparse.Namespace(username=username, isbn=isbn))
        
        elif choice == "8":
            if not current_user:
                print_error("Please login first.")
                continue
            isbn = input("Enter ISBN to return: ").strip()
            username = current_user['username']
            handle_return_book(argparse.Namespace(username=username, isbn=isbn))
        
        elif choice == "9":
            current_user = None
            print_success("Logged out successfully.")
        
        elif choice == "10":
            print_info("Exiting system... Thank you for using the library system.")
            break
        
        else:
            print_error("Invalid choice. Please try again.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Library Management System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s register --username john --password secret123 --role student
  %(prog)s login --username john --password secret123
  %(prog)s add-book --title "Python Basics" --author "John Doe" --isbn 1234567890 --copies 5
  %(prog)s list-books
  %(prog)s search-book --query "Python"
  %(prog)s delete-book --isbn 1234567890
  %(prog)s borrow-book --username john --isbn 1234567890
  %(prog)s return-book --username john --isbn 1234567890
        """
    )
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Register command
    register_parser = subparsers.add_parser('register', help='Register a new user')
    register_parser.add_argument('--username', required=True, help='Username')
    register_parser.add_argument('--password', required=True, help='Password')
    register_parser.add_argument('--role', required=True, choices=['admin', 'librarian', 'student'], help='User role')
    
    # Login command
    login_parser = subparsers.add_parser('login', help='Login to the system')
    login_parser.add_argument('--username', required=True, help='Username')
    login_parser.add_argument('--password', required=True, help='Password')
    
    # Add book command
    add_parser = subparsers.add_parser('add-book', help='Add a new book')
    add_parser.add_argument('--title', required=True, help='Book title')
    add_parser.add_argument('--author', required=True, help='Book author')
    add_parser.add_argument('--isbn', required=True, help='Book ISBN')
    add_parser.add_argument('--copies', type=int, required=True, help='Number of copies')
    
    # List books command
    list_parser = subparsers.add_parser('list-books', help='List all books')
    
    # Delete book command
    delete_parser = subparsers.add_parser('delete-book', help='Delete a book')
    delete_parser.add_argument('--isbn', required=True, help='Book ISBN')
    
    # Search book command
    search_parser = subparsers.add_parser('search-book', help='Search for a book')
    search_parser.add_argument('--query', required=True, help='Search query')
    
    # Borrow book command
    borrow_parser = subparsers.add_parser('borrow-book', help='Borrow a book')
    borrow_parser.add_argument('--username', required=True, help='Username')
    borrow_parser.add_argument('--isbn', required=True, help='Book ISBN')
    
    # Return book command
    return_parser = subparsers.add_parser('return-book', help='Return a book')
    return_parser.add_argument('--username', required=True, help='Username')
    return_parser.add_argument('--isbn', required=True, help='Book ISBN')
    
    args = parser.parse_args()
    
    # If no command, run interactive mode
    if not args.command:
        interactive_mode()
        return
    
    # Handle commands
    if args.command == 'register':
        handle_register(args)
    elif args.command == 'login':
        handle_login(args)
    elif args.command == 'add-book':
        handle_add_book(args)
    elif args.command == 'list-books':
        handle_list_books(args)
    elif args.command == 'delete-book':
        handle_delete_book(args)
    elif args.command == 'search-book':
        handle_search_book(args)
    elif args.command == 'borrow-book':
        handle_borrow_book(args)
    elif args.command == 'return-book':
        handle_return_book(args)


if __name__ == "__main__":
    main()

