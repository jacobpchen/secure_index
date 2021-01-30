import os.path
from cryptography.fernet import Fernet

class Decryption():
    def __init__(self, list_of_docs):
        self.list_of_docs = list_of_docs

        # check if key exists
        self.doesKeyExist = True

    def load_key(self):
        return open("key.key", "rb").read()

    def decryption(self):
        key = self.load_key()
        f = Fernet(key)

        for document in range(0, len(self.list_of_docs)):
            print(self.list_of_docs[document])

            path = '.\Encrypted Files\\'
            with open(path+self.list_of_docs[document] + '.txt', 'rb') as file:
                # Read the encrypted data
                encrypted_data = file.read()

            decrypted_data = f.decrypt(encrypted_data)
            # Create a folder to store decrypted documents
            path = '.\Decrypted Files\\'
            with open(path+self.list_of_docs[document] + '.txt', 'wb') as file:
                file.write(decrypted_data)



