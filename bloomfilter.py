import math
import random
from math import *
import hashlib
from bitarray import bitarray

class BloomFilter(object):
    '''
    Class for Bloom filter, using SHA1 hash function
    '''

    def __init__(self, items_count):
        # Size of bit array to use 2^16
        self.size = 65536

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

        # Test var
        self.true_bits = []

    def add(self, item):
        #Add an item in the filter
        digest = item
        # seperate the digest into 2 bytes
        n = 4
        digests = [digest[i:i + n] for i in range(0, len(digest), n)]
        # print(digests)
        last_two_bytes_digest = digests[len(digests)-1]
        #print(last_two_bytes_digest)
        # Convert to the 10 hexadecimal digit to an integer between 0 - m
        bit = int(last_two_bytes_digest, 16)
        self.bit_array[bit] = True

        self.true_bits.append(bit)

    def check(self, item):
        for index in range(0, len(item)):
            digest = item[index]
            print(digest)

            n = 4
            digests = [digest[i:i + n] for i in range(0, len(digest), n)]
            last_two_bytes_digest = digests[len(digests) - 1]
            # print(last_two_bytes_digest)
            bit = int(last_two_bytes_digest, 16)
            if self.bit_array[bit] == False:
                return False

            return True

    def set_index(self, index):
        while (1):
            # print("Setting: ", index, "true")
            if self.bit_array[index] == False:
                self.bit_array[index] = True
                break
            else:
                index = random.randrange(0, self.size)











