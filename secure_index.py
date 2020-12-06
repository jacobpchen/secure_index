import hmac
import hashlib
import secrets

class SearchableEncryptionScheme():

    def keygen(self, size):
        # Generates a master_key of size bytes
        master_key = secrets.token_bytes(size)

        # number of functions
        r = 5

        # Create an empty list to hold the kpriv
        kpriv = []
        for i in range (0,r):

            hmac_digest = hmac.new(master_key, msg=secrets.token_bytes(size), digestmod=hashlib.sha1)
            hmac_digest = hmac_digest.hexdigest()
            kpriv.append(hmac_digest)

        # hmac digest 40 bytes length
        print(kpriv)
        return kpriv

    def trapdoor(self, kpriv, w):


