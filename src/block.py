from hashlib import sha256
import json
import time
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = []
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
    def compute_hash(block):
        """ this function will calculate the hash for the block 
        normally in a blockchain we need to hash every single 
        transaction , since this is a first try we will try to keep 
        things simple see https://en.wikipedia.org/wiki/Merkle_tree """
        block_string = json.dumps(self.__dict__,sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

