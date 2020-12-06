from secure_index import SearchableEncryptionScheme

sse = SearchableEncryptionScheme()
keys = sse.keygen(20)
print("These are the keys: " + str(keys))
trapdoors = sse.trapdoor(keys, 'test')
print("These are the trapdoors: " + str(trapdoors))

# SearchableEncryptionScheme.keygen()

