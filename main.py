from secure_index import SearchableEncryptionScheme

sse = SearchableEncryptionScheme()
keys = sse.keygen(20)
print("These are the keys: " + str(keys))

# Call function to open a directory and scan all doc files for unique words.
# Calculate the average for noise
average_unique_words = sse.calculate_noise()
# sse.set_r(average_unique_words)



# Build index is a list of tuples containing the bloom filter and the document unique identifier.
build_index = []
build_index.append(sse.build_index('document1', keys, ['oranges', 'bananas', 'apples', 'pears', 'groceries', 'shopping', 'list']))
print("This is the type for build index", type(build_index))
print(build_index)



# Stuck here - Codewords aren't matching up
trapdoors = sse.trapdoor(keys, 'apples')
print(sse.searchIndex(trapdoors, build_index))
