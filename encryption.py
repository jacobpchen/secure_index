from os import path
from cryptography.fernet import Fernet

class Encryption():
    def __init__(self, filename, document_identifier):
        self.filename = filename
        self.document_identifier = document_identifier
        self.write_key()

    def write_key(self):
        """
        Generates a key and save it into a file
        """
        # Checks if there is a key file in the current directory, creates one if not found
        if path.isfile('key.key') == False:
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)
                print(key)

    def load_key(self):
        """
        Loads the key from the current directory named `key.key`
        """
        return open("key.key", "rb").read()

    def encrypt(self):
        key = self.load_key()
        f = Fernet(key)
        with open(self.filename, 'rb') as file:
            plaintext_data = file.read()
            encrypted_data = f.encrypt(plaintext_data)
            file.close()

        # Creates encrypted documents
        path = '.\Encrypted Files\\'
        with open(path + self.document_identifier + '.txt', 'wb') as file:
            file.write(encrypted_data)
            file.close()