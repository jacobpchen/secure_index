import os.path
from cryptography.fernet import Fernet

class Encryption():
    def __init__(self, filename, document_identifier):
        self.filename = filename
        self.document_identifier = document_identifier

        # check if key exists
        self.doesKeyExist = True

    def write_key(self):
        """
        Generates a key and save it into a file
        """
        if self.doesKeyExist == False:
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)
            self.doesKeyExist = True

    def load_key(self):
        """
            Loads the key from the current directory named `key.key`
            """
        return open("key.key", "rb").read()

    def encrypt(self):

        key = self.load_key()
        print(key)
        f = Fernet(key)
        with open(self.filename, 'rb') as file:
            plaintext_data = file.read()
            encrypted_data = f.encrypt(plaintext_data)
            file.close()

            path = 'C:\Projects\secure index\Encrypted Files'
            file_name = self.filename
            print(file_name)
            complete_path_name = os.path.join(path, file_name)

        # Creates encrypted documents
        path = '.\Encrypted Files\\'
        with open(path + self.document_identifier + '.txt', 'wb') as file:
            file.write(encrypted_data)
            file.close()

