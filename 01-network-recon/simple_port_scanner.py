import socket
import sys

# Setting up the target IP and the list of ports we want to test
# 127.0.0.1 is localhost, which means we are scanning our own computer
TARGET_HOST = "127.0.0.1"
PORTS_TO_SCAN = [21, 22, 80, 443, 8080]

print(f"Scanning target: {TARGET_HOST}\n" + "-" * 30)

try:
    # This loop goes through our array of ports one by one to automate the scan
    for port in PORTS_TO_SCAN:
        
        # This initializes the socket channel using the built-in library
        # AF_INET tells the OS we are using an IPv4 address
        # SOCK_STREAM tells it to use the TCP protocol (the three-way handshake)
        # Using 'with' acts as a manager that automatically closes the socket after each check
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # We set a 1-second timeout so the script doesn't freeze forever
            # If a port is blocked or firewalled, the script will give up and move on quickly
            s.settimeout(1.0)
            
            # This is the exact instance where the scanner targets the port
            # Under the hood, the Operating System network stack generates a random source port
            # The packet is sent from that random port to the destination port we specified
            # We use connect_ex instead of connect so the script doesn't crash on closed ports
            result = s.connect_ex((TARGET_HOST, port))
            
            # Evaluating the result from the OS network stack
            # 0 is the magic number meaning the TCP Three-Way Handshake was successful
            # It means the target host port sent back an acknowledgment packet to our random port
            if result == 0:
                print(f"Port {port}: OPEN - This protocol service is actively running right now")
            
            # Any non-zero number means the connection failed or was refused
            # It means the service on our local host is inactive at the current moment
            else:
                print(f"Port {port}: Closed - Service is inactive")

# This is an emergency brake so we can press Ctrl+C to stop the loop instantly
except KeyboardInterrupt:
    print("\nScan cancelled by user. Exiting.")
    sys.exit()
    
