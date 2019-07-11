import hashlib
import requests
from uuid import uuid4
import time

import sys
import os

def handle_id():
    id_file = open('my_id.txt', 'w+')
    if os.stat("my_id.txt").st_size != 0:
        id = id_file.read().split(",")
    else:
        id_file.write(str(uuid4()).replace('-', ''))
        id = id_file.read().split(",")
    id_file.close()
    return id

def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    print("Proof found: " + str(proof))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = int(sys.argv[1])
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    id = handle_id()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
   
        start_time = time.time()
        new_proof = proof_of_work(data.get('proof'))
        end_time = time.time()

        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print(f"Total coins mined: {str(coins_mined)} in {round((end_time - start_time), 2)}s")
        else:
            print(data.get('message'))
