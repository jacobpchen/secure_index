from secure_index import SearchableEncryptionScheme

sse = SearchableEncryptionScheme()
keys = sse.keygen(20)
print("These are the keys: " + str(keys))
# trapdoors = sse.trapdoor(keys, 'test')
# print("These are the trapdoors: " + str(trapdoors))

# Build index is a list of tuples containing the bloom filter and the document unique identifier.
build_index = []

build_index.append(sse.build_index('document1', keys, ['apples', 'bananas', 'oranges', 'pears', 'groceries', 'shopping', 'list']))
print(type(build_index))
print(build_index)

trapdoors = sse.trapdoor(keys, 'bananas')

