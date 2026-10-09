import hashlib
import json
import os
from datetime import datetime

BLOCKCHAIN_FILE = "blockchain.json"


class Block:
    def __init__(self, index, land_data, previous_hash, timestamp=None, block_hash=None):
        self.index = index
        self.timestamp = timestamp or str(datetime.now())
        self.land_data = land_data
        self.previous_hash = previous_hash
        self.hash = block_hash or self.calculate_hash()

    @property
    def data(self):
        # Compatibility with older templates.
        return self.land_data

    def calculate_hash(self):
        text = (
            str(self.index)
            + self.timestamp
            + json.dumps(self.land_data, sort_keys=True)
            + self.previous_hash
        )
        return hashlib.sha256(text.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "land_data": self.land_data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self.load()

    def genesis_block(self):
        return Block(0, {"message": "Land Registry Genesis Block"}, "0")

    def load(self):
        if not os.path.exists(BLOCKCHAIN_FILE):
            self.chain = [self.genesis_block()]
            self.save()
            return

        try:
            with open(BLOCKCHAIN_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.chain = []
            for item in data:
                land_data = item.get("land_data")
                if land_data is None:
                    land_data = item.get("data", {})

                self.chain.append(
                    Block(
                        item["index"],
                        land_data,
                        item["previous_hash"],
                        item.get("timestamp"),
                        item.get("hash")
                    )
                )

            if not self.chain:
                self.chain = [self.genesis_block()]
                self.save()

        except (json.JSONDecodeError, KeyError, TypeError):
            self.chain = [self.genesis_block()]
            self.save()

    def save(self):
        with open(BLOCKCHAIN_FILE, "w", encoding="utf-8") as file:
            json.dump([block.to_dict() for block in self.chain], file, indent=4)

    def add_block(self, land_data):
        previous = self.chain[-1]
        block = Block(len(self.chain), land_data, previous.hash)
        self.chain.append(block)
        self.save()
        return block

    def verify_chain(self):
        if not self.chain:
            return False

        for i, block in enumerate(self.chain):
            if block.hash != block.calculate_hash():
                return False

            if i == 0:
                if block.previous_hash != "0":
                    return False
            elif block.previous_hash != self.chain[i - 1].hash:
                return False

        return True

    def find_land(self, land_id):
        return [
            block for block in self.chain
            if isinstance(block.land_data, dict)
            and block.land_data.get("land_id") == land_id
        ]
