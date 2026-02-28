from services.auth_service import register, login
from services.book_service import add_book, list_books, delete_book, search_book
from services.borrow_service import borrow_book as br_borrow_book, return_book as br_return_book

def main():
    """
    main CLI entry point
    control user navigation
    """
    while True:
        print("\nLibrary Management System")
        print("1. Register")
        print("2. Login")
        print("3. Add Book")
        print("4. List Books")
        print("5. Delete Book")
        print("6. Search Book")
        print("7. Borrow Book")
        print("8. Return Book")
        print("9. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role: (admin/librarian/student) ")
            register(username, password, role)
            print("User registered successfully.")
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = login(username, password)
            if user:
                print(f"Welcome, {user['username']} ({user['role']})")
            else:
                print("Invalid username or password.")
        elif choice == "3":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            copies = input("Enter number of copies: ")
            add_book(title, author, isbn, int(copies))
            print("Book added successfully.")
        elif choice == "4":
            books = list_books()
            if books:
                print("\n--- Book List ---")
                for book in books:
                    print(f"Title: {book.get('title', 'N/A')}, Author: {book.get('author', 'N/A')}, ISBN: {book.get('isbn', 'N/A')}, Available: {book.get('available_copies', 0)}")
            else:
                print("No books found.")
        elif choice == "5":
            isbn = input("Enter ISBN to delete: ")
            delete_book(isbn)
        elif choice == "6":
            title = input("Enter book title to search: ")
            books = search_book(title)
            if books:
                for book in books:
                    print(f"Found: {book.get('title', 'N/A')} by {book.get('author', 'N/A')}")
            else:
                print("Book not found.")
        elif choice == "7":
            isbn = input("Enter ISBN to borrow: ")
            username = input("Enter your username: ")
            result = br_borrow_book(username, isbn)
            print(result)
        elif choice == "8":
            isbn = input("Enter ISBN to return: ")
            username = input("Enter your username: ")
            result = br_return_book(username, isbn)
            print(result)
        elif choice == "9":
            print("Exiting system... Thank you for using the library system.")
            break
        else:
            print("Invalid choice. Please try again.")


#ensures program runs only if executed directly 

if __name__ == "__main__":
    main()

