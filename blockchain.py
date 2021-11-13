import json
from hashlib import sha256
from time import time


class Block:
    def __init__(
        self,
        data: None | dict = None,
        previous_hash: str = None,
        timestamp: float = time(),
    ):
        """Create a new block for the Blockchain

        :param timestamp: Timestamp of the block
        :param data: Data to store in the block
        :param previous_hash: Hash of the previous block
        """
        print("Creating block...")
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self._hash = None
        self.nonce = 0

    @property
    def hash(self):
        """Return the (non-python) hash of the block

        :return: The bytes of the hash of this block
        """
        if self._hash is None:
            hashFun = sha256()
            hashFun.update(self.encode(self.previous_hash))
            hashFun.update(self.encode(self.timestamp))
            hashFun.update(self.encode(self.data))
            hashFun.update(self.encode(self.nonce))
            self._hash = hashFun.hexdigest()
        return self._hash

    def rehash(self):
        """Mark this block to re-calculate the hash the next time it's grabbed."""

        self._hash = None

    @staticmethod
    def encode(val: str | int | float | bytes | dict | None):
        """Generate a UTF-8 bytes object to represent any object

        :param val: Value to encode
        :return: UTF-8 encoded byte representation of val
        """
        return str(val).encode("utf-8")

    def mine(self, difficulty: int):
        """Mine this block until a valid hash is found, based on leading zeros

        Basically, it loops until our hash starts with
        the string 0...000 with length of <difficulty>.

        :param difficulty: length of the leading zeros to mine for
        """
        print("Mining...")
        while self.hash[:difficulty] != "0" * difficulty:
            # We increases our nonce so that we can get a whole different hash.
            self.nonce += 1
            # Update our new hash with the new nonce value.
            self.rehash()


class Blockchain:
    def __init__(self):
        """Initialize the blockchain with an empty, unmined "genesis" block."""
        print("Creating blockchain...")
        self.chain = [Block()]
        self.block_time = 30000
        self.difficulty = 1

    def __iter__(self):
        for block in self.chain:
            yield block

    def __getitem__(self, item):
        return self.chain[item]

    def __repr__(self):
        return json.dumps(
            [
                {
                    k: getattr(item, k)
                    for k in ["data", "timestamp", "nonce", "hash", "previous_hash"]
                }
                for item in self
            ],
            indent=4,
        )

    def append(self, data: None | dict, timestamp: float = time()):
        """Add a new block to the blockchain from a new piece of data and an optional timestamp.

        :param data: Data to add to the new block.
        :param timestamp: UTC timecode of the new block
        """

        # Since we are adding a new block, previous_hash will be the hash of the old latest block
        block = Block(
            data=data,
            previous_hash=self[-1].hash,
            timestamp=timestamp,
        )
        block.mine(self.difficulty)

        # Since now previous_hash has a value, we must reset the block's hash
        self.chain.append(block)

        if time() - self[-1].timestamp < self.block_time:
            self.difficulty += 1
        else:
            self.difficulty -= 1

    def is_valid(self):
        """Iterates over the pairs of sequential blocks to validate that their previous hashes are set correctly

        :return: `True` if Valid, `False` otherwise
        """

        for previous_block, current_block in zip(self.chain[:-1], self.chain[1:]):

            # Check validation
            if previous_block.hash != current_block.previous_hash:
                return False

        return True
