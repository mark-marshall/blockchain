import hashlib
import requests
from uuid import uuid4
import time

import sys
import os

def handle_id():
    """
    Checks to see whether a my_id text file exists and creates one
    with a new ID for the miner if it doesn't
    """
    try:
        id_file = open('credit_for_mining_p/my_id.txt', 'r')
        id_file.close()
    except:
        id_file = open('credit_for_mining_p/my_id.txt', 'w')
        id_file.write(str(uuid4()).replace('-', ''))
        id_file.close()

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
    handle_id()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        # record time of proof finding for client
        start_time = time.time()
        new_proof = proof_of_work(data.get('proof'))
        end_time = time.time()
        # grab the id to send to the mine endpoint
        sender_id_file = open('credit_for_mining_p/my_id.txt', 'r')
        sender_id = sender_id_file.read()
        # assemble data for the mine endpoint
        post_data = {"proof": new_proof, "id": sender_id}
        # make the request to /mine
        r = requests.post(url=node + "/mine", json=post_data)
        # close the id file
        sender_id_file.close()
        # handle response from server for client
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print(f"Total coins mined: {str(coins_mined)} in {round((end_time - start_time), 2)}s")
        else:
            print(data.get('message'))
