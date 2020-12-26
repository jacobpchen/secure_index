# Secure Index

###### tags: `secure index` `searchable encryption scheme` `bloom filter` `encryption`

## What is a secure index?

### Introduction

#### 1. What is a secure index?
   - A secure index allows a user to query a server with a "trapdoor" for a word x to test in O(1) time if the index contains x per document. 
   - The main purpose of this application is to allow the searching of encrypted data. As more companies are shifting to public cloud backs up and remote data storage are commonly being stored offsite. Sensitive documents should be encrypted before storing remotely.
   - However once the files are encrypted it is difficult to retrieve files based on their content. For example if a user wants to retrieve all files containing the word "password" from a server the user must download all the files, decrypt them, and then search the documents for the word "password".
   - This application will allow the user to search for the keyword "password" while ensuring that the server learns nothing about the keyword of the document contents.

### Definitions
- digest
- trapdoor
- codeword
- bloom filter
  
### How does it work?

The application implements 4 main functions:
- Keygen(size): Given a size parameter in bytes generates a key in hexadecimal that is double the size. The default setting is 20 bytes. The key that is generated is 40 bytes long which matches the HMAC-SHA1 digest. Returns a list of keys (kpriv).
- Trapdoor(kpriv, *w*): Given the list of keys and word *w*, outputs the trapdoor T~w~ for *w*. 
- BuildIndex(D, Kpriv): Given a unique document identifier (i.e. file name) creates a list of codewords to insert into the document's bloom filter. Returns the document bloom filter to be stored in a list of bloom filters (I~Did~).
- SearchIndex(T~w~, I~Did~): The input is the trapdoor generated from the trapdoor function for word *w* and the list of bloom filters (I~Did~). Calculates the codeword for *w* and searches in linear time if the list of bloom filters (I~Did~) contains the codewords. Return 1 or 0 and the document identifier.

#### Things to add
- [ ] High level flow diagram
- [ ] Ability to encrypt files and transfer it via FTP to a remote server.

