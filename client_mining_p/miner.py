import hashlib
import requests
import random
import sys
import json

# note: ID is user ID
# proof: is the salt-nance-proof that when added to the last block
# 

def proof_of_work(block):

    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while not valid_proof(block_string, proof):
        proof += 1
        #proof = str(random.random())
    return proof

def valid_proof(block_string, proof):

    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # returns True/False
    return guess_hash[:3] == "000"



if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://0.0.0.0:5000"

    # variable
    number_of_blocks_mined = 0

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

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

        # TODO: Get the block from `data` and use it to look for a new proof
        # data = {'last_block': blockchain.last_block}

        print("starting")
        new_proof = proof_of_work(data)
        print("done")

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        # pass
        # 
        if data["message"] == 'New Block Forged':
            number_of_blocks_mined += 1
            print(f'number_of_blocks_mined = {number_of_blocks_mined}')

        elif data["message"] != 'New Block Forged':
            print(data["message"])
            
        love = 5
        if number_of_blocks_mined == love:
            break

