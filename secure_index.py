import hmac
import hashlib
import secrets
import math
import glob
import random
from math import *
from bitarray import bitarray
from bloomfilter import BloomFilter
from encryption import Encryption

class SearchableEncryptionScheme():

    '''
    Constructor - sets the number of functions (r)
    '''
    def __init__(self):
        # number of functions
        self.r = 5

        # unique word count
        self.unique_word_count = 0

    def keygen(self, size):
        # Generates a master_key of size bytes
        master_key = secrets.token_bytes(size)

        # Create an empty list to hold the kpriv
        kpriv = []
        for i in range (0, self.r):
            # Generate r keys and stores it in kpriv
            hmac_digest = hmac.new(master_key, msg=secrets.token_bytes(size), digestmod=hashlib.sha1)
            # convert the digest from a bytes to hex
            hmac_digest = hmac_digest.hexdigest()
            kpriv.append(hmac_digest)

        return kpriv

    def trapdoor(self, kpriv, word):
        word = word.lower()
        # Creates an empty list to hold the trapdoors for word
        tw = []
        # Convert the word into a bytes object - Necessary to use HMAC
        w = bytes(word, 'utf-8')

        print(type(w))

        for i in range(0, self.r):
            # Converts kpriv[i] from hex to a bytes object - Necessary to use HMAC
            key = bytes.fromhex(kpriv[i])
            trapdoor_digest = hmac.new(key, msg=w, digestmod=hashlib.sha1)
            trapdoor_digest = trapdoor_digest.hexdigest()
            tw.append(trapdoor_digest)

        return tw

    def build_index(self, document_identifier, kpriv, list_of_words):
        # Create an empty list to hold the trapdoors for the word (x1, x2, ..., xr)
        trapdoor = []
        # Create an empty list to hold the codewords for the word (y1, y2, ..., yr)
        codewords = []

        for word in list_of_words:
            '''
            Create a trapdoor for each unique word
            '''
            # Takes the word and creates a trapdoor
            for i in range(0,self.r):
                # Converts kpriv[i] from hex to a bytes object - Necessary to use HMAC
                key = bytes.fromhex(kpriv[i])
                w = bytes(word, 'utf-8')
                trapdoor_digest = hmac.new(key, msg=w, digestmod=hashlib.sha1)
                trapdoor_digest = trapdoor_digest.hexdigest()
                trapdoor.append(trapdoor_digest)

        '''
        Error was here - my loop to create a codeword would take ONLY the first word and add it 5 times. 
        I changed it so that I now generate ALL trapdoors then I use another loop to generate codewords
        instead of word by word        
        '''

        # Take each word and hash it again with the document_identifier as the key to generate y1, y2, ..., yr
        for i in range(0, len(trapdoor)):
            # encode the docunemt identifier and the trapdoor[i]
            d_id = bytes(document_identifier, 'utf-8')
            message = bytes(trapdoor[i], 'utf-8')
            codeword_digest = hmac.new(message, msg=d_id, digestmod=hashlib.sha1)
            codeword_digest = codeword_digest.hexdigest()
            codewords.append(codeword_digest)

        '''
        Create a bloom filter and insert the codewords into the bloom filter
        '''
        # Creates a bloom filter and prints the stats
        bf = BloomFilter(len(codewords))

        # For each value in the list of codewords, add the codeword to the bloom filter
        for codeword in codewords:
            bf.add(codeword)

        # adding noise - take the total number of words - unique words * r and insert into bloom filter
        for i in range (0, (self.unique_word_count - len(list_of_words)) * self.r):
            # generate a random number from 0 - bf.size
            index = random.randrange(0, bf.size-1)
            bf.set_index(index)

        return(document_identifier, bf)

    def searchIndex(self, trapdoor, secure_index):

        # Create a documents set that will store the documents that return true from BF
        documents = set()

        for i in range(0, len(secure_index)):
            # Create a list to store the codewords for each document
            codewords = []
            d_id = bytes(secure_index[i][0], 'utf-8')

            # Take each word and hash it again with the document_identifier as the key to generate y1, y2, ..., yr
            for i in range(0, self.r):
                # encode the document identifier and the trapdoor[i]
                message = bytes(trapdoor[i], 'utf-8')
                codeword_digest = hmac.new(message, msg=d_id, digestmod=hashlib.sha1)
                codeword_digest = codeword_digest.hexdigest()
                codewords.append(codeword_digest)

            # Once you have the codewords for the specific document check it against ALL BF's
            for i in range (0, len(secure_index)):
                if secure_index[i][1].check(codewords):
                    documents.add(d_id)

        # Convert the type of the documents from bytes to string
        string_documents = []
        bytes_documents = list(documents)
        for i in range (0, len(documents)):
            string_documents.append(bytes_documents[i].decode("utf-8"))

        return string_documents

    '''
    Helper Functions
    '''
    def get_unique_words(self):
        all_unique_words = []
        document_number = 1
        files = glob.glob('recipes/**/*.txt', recursive=True)

        for file in files:
            document_identifier = 'document' + str(document_number)
            document_number += 1
            unique_word_count = 0
            unique_words_in_document = set()
            f = open(file, 'r')
            for line in f:
                for word in line.split():
                    word = word.lower()
                    if word not in unique_words_in_document:
                        unique_words_in_document.add(word)
                        unique_word_count += 1
            f.close()

            if unique_word_count > self.unique_word_count:
                self.unique_word_count = unique_word_count+25

            all_unique_words.append((document_identifier, unique_words_in_document, unique_word_count))

            # Create an encrypted file and store it in the encrypted files folder
            encrypt = Encryption(file, document_identifier)
            encrypt.encrypt()

        return all_unique_words