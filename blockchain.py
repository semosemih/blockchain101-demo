import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, transactions, difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = int(time.time())
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        while True:
            value = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.transactions) + str(self.nonce)
            calculated_hash = hashlib.sha256(value.encode()).hexdigest()
            if calculated_hash[:self.difficulty] == "0" * self.difficulty:
                return calculated_hash
            self.nonce += 1


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.mempool = []

    def create_genesis_block(self):
        return Block(0, "0", ["Genesis Block"], 2)  # Difficulty level set to 2 initially

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_last_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash() or current_block.previous_hash != previous_block.hash:
                return False
        return True

    def add_to_mempool(self, data):
        self.mempool.extend(data)
    
    def view_mempool(self):
        print("Last 5 entries in the mempool:")
        if len(self.mempool) > 5:
            for i, transaction in enumerate(self.mempool[-5:], start=1):
                print(f"{i}. {transaction}")
        else:
            for i, transaction in enumerate(self.mempool, start=1):
                print(f"{i}. {transaction}")

# Create a blockchain
my_blockchain = Blockchain()

# Collect data for blocks
transaction_data = []
for i in range(15):
    data = input(f"Enter transaction data {i + 1}: ")
    transaction_data.append(data)

# Create 5 blocks with the provided data, each containing 2 transactions
for i in range(5):
    user_difficulty = int(input(f"Enter difficulty level (number of leading zeros) for block {i + 1}: "))
    start_idx = i * 2
    end_idx = start_idx + 2
    my_blockchain.add_block(Block(i + 1, my_blockchain.get_last_block().hash, transaction_data[start_idx:end_idx], user_difficulty))

# View the last 5 entries in the mempool
my_blockchain.view_mempool()

# Print the blockchain
for block in my_blockchain.chain:
    print("Block #", block.index)
    print("Hash:", block.hash)
    print("Previous Hash:", block.previous_hash)
    print("Transactions:", block.transactions)
    print("Timestamp:", block.timestamp)
    print()

# Validate the blockchain
if my_blockchain.is_chain_valid():
    print("Blockchain is valid.")
else:
    print("Blockchain is invalid.")
