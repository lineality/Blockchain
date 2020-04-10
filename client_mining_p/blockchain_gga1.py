import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

# are we supposed to import from miner.py?
# from miner import *


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        if len(self.chain) > 0:
            block_string = json.dumps(self.last_block, sort_keys=True)
            guess = f"{block_string}{proof}".encode()
            current_hash = hashlib.sha256(guess).hexdigest()
        else:
            current_hash = ""

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
            "hash": current_hash,
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block": <dict> Block
        "return": <str>
        """
        # Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        # Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):

        # Validates the Proof:  Does hash(block_string, proof) contain 3
        # :return: True if resulting hash is valid, else False

        block_string = json.dumps(block_string, sort_keys=True)
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # returns True/False
        return guess_hash[:3] == "000"
        # return guess_hash[:6] == "000000"


# End of Class


# answer_already_found_flag
answer_already_found_flag = False

# answer_ok flag
answer_ok = False


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace("-", "")

# Instantiate the Blockchain
blockchain = Blockchain()  # best name ever


@app.route("/mine", methods=["POST"])
def mine():

    # # dummy output
    # response = {"message": "New Block Forged"}
    # return jsonify(response), 200

    # this gets the json object
    json_obj = request.get_json()  # (force=True)
    # these lines brake up the json object into variables use-able by python
    proof_input = json_obj["proof"]
    id_input = json_obj["id"]

    # check for input, give error if input missing
    if not proof_input:
        response = {"message": "400 error: missing proof input."}
        return jsonify(response), 400

    if not id_input:
        response = {"message": "400 error: missing id input."}
        return jsonify(response), 400

    # # test: validate the sumbission
    # if answer_already_found_flag is False:

    # inspection
    print("checking hash")

    # this sets the answer ok flag to T or F
    answer_ok = blockchain.valid_proof(blockchain.last_block, proof_input)

    print("answer_ok", answer_ok)

    if answer_ok is True:

        # inspection
        print("test passed")

        previous_hash = blockchain.hash(blockchain.last_block)

        # add new block to chain
        block = blockchain.new_block(proof_input, previous_hash)

        response = {
            "message": "New Block Forged",
            "index": block["index"],
            "transactions": block["transactions"],
            "proof": block["proof"],
            "previous_hash": block["previous_hash"],
        }

        return jsonify(response), 200

    # else:
    #     response = {"message": "400 error: something bad happened..."}
    #     return jsonify(response), 400

    # otherwise, invalid 400

    # # elif id_input is not None and proof_input is not None:
    # elif answer_already_found_flag is True and answer_ok is True:
    #     response = {"message": "New Block Forged"}
    #     return jsonify(response), 200


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {"length": len(blockchain.chain), "chain": blockchain.chain}
    return jsonify(response), 200


@app.route("/lastblock", methods=["GET"])
def last_block():
    response = {
        "last_block": blockchain.last_block,
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
