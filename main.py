from secure_index import SearchableEncryptionScheme

sse = SearchableEncryptionScheme()
keys = sse.keygen(20)

# Call function to open a directory and scan all doc files for unique words.
doc_identifier_and_unique_words = sse.get_unique_words()

# Build index is a list of tuples containing the bloom filter and the document unique identifier
# i.e. ('document1', document1 bf, 'document2', document2 bf, ...)
index = []

for i, tuple in enumerate(doc_identifier_and_unique_words):
    doc_id = tuple[0]
    unique_words = tuple[1]
    index.append(sse.build_index(doc_id, keys, unique_words))

'''
Ask user to select folder path
Accept multiple words? chicken pesto (search once for chicken then search only those docs for pesto?)
'''

search_keyword = input("Enter your search: ")
# change to lower case for search keyword

trapdoors = sse.trapdoor(keys, search_keyword)
documents = sse.searchIndex(trapdoors, index)
print(documents)