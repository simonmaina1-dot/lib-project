import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib
from utils.file_handler import load_data, save_data
from models.user import User

USER_FILE = "data/users.json"

def hash_password(password):
    """hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password, role):
    """
    Registers a new user and saves to JSON file.
    """
    users = load_data(USER_FILE)

    # Hash password before saving
    hashed_password = hash_password(password)

    # Create User object
    user = User(username, hashed_password, role)

    # Add user to list
    users.append(user.to_dict())

    # Save updated list
    save_data(USER_FILE, users)


def login(username, password):
    """
    Authenticates a user.
    Returns user dictionary if successful.
    """
    users = load_data(USER_FILE)
    hashed_password = hash_password(password)

    for user in users:
        # Compare username and hashed password
        if user["username"] == username and user["password"] == hashed_password:
            return user

    return None