from secure_index import SearchableEncryptionScheme
from decryption import Decryption

sse = SearchableEncryptionScheme()
keys = sse.keygen(20)

# Call function to open a directory and scan all doc files for unique words.
doc_identifier_and_unique_words = sse.get_unique_words('recipes/**/*.txt')

# Build index is a list of tuples containing the bloom filter and the document unique identifier
# i.e. ('document1', document1 bf, 'document2', document2 bf, ...)
index = []

# Destructure the list and create a bloom filter for each document
for i, tuple in enumerate(doc_identifier_and_unique_words):
    doc_id = tuple[0]
    unique_words = tuple[1]
    index.append(sse.build_index(doc_id, keys, unique_words))

print('Number of files before adding:', len(index))
# add a document
sse.add_document(index, keys, 'recipes to add/**/*.txt')
print('Number of files after adding:', len(index))

# delete a document
file = input("Please type in the document name that you wish to delete: ")
sse.delete_document(file, index)

search_keyword = input("Enter your search: ")

trapdoors = sse.trapdoor(keys, search_keyword)
documents = sse.search_index(trapdoors, index)

# To decrypt
decrypt = Decryption(documents)
print(decrypt.decryption())