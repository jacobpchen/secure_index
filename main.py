from secure_index import SearchableEncryptionScheme

sse = SearchableEncryptionScheme()
keys = sse.keygen(20)
print("These are the keys: " + str(keys))

# Call function to open a directory and scan all doc files for unique words.
doc_identifier_and_unique_words = sse.get_unique_words()
print(type(doc_identifier_and_unique_words))
print(doc_identifier_and_unique_words)

# Build index is a list of tuples containing the bloom filter and the document unique identifier
# i.e. ('document1', document1 bf, 'document2', document2 bf, ...)
index = []

for i, tuple in enumerate(doc_identifier_and_unique_words):
    doc_id = tuple[0]
    unique_words = tuple[1]
    highest_word_count = tuple[2]
    index.append(sse.build_index(doc_id, keys, unique_words, highest_word_count))

# index.append(sse.build_index('document1', keys, ['bananas', 'oranges', 'apples', 'pears', 'groceries', 'shopping', 'list'], 8))

print("This is the type for build index", type(index))
print("This is how many BF's there are: ", len(index))

trapdoors = sse.trapdoor(keys, 'herb')
print(sse.searchIndex(trapdoors, index))
