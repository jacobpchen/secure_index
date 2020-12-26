from secure_index import SearchableEncryptionScheme

sse = SearchableEncryptionScheme()
keys = sse.keygen(20)
print("These are the keys: " + str(keys))

# Call function to open a directory and scan all doc files for unique words.
doc_identifier_and_unique_words = sse.get_unique_words()
print(type(doc_identifier_and_unique_words))
print(doc_identifier_and_unique_words)

# Build index is a list of tuples containing the bloom filter and the document unique identifier.
build_index = []
'''
for index, tuple in enumerate(doc_identifier_and_unique_words):
    doc_id = tuple[0]
    unique_words = tuple[1]
    build_index.append(sse.build_index(doc_id, keys, unique_words))
'''


build_index.append(sse.build_index('document1', keys, ['oranges', 'bananas', 'apples', 'pears', 'groceries', 'shopping', 'list']))
print("This is the type for build index", type(build_index))
print(build_index)

# Stuck here - Codewords aren't matching up
trapdoors = sse.trapdoor(keys, 'oranges')
print(sse.searchIndex(trapdoors, build_index))
