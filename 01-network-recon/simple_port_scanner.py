import socket
import sys

# setting up the target IP and the list of ports we want to test
# 127.0.0.1 is localhost, which just loops back to scan our own machine
TARGET_HOST = "127.0.0.1"
PORTS_TO_SCAN = [21, 22, 80, 443, 8080]

print(f"Scanning target: {TARGET_HOST}\n" + "-" * 30)

try:
    # loop through the ports list one by one to automate the checks
    for port in PORTS_TO_SCAN:
        
        # open up a raw socket channel using python's built-in library
        # AF_INET tells the OS we're using an IPv4 address string
        # SOCK_STREAM tells it to use TCP so we can attempt a three-way handshake
        # 'with' handles dropping and closing the connection cleanly after each loop
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # set a 1-second timeout so the script doesn't freeze up completely
            # if a port is firewalled, this forces us to drop it and move on fast
            s.settimeout(1.0)
            
            # here is where we actually knock on the specific target port
            # the OS network stack secretly creates a random source port under the hood
            # the request fires from that random port to our destination port
            # connect_ex returns a status code instead of throwing a massive crash on closed ports
            result = s.connect_ex((TARGET_HOST, port))
            
            # check the response number we got back from the OS
            # 0 is the magic success code for a completed TCP handshake
            # it means the target port sent an acknowledgment packet back to our random source port
            if result == 0:
                print(f"Port {port}: OPEN - This protocol service is actively running right now")
            
            # getting any other number means the connection failed or timed out
            # means nothing is listening or running on this local port right now
            else:
                print(f"Port {port}: Closed - Service is inactive")

# basic keyboard interrupt catcher so hitting Ctrl+C stops the scan instantly
except KeyboardInterrupt:
    print("\nScan cancelled by user. Exiting.")
    sys.exit()
    
