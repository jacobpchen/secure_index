import shutil
from cryptography.fernet import Fernet

class Encryption():
    def __init__(self, filename, key, document_identifier):
        self.filename = filename
        self.key = key
        self.document_identifier = document_identifier

        # check if key exists
        self.doesKeyExist = False

    def write_key(self):
        """
        Generates a key and save it into a file
        """
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

    def encrypt(self, filename, key):
        f = Fernet(self.key)
        with open(filename, 'rb') as file:
            encrypted_data = file.read()

        with open('document_identifier', 'wb') as file:
            file.write(encrypted_data)