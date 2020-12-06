import hmac
import hashlib
import secrets

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

