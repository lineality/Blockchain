import hashlib
import requests

# import random
import sys
import json

# note: ID is user ID
# proof: is the salt-nance-proof that when added to the last block
#


def proof_of_work(block):

    block_string = json.dumps(block["last_block"], sort_keys=True)
    # block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while not valid_proof(block_string, proof):
        proof += 1
        # proof = str(random.random())
    return proof


# def valid_proof(block_string, proof):
#
#     guess = f"{block_string}{proof}".encode()
#     guess_hash = hashlib.sha256(guess).hexdigest()
#     # returns True/False
#     return guess_hash[:3] == "000"


def valid_proof(block_string, proof):

    # Validates the Proof:  Does hash(block_string, proof) contain 3
    # :return: True if resulting hash is valid, else False

    block_string = json.dumps(block_string, sort_keys=True)
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # returns True/False
    return guess_hash[:3] == "000"
    # return guess_hash[:6] == "000000"


# 1. get last block from endpoint
# 2. make a valid nonce-proof
# 3.
# 4. get the new-new block when you test the validity
#

# recording user id?

if __name__ == "__main__":
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://0.0.0.0:5000"

    # variable
    blocks_mined_or_coins = 0

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # for testing only
    clicker = 0

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/lastblock")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # Get the block from `data` and use it to look for a new proof
        # data = {'last_block': blockchain.last_block}
        # print("data", data)
        new_proof = proof_of_work(data)
        # print("new_proof", new_proof)

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)

        # is this the data recieved?
        new_response_data = r.json()

        # If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.

        if new_response_data["message"] == "New Block Forged":
            blocks_mined_or_coins += 1
            print(f"blocks_mined_or_coins = {blocks_mined_or_coins}")

        elif new_response_data["message"] != "New Block Forged":
            print(new_response_data["message"])

        print(f"blocks_mined_or_coins = {blocks_mined_or_coins}")

        # stop miner after 5 blocks
        clicker += 1
        love = 5
        if blocks_mined_or_coins is love or clicker is love:
            break
