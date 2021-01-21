import hmac
import hashlib
import secrets
import math
import glob
import random
from math import *
from bitarray import bitarray
from bloomfilter import BloomFilter


# Generate 1 key
master_key = secrets.token_bytes(size)

hmac_digest = hmac.new()