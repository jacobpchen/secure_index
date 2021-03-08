import os.path
from cryptography.fernet import Fernet
from ftplib import FTP

class Decryption():
    def __init__(self, list_of_docs):
        self.list_of_docs = list_of_docs

        # check if key exists
        self.doesKeyExist = True

        # login credentials
        self.ftp = FTP("192.168.68.200")
        self.ftp.login(user="Jacob", passwd="asdfasdf")

    def load_key(self):
        return open("key.key", "rb").read()

    def decryption(self):
        key = self.load_key()
        f = Fernet(key)
        count = 0

        try:
            for document in range(0, len(self.list_of_docs)):
                # Download the file from FTP server to a local folder decrypted files
                self.ftp.cwd('/Encrypted Files/')
                filename = self.list_of_docs[document] + '.txt'
                path = '.\Decrypted Files\\'
                with open(path+self.list_of_docs[document] + '.txt', 'wb') as file:
                    self.ftp.retrbinary("RETR " + filename, file.write)

                # Decrypt the file
                path = '.\Decrypted Files\\'
                with open(path+filename, 'rb') as file:
                    # Read the encrypted data
                    encrypted_data = file.read()
                    file.close()

                decrypted_data = f.decrypt(encrypted_data)
                # Overwrite the encrypted file with the decrypted one
                path = '.\Decrypted Files\\'
                with open(path + self.list_of_docs[document] + '.txt', 'wb') as file:
                    # Creates a local decrypted file
                    file.write(decrypted_data)
                    file.close()
                    count += 1

            return 'Sucessfully decrypted',  count, 'files'
        except:
            print("Error when trying to decrypt")
