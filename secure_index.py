import hmac
import hashlib
import secrets
import math
import glob
import random
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

        # highest word count
        self.highest_word_count = 0

    def keygen(self, size):
        # Generates a master_key of size bytes
        master_key = secrets.token_bytes(size)
        # print(len(master_key))

        # Create an empty list to hold the kpriv
        kpriv = []
        for i in range (0, self.r):
            # Generate r keys and stores it in kpriv
            hmac_digest = hmac.new(master_key, msg=secrets.token_bytes(size), digestmod=hashlib.sha1)
            #print("The digest size is: " + str(hmac_digest.digest_size))
            #print(hmac_digest.digest())

            # convert the digest from a bytes to hex
            hmac_digest = hmac_digest.hexdigest()

            kpriv.append(hmac_digest)

        # print(kpriv)
        return kpriv

    def trapdoor(self, kpriv, word):
        # Creates an empty list to hold the trapdoors for word
        tw = []
        # print(word)
        # Convert the word into a bytes object - Necessary to use HMAC
        w = bytes(word, 'utf-8')

        print(type(w))

        for i in range(0, self.r):
            # Converts kpriv[i] from hex to a bytes object - Necessary to use HMAC
            key = bytes.fromhex(kpriv[i])

            trapdoor_digest = hmac.new(key, msg=w, digestmod=hashlib.sha1)
            trapdoor_digest = trapdoor_digest.hexdigest()
            # print("This is the trapdoor digest" , trapdoor_digest)
            tw.append(trapdoor_digest)

        print("These are the trapdoors: " , tw)
        return tw

    def build_index(self, document_identifier, kpriv, list_of_words, highest_word_count):
        print(list_of_words)
        # Create an empty list to hold the trapdoors for the word (x1, x2, ..., xr)
        trapdoor = []
        # Create an empty list to hold the codewords for the word (y1, y2, ..., yr)
        codewords = []

        for word in list_of_words:
            '''
            Create a trapdoor for each unique word
            '''
            # print("Creating trapdoor for: " + str(word))

            # Takes the word and creates a trapdoor
            for i in range(0,self.r):
                # Converts kpriv[i] from hex to a bytes object - Necessary to use HMAC
                key = bytes.fromhex(kpriv[i])

                w = bytes(word, 'utf-8')
                trapdoor_digest = hmac.new(key, msg=w, digestmod=hashlib.sha1)
                trapdoor_digest = trapdoor_digest.hexdigest()
                trapdoor.append(trapdoor_digest)

        print(trapdoor)

        '''
        Take the trapdoor and create a codeword for each word in list_of_words
        '''


        '''
        Error was here - my loop to create a codeword would take ONLY the first word and add it 5 times. 
        I changed it so that I now generate ALL trapdoors then I use another loop to generate codewords
        instead of word by word        
        '''

        # Take each word and hash it again with the document_identifier as the key to generate y1, y2, ..., yr
        for i in range(0, len(trapdoor)):
            # encode the docunemt identifier and the trapdoor[i]
            d_id = bytes(document_identifier, 'utf-8')
            # print(type(d_id))
            message = bytes(trapdoor[i], 'utf-8')
            # print("This is trapdoor",i,  trapdoor[i])
            # print("This is the message", message)

            codeword_digest = hmac.new(message, msg=d_id, digestmod=hashlib.sha1)
            codeword_digest = codeword_digest.hexdigest()
            # print("This is the codeword digest", codeword_digest)
            codewords.append(codeword_digest)
            # print("This is the len of codewords: ", len(codewords))

        print("These are the trapdoors: " + str(trapdoor))
        print("These are the codewords: " + str(codewords))

        '''
        Create a bloom filter and insert the codewords into the bloom filter
        '''
        # Creates a bloom filter and prints the stats
        bf = BloomFilter(len(codewords) + 5)
        print("Size of bit array: {}".format(bf.size))
        print("Size of numbers of items in the bloom filter (n)", len(codewords))

        # For each hash value in the list of codewords, add the codeword to the bloom filter
        for codeword in codewords:
            # print("Adding the codeword: " + str(codeword), "to the BF")
            bf.add(codeword)

        print("This is the list of true bits BEFORE", bf.true_bits)
        print("This is the size of true bits BEFORE", int(len(bf.true_bits)))

        # adding noise - take the total number of words - unique words * r and insert into bloom filter
        print("The highest word count is: ", self.highest_word_count)
        print(len(list_of_words))
        print((self.highest_word_count - len(list_of_words)) * self.r)
        for i in range (0, (self.highest_word_count - len(list_of_words)) * self.r):
            # generate a random number from 0 - bf.size
            index = random.randrange(0, bf.size-1)
            bf.set_index(index)
            bf.true_bits.append(index)

        print("This is the list of true bits AFTER", bf.true_bits)
        print("This is the size of true bits AFTER", int(len(bf.true_bits)))

        return(document_identifier, bf)

    def searchIndex(self, trapdoor, secure_index):
        print(trapdoor)
        print(type(trapdoor))
        print(secure_index)
        print(len(secure_index))
        print("The type for secure index is:" , type(secure_index[0][1]))

        # Create a list to store the codewords
        codewords = []

        '''
        Take the trapdoor and create a codeword for each word in list_of_words
        '''

        # Take each word and hash it again with the document_identifier as the key to generate y1, y2, ..., yr
        for i in range(0, self.r):
            # encode the document identifier and the trapdoor[i]
            print("This is secure index sub 0", secure_index[0][0])
            print("This is secure index[0][1]", secure_index[0][1])

            d_id = bytes(secure_index[0][0], 'utf-8')
            # print(type(d_id))
            # print("This is the trapdoor[i]", trapdoor[i])
            print("Trapdoor[i] is:", trapdoor[i])
            message = bytes(trapdoor[i], 'utf-8')
            print("This is trapdoor[i]", trapdoor[i])
            print("This is the message", message)

            codeword_digest = hmac.new(message, msg=d_id, digestmod=hashlib.sha1)
            codeword_digest = codeword_digest.hexdigest()
            print("This is the codeword_digest", codeword_digest)
            codewords.append(codeword_digest)

        print("These are the codewords: " + str(codewords))

        count = 0
        for i in range(0, len(secure_index)):
            print(i)
            print(type(i))
            print(secure_index[i][1])
            if secure_index[i][1].check(codewords):
                return True, d_id
        return False

    '''
    Helper Functions
    '''
    def get_unique_words(self):
        print("Using glob.glob()")
        all_unique_words = []
        document_number = 1
        files = glob.glob('recipes/**/*.txt', recursive=True)

        for file in files:
            document_identifier = 'document' + str(document_number)
            document_number += 1
            total_word_count = 0
            unique_words_in_document = set()
            print(file)
            f = open(file, 'r')
            for line in f:
                for word in line.split():
                    if word not in unique_words_in_document:
                        unique_words_in_document.add(word)
                        total_word_count += 1
                    else:
                        total_word_count += 1
            f.close()

            if total_word_count > self.highest_word_count:
                self.highest_word_count = total_word_count

            print("The total word count for: ", document_identifier,  str(total_word_count))
            print("The unique words for: ", document_identifier, str(len(unique_words_in_document)))

            all_unique_words.append((document_identifier, unique_words_in_document, total_word_count))

        print(self.highest_word_count)
        return all_unique_words






