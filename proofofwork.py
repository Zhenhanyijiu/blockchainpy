#!/usr/bin/env python
# example of proof-of-work algorithm
import hashlib
import time
max_nonce = 2 ** 32 # 4 billion
def proof_of_work(header, difficulty_bits):
	# calculate the difficulty target
	target = 2 ** (256-difficulty_bits)
	for nonce in range(max_nonce):
		input=str(header)+str(nonce)
		hash_result = hashlib.sha256(input.encode('utf-8')).hexdigest()
		# check if this is a valid result, below the target
		if int(hash_result, 16) < target:
			print("Success with nonce %d" %nonce)
			print("Hash is %s" %hash_result)
			return (hash_result,nonce)
	print("Failed after %d (max_nonce) tries" % nonce)
	return nonce

#if __name_ == '__main__':
	
nonce = 0
hash_result = ''
# difficulty from 0 to 31 bits
for difficulty_bits in range(32):
	difficulty = 2 ** difficulty_bits
	print("\nDifficulty: %ld (%d bits)" % (difficulty, difficulty_bits))
	print("Starting search...")
	# checkpoint the current time
	start_time = time.time()
	# make a new block which includes the hash from the previous block
	# we fake a block of transactions - just a string
	#new_block = 'test block with transactions' + hash_result
	new_block = '200000000000000000000002a7bbd25a417c0374cc55261021e8a9ca74442b01284f0569c91c008c26e50763e9f548bb8b2fc323735f73577effbc55502c51eb4cc7cf2e52be093a1903a30c' + hash_result
	# find a valid nonce for the new block
	(hash_result, nonce) = proof_of_work(new_block, difficulty_bits)
	# checkpoint how long it took to find a result
	end_time = time.time()
	elapsed_time = end_time - start_time
	print("Elapsed Time: %.4f seconds" % elapsed_time)
		
	if elapsed_time > 0:
		# estimate the hashes per second
		hash_power = float(int(nonce)/elapsed_time)
		print("Hashing Power: %ld hashes per second" % hash_power)