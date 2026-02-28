class User:
    """represent a system user.
    user can be:
    -admin
    -librarian
    -student
    """
    def __init__(self, username, password, role):
        self.username = username
        self.password = password #hashed- not stored in plane text
        self.role = role # role determines system permissions
    
    def to_dict(self):
        """convert user objects to a dictionary for easy storage in JSON"""
        return self.__dict__