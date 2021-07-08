import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

from miner import*

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
            guess = f'{block_string}{proof}'.encode()
            current_hash = hashlib.sha256(guess).hexdigest()
        else:
            current_hash = ""

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'hash': current_hash,
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

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        block_string = json.dumps(block_string, sort_keys=True)
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # returns True/False
        return guess_hash[:6] == "000000"


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()  # best name ever


@app.route('/mine', methods=['POST'])
def mine():

    # this gets the json object
    json_obj = request.get_json()  #(force=True)

    # # start set to: None
    # proof_input = None
    # id_input = None

    # these lines brake up the json object into variables use-able by python
    proof_input = json_obj["proof"]
    id_input = json_obj["id"]

    # check for input
    if len(proof_input) == 0 or not proof_input:
        response = {"message": "400 error: missing proof input. You have failed. You are done. Go away."}
        return jsonify(response), 400

    if len(id_input) == 0 or not id_inpt:
        response = {"message":"400 error: missing id input."}
        return jsonify(response), 400


    # create is answer_already_found_flag
    answer_already_found_flag = False

    # answer_ok flag
    answer_ok = False

    # check the answer (if answer not already found)
    if answer_already_found_flag == False:
        # this sets the answer ok flag to T or F
        answer_ok = valid_proof(last_block, proof_input)

    # check input
    answer_ok = blockchain.valid_proof(blockchain.last_block, proof_input)

    # if the incoming answer is good, and the answer_already_found_flag is false
    # then the answer is valid
    if answer_ok == True and answer_already_found_flag == False:
        
        # this puts the new valid block ont he chain
        # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }

    response = {'message':f'happy trees love {proof_input}{id_}'}

    return jsonify(response), 200
    
    # otherwise, invalid 400


    # Run the proof of work algorithm to get the next proof
    # proof = blockchain.proof_of_work()

    # * Use `data = request.get_json()` to pull the data out of the POST
    # * Note that `request` and `requests` both exist in this project
    # * Check that 'proof', and 'id' are present
    # * return a 400 error using `jsonify(response)` with a 'message'
    # * Return a message indicating success or failure.
    # Remember, a valid proof should fail for all senders except the first. 

    # # Forge the new Block by adding it to the chain with the proof
    # previous_hash = blockchain.hash(blockchain.last_block)
    # block = blockchain.new_block(proof, previous_hash)

    # response = {
    #     'message': "New Block Forged",
    #     'index': block['index'],
    #     'transactions': block['transactions'],
    #     'proof': block['proof'],
    #     'previous_hash': block['previous_hash'],
    # }

    # proof is their dictionary and salt
    # we checking by running 
    # 000000 only the first is valid

    # make it a game with one winer



    #elif id_input is not None and proof_input is not None:
    elif answer_already_found_flag == True and answer_ok == True:
        response = {"message":"New Block Forged"}
        return jsonify(response), 200

    #elif id_input is not None and proof_input is not None:
    elif answer_already_found_flag == True and answer_ok == False:
        response = {"message":"200: proof and id recieved. someone beat you to it"}
        return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200

@app.route('/lastblock', methods=['GET'])
def last_block():
    response = {
        'last_block': blockchain.last_block,
    }
    return jsonify(response), 200

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)