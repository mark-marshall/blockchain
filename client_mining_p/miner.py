import hashlib
import requests

import sys

def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 5
    leading zeroes?
    """
    # encode a guess
    guess = f"{last_proof}{proof}".encode()
    # hashing the guess
    guess_hash = hashlib.sha256(guess).hexdigest()

    # return True if leading 5 digits of the hash are zreos
    return guess_hash[0:5] == "00000"

def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 4 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """
    # start our proof at zero
    proof = 0

    # increment proof by 1 until valid proof returns true
    while valid_proof(last_proof, proof) is False:
        proof += 1

    # once a valid proof is reached return it
    return proof

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        res = requests.get(f"{node}/last-proof")
        last_proof = res.json()['last_proof']
        # Find a new proof
        new_proof = proof_of_work(last_proof)
        # Post the proof to the server
        proof_submission = requests.post(f"{node}/mine", json={"proof": new_proof})
        proof_res = proof_submission.json()
        if proof_res['message'] == 'New Block Forged':
            # Add 1 to the number of coins mined and print it
            coins_mined += 1
            print(f"Coins mined: {coins_mined}")
        # Otherwise, print the failure message from the server
        else:
            print(proof_res['failure'])
