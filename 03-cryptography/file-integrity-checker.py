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
  
