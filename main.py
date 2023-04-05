import hashlib
import os

def computinghash(file_path):
    #Computing the hash value of a file.
    hashing = hashlib.sha1() 
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashing.update(chunk)
    return hashing.digest()



def computingTopHash(file_paths):
    #Compute the Top Hash for files.
    #Computing the hash value of each file
    fileHash = [computinghash(path) for path in file_paths]

    #Building the Merkle Hash Tree
    tree = fileHash
    while len(tree) > 1:
        if len(tree) % 2 == 1:
            tree.append(tree[-1]) # duplicate last hash when odd number of hashes
        pairs = [tree[i:i+2] for i in range(0, len(tree), 2)]
        tree = [hashlib.sha1(pair[0] + pair[1]).digest() for pair in pairs]

    #Returning the Top Hash
    return tree[0]



#Testing the program
if __name__ == '__main__':
    #Compute Top Hash of the files listed
    file_paths = ['L1.txt', 'L2.txt', 'L3.txt', 'L4.txt']
    top_hash = computingTopHash(file_paths)
    print(f"Top Hash: {top_hash.hex()}")

    #Modify the file and check for Top Hash changes
    with open('L1.txt', 'wb') as f:
        f.write(b'new content')
    NewTopHash = computingTopHash(file_paths)
    print(f"New Top Hash: {NewTopHash.hex()}")

    if top_hash == NewTopHash:
        print("Error: The Top Hash can not match!")
