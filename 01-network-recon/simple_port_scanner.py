import socket
import sys

TARGET_HOST = "127.0.0.1"
PORTS_TO_SCAN = [21, 22, 80, 443, 8080]

print(f"Scanning target: {TARGET_HOST}\n" + "-" * 30)

try:
    for port in PORTS_TO_SCAN:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            result = s.connect_ex((TARGET_HOST, port))
            if result == 0:
                print(f"Port {port}: OPEN")
            else:
                print(f"Port {port}: Closed")

except KeyboardInterrupt:
    print("\nScan cancelled by user. Exiting.")
    sys.exit()
  
