from hashlib import sha256
import json
import time

class Block:
    def __init__(self, index, transactions,  timestamp,previous_hash,hash = '',nonce = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        if hash != '':
            self.hash = hash
    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    def get_dict(self):
        return self.__dict__
