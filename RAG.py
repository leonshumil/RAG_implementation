from typing import List, Optional, Set
from dataclasses import dataclass
import string

# RAG paramaters
#tabale size should be prime number
TABLE_SIZE = 101
#use for hamming distance
HAMMING_THRESHOLD = 10

##################################### DATA STRUCTERS ###################################
@dataclass
#proporties of an item store in the HashTable
class HashNode:
    query: str #input type
    response: str #output type
    binary_code: int #binary hashing
    next: Optional['HashNode'] = None # link list

#proporties of HashTable
class HashTable:
    def __init__(self):
        self.buckets = [None] * TABLE_SIZE #creat empty table 
        self.size = 0 #count how many pairs inserted

################################### BUILD CUSTOM HASH TABLE ###########################
def custom_hash(query: str) -> int:

    # some words have no real meaning in context of LLM so we can remove them
    redundant_words = {'the', 'a', 'an', 'is', 'are', 'what', 'how', 'to', 'for', 'of', 'in'}
    
    # change to lower case and remove punctuation
    text = query.lower().translate(str.maketrans('', '', string.punctuation))
    #split words int tokens
    tokens = text.split()
    
    # remove redundant words and short ones
    clean_tokens = [t for t in tokens if t not in redundant_words and len(t) > 1]
    
    # handel edge case where token is only redundant words and short one
    if not clean_tokens:
        clean_tokens = tokens 
    
    # use sort for unified order of the tokens
    clean_tokens.sort()

    # init binary hash vector   
    vector = [0] * 64

    #the hashing phase 
    #convert token to number
    for token in clean_tokens:
        word_hash = 0
        for char in token:
            word_hash = word_hash * 31 + ord(char) # used to made words into number ( same as hashlib do)
        
        #simhash
        for i in range(64):
            if (word_hash >> i) & 1:
                vector[i] += 1
            else:
                vector[i] -= 1
    
    # compress vector to 64 bit
    fingerprint = 0
    for i in range(64):
        if vector[i] > 0:
            fingerprint |= (1 << i)
            
    return fingerprint


######################################### INSERT ##############################################

def insert(table: HashTable, query: str, response: str):
   
    # get the binary hash
    binary_code = custom_hash(query)
    
    # calc index
    bucket_index = binary_code % TABLE_SIZE
    
    # creat node for the inserted value
    node = HashNode(query, response, binary_code)
    
    # do chaining for collision evoidense 
    node.next = table.buckets[bucket_index]
    table.buckets[bucket_index] = node
    table.size += 1



######################################### RETRIEVE ##############################################

def retrieve(table: HashTable, query: str) -> Optional[str]:

    #use hashing function and get the correlated bucket
    query_code = custom_hash(query)
    bucket_index = query_code % TABLE_SIZE
    
    best_response = None
    #equivalent to inf in 64 bit 
    min_distance = 65 
    current = table.buckets[bucket_index]
    
    #search the link list in the bucket for best response
    while current:
        # using xor to find hamming distance
        xor_val = query_code ^ current.binary_code
        distance = bin(xor_val).count('1')
        
        # find closest match 
        if distance < min_distance and distance <= HAMMING_THRESHOLD:
            min_distance = distance
            best_response = current.response
            
        current = current.next
        
    if best_response:
        return best_response
    else:
        return None
    

######################################### DEMO ##############################################

def main():
    rag = HashTable()
    
    # pair prompt response
    data = [

        ("The lecturer and teaching assistant are totally awesome", "The course staff is amazing!"),
        ("The DS course team is actually really good", "The course staff is amazing!"), 
        ("Are the DS course team good?", "The course staff is amazing!"), 

        ("What is a hash table?", "Hash table is a data structure that maps keys to values for fast O(1) lookups."),
        ("Can you recommend a data structure with fast O(1) lookups?", "Hash table is a data structure that maps keys to values for fast O(1) lookups."),

        ("How do we deal with collisions in the table?", "Common methods are chaining (linked lists)."),

        ("What does RAG stand for?", "Retrieval-Augmented Generation."),
        ("Can you recommend a way to not only rely on internal data in LLM?", "Retrieval-Augmented Generation."),

        ("When is this assignment due?", "The deadline is January 25th."),
        ("What's the submission date?", "The deadline is January 25th."),

        ("What language is popular for LLMs?", "Python is a popular language to write LLMs."),
        ("Why was this assignment asked to use Python?", "Python is a popular language to write LLMs.")

    ]
    
    #insert
    for q, r in data:
        insert(rag, q, r)
        
    print(f"Loaded {rag.size} items.")
    
    # test 1
    q1 = "are the DS course team ok?"
    print(f"\nQuery: {q1}")
    print(f"Result: {retrieve(rag, q1)}")

    # test 2
    q2 = "What is hash table?" 
    print(f"\nQuery: {q2}")
    print(f"Result: {retrieve(rag, q2)}")

if __name__ == "__main__":
    main()
