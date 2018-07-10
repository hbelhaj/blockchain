from blockchain.block import *
class Blockchain:
    # complexity of proof of work algorithm
    complexity = 2

    def __init__(self):
        self.unconfirmed_transactions = []  # transactions to add to the blockchain
        self.chain = []
        self.create_genesis_block()
        """ we need to init the first block of the blockchain with some
        hash since the other blocks have the previous block hash """

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        """we will try different values of randint that satisfies
        our complexity criteria, this is a naive  method but the goal here
        is to demonstrate a simple version of PoW """
        block.randint = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.complexity):
            block.randint += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_block(self, block, proof):
        """ function to add a block to the blockchain, in
        order to add a block we need to check if the PoW is
        correct and that previous hash point to the last block
        of the BC """
        previous_hash = self.last_block().hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """ we need to verify that the hash verify the criteria
        of PoW """
        return (block_hash.startswith('0' * Blockchain.complexity) and block_hash == block.compute_hash())

    def mine(self):
        """ this function serves as an interface to add the transactions
        to the blockchain by adding them to the block and calculating the Proof of Work"""

        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block()
        new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, timestamp=time.time(), previous_hash=last_block.hash)
        proof  = self.proof_of_work(new_block)
        self.add_block(new_block,proof)
        self.unconfirmed_transactions = []
        return new_block.index
        

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)


