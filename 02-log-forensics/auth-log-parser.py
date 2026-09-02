LOG_FILE = "auth.log"

print(f"Parsing log file: {LOG_FILE}\n" + "-" * 40)

try:
    # open up the log file to read it
    # 'with' handles closing the file automatically so we don't leak system memory
    with open(LOG_FILE, "r") as file:
        
        # loop through the text file line by line 
        # this stops the script from loading a massive file all at once and crashing
        for line in file:
            
            # check if the phrase "Failed password" is in the text
            # if it's not there, we just skip it because it's a normal login or system noise
            if "Failed password" in line:
                
                # chop the line into an array of separate words wherever there is a space
                # we need to do this so we can isolate and count the exact position of the text
                words = line.split()
                
                # standard system logs always stamp the word 'from' right before the IP address
                if "from" in words:
                    
                    # find where the word 'from' sits inside our array
                    from_index = words.index("from")
                    
                    # here is where we get the actual data we want
                    # we grab the item exactly one slot to the right of 'from' to snatch the raw IP
                    ip_address = words[from_index + 1]
                    
                    # print out the attacker's IP so we can throw it into a firewall blocklist
                    print(f"Suspicious IP Found: {ip_address}")

# quick fallback so the program doesn't throw a giant python crash if the file is missing
except FileNotFoundError:
    print(f"Error: The file '{LOG_FILE}' was not found. Please create it first.")
  
