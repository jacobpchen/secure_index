import hmac
import hashlib
import secrets
import math
from math import *
from bitarray import bitarray
from bloomfilter import BloomFilter

class SearchableEncryptionScheme():

    '''
    Constructor - sets the number of functions (r)
    '''
    def __init__(self):
        # number of functions
        self.r = 5

    def keygen(self, size):
        # Generates a master_key of size bytes
        master_key = secrets.token_bytes(size)
        print(len(master_key))

        # Create an empty list to hold the kpriv
        kpriv = []
        for i in range (0, self.r):
            # Generate r keys and stores it in kpriv
            hmac_digest = hmac.new(master_key, msg=secrets.token_bytes(size), digestmod=hashlib.sha1)
            # print("The digest size is: " + str(hmac_digest.digest_size))
            print(hmac_digest.digest())

            '''
            Does it matter that it returns 40 bytes instead of 20?
            '''
            # convert the digest from a bytes to hex
            hmac_digest = hmac_digest.hexdigest()

            kpriv.append(hmac_digest)

        # hmac digest 20 bytes length
        print(kpriv)
        return kpriv

    def trapdoor(self, kpriv, word):
        # Creates an empty list to hold the trapdoors for word
        tw = []
        print(word)
        # Convert the word into a bytes object - Necessary to use HMAC
        w = bytes(word, 'utf-8')

        print(type(w))

        for i in range(0, self.r):
            # Converts kpriv[i] from hex to a bytes object - Necessary to use HMAC
            key = bytes.fromhex(kpriv[i])

            trapdoor_digest = hmac.new(key, msg=w, digestmod=hashlib.sha1)
            trapdoor_digest = trapdoor_digest.hexdigest()
            print(trapdoor_digest)
            tw.append(trapdoor_digest)

        return tw

    def build_index(self, document_identifier, kpriv, list_of_words):
        print(list_of_words)
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
            Take the trapdoor and create a codeword for each word in list_of_words
            '''

            # Take each word and hash it again with the dociment_identifier as the key to generate y1, y2, ..., yr
            for i in range(0, self.r):
                # encode the docunemt identifier and the trapdoor[i]
                d_id = bytes(document_identifier, 'utf-8')
                message = bytes(trapdoor[i], 'utf-8')

                codeword_digest = hmac.new(d_id, msg=message, digestmod=hashlib.sha1)
                codeword_digest = codeword_digest.hexdigest()
                codewords.append(codeword_digest)

        '''
        Create a bloom filter and insert the codewords into the bloom filter
        '''
        # Creates a bloom filter and prints the stats
        bf = BloomFilter(len(codewords))
        print("Size of bit array: {}".format(bf.size))
        print("Size of numbers of items in the bloom filter (n)", len(codewords))
        print("False positive probability: {:.6%}".format(bf.fp_prob))
        print("Number of hash functions:{}".format(bf.hash_count))

        # For each hash value in the list of codewords, add the codeword to the bloom filter
        for codeword in codewords:
            bf.add(codeword)

        # Test the bloom filter - Check if trapdoor returns true
        count = 0
        for word in trapdoor:
            if bf.check(word):
                count += 1
                print("False Positive")
            else:
                print("Not Found")
        print(count)

        # Test the bloom filter - Check if each codeword returns true
        count = 0
        for word in codewords:
            if bf.check(word):
                print("Found!")
            else:
                print("Error")
                count += 1
        print("Errors found" + str(count))





        print("This is the list of trapdoors: " + str(trapdoor))
        print(len(trapdoor))
        print("This is the list of codewords: " + str(codewords))
        print(len(codewords))









