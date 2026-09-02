import hashlib
import sys

# this points to the critical file we want to protect from being messed with
TARGET_FILE = "system_config.txt"

print(f"Calculating fingerprint for: {TARGET_FILE}\n" + "-" * 50)

try:
    # opening the file in read-binary ("rb") mode instead of standard text mode
    # reading raw bytes handles everything down to hidden spaces, formatting, or tabs
    with open(TARGET_FILE, "rb") as file:
        
        # initialize a completely fresh sha256 calculator from the hashlib library
        hasher = hashlib.sha256()
        
        # pull all the raw binary data (1s and 0s) out of the file
        file_bytes = file.read()
        
        # feed those raw binary bytes directly into our hashing engine
        hasher.update(file_bytes)
        
        # here is where we get the actual data we want
        # hexdigest finishes the math and turns the raw result into a readable 64-character text string
        file_fingerprint = hasher.hexdigest()
        
        # printing out the unique cryptographic fingerprint of the file at this exact microsecond
        print(f"SHA-256 Fingerprint: {file_fingerprint}")

# basic fallback if you run the script before actually making the system_config.txt file
except FileNotFoundError:
    print(f"Error: The file '{TARGET_FILE}' was not found. Please create it first.")
    sys.exit()

# ==============================================================================
# HOW TO MATCH AND CHECK IF THE FILE WAS ALTERED (THE VERIFICATION WORKFLOW)
# ==============================================================================
# The next time you want to check if this file was tampered with, you just run 
# this script again. The script will crunch the file's current state and spit 
# out a new SHA-256 hash. 
# 
# Now you just take that new code and compare it to your original baseline code:
# -> If the codes match perfectly: Awesome, there is absolutely no alteration.
# -> If the codes do not match: Stop everything, it has been altered unauthorizedly.
# 
# EXAMPLE OF WHAT THE OUTPUT LOOKS LIKE IN YOUR TERMINAL:
# ------------------------------------------------------------------------------
# Calculating fingerprint for: system_config.txt
# ------------------------------------------------------------------------------
# SHA-256 Fingerprint: 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae
# ------------------------------------------------------------------------------
# 
# QUICK REFRESHER ON THE BASIC THEORY:
# 1. SHA-256 stands for Secure Hash Algorithm 256-bit. It's a one-way mathematical 
#    crusher. You can turn a file into this 64-character string, but you can never 
#    reverse engineer this string back into your original text file.
# 2. The algorithm relies on the "Avalanche Effect". If a bad actor modifies even 
#    a single hidden space, punctuation mark, or letter inside that file, the math 
#    breaks completely under the hood. The resulting hash scrambles into an entirely 
#    unrecognizable new code, giving you instant proof of tampering.
# ==============================================================================
