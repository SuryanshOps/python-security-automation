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
            # both successful and unsuccessful attempts are recorded in this file side-by-side:
            # 
            # SUCCESSFUL LOGIN FORMAT:
            # Feb 23 12:10:05 server sshd: Accepted password for james from 192.168.1.50 port 54321 ssh2
            # 
            # MALICIOUS/UNSUCCESSFUL LOGIN FORMAT:
            # Feb 23 12:05:22 server sshd: Failed password for root from 203.0.113.5 port 49211 ssh2
            # 
            # Our filter strictly looks for "Failed password", so it skips all the successful entries automatically
            if "Failed password" in line:
                
                # chop the line into an array of separate words wherever there is a space
                # usernames change in length, so the word array lets us find static anchor points
                words = line.split()
                
                # the OS always stamps the word 'from' right before the attacker's IP address
                # we use 'from' as a permanent physical marker to handle shifting text lengths
                if "from" in words:
                    
                    # find the exact position index where the word 'from' sits inside our array
                    from_index = words.index("from")
                    
                    # here is where we get the actual data we want
                    # jumping exactly one slot to the right (+ 1) guarantees we snatch the raw IP address
                    ip_address = words[from_index + 1]
                    
                    # print out the attacker's IP so we can throw it into a firewall blocklist
                    print(f"Suspicious IP Found: {ip_address}")

# quick fallback so the program doesn't throw a giant python crash if the file is missing
except FileNotFoundError:
    print(f"Error: The file '{LOG_FILE}' was not found. Please create it first.")
    
