import hashlib
import json
import time
from typing import List
from uuid import uuid4


class Block:
    """
    Represents a single block in the blockchain.
    """

    def __init__(self, index: int, transactions: List[dict], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self) -> str:
        """
        Computes SHA-256 hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    """
    Simple blockchain implementation with Proof-of-Work.
    """

    difficulty = 4  # Number of leading zeros required in hash

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Generates genesis block and appends it to chain.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float):
        """
        Adds a transaction to unconfirmed transactions pool.
        """
        self.unconfirmed_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def proof_of_work(self, block: Block) -> str:
        """
        Simple Proof-of-Work algorithm.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_block(self, block: Block, proof: str):
        """
        Adds a block to chain after verification.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not proof.startswith("0" * Blockchain.difficulty) or proof != block.compute_hash():
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def mine(self, miner_address: str):
        """
        Mines pending transactions.
        """
        if not self.unconfirmed_transactions:
            return False

        # Reward transaction
        self.unconfirmed_transactions.append({
            "sender": "NETWORK",
            "recipient": miner_address,
            "amount": 1
        })

        new_block = Block(
            index=self.last_block.index + 1,
            transactions=self.unconfirmed_transactions,
            timestamp=time.time(),
            previous_hash=self.last_block.hash
        )

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index


if __name__ == "__main__":
    blockchain = Blockchain()

    # Demo transactions
    blockchain.add_transaction("Alice", "Bob", 5)
    blockchain.add_transaction("Bob", "Charlie", 2)

    print("Mining block...")
    blockchain.mine("Miner1")

    for block in blockchain.chain:
        print(vars(block))
