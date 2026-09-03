# Simple Python Port Scanner (SPPS)

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Concept](https://img.shields.io/badge/concept-Network_Engineering-purple.svg) ![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Academic Integrity & Ethics](#academic-integrity--ethics)
3. [Technical Architecture](#technical-architecture)
4. [Engineering Analysis & Trade-offs](#engineering-analysis--trade-offs)
5. [Installation & Execution](#installation--execution)
6. [Source Code Implementation](#source-code-implementation)
7. [Future Enhancements](#future-enhancements)
8. [Conclusion](#conclusion)

---

## Executive Summary

The **Simple Python Port Scanner (SPPS)** is a lightweight, dependency-free network utility designed to identify open TCP ports on a host system. Built entirely using Python's standard library, this project serves as a practical application of foundational computer science concepts, specifically focusing on network engineering, socket programming, and system-level I/O operations. 

By avoiding third-party libraries, the project demonstrates a core understanding of how operating systems handle network traffic, exception handling, and resource allocation at the socket level.

---

## Academic Integrity & Ethics

> **Note on Ethical Usage:** 
> This tool was developed strictly for **educational purposes, local environment testing, and academic demonstration**. In the field of computer science, understanding network auditing is essential for building robust, secure systems. However, scanning external networks without explicit, written authorization is a violation of ethical computing standards. This script is configured by default to safely target only the local loopback environment (`127.0.0.1`).

---

## Technical Architecture

### 1. TCP vs. UDP Protocol 
This application focuses exclusively on **TCP (Transmission Control Protocol)** rather than UDP. TCP is a connection-oriented protocol, meaning it requires a strict handshake to establish communication. This makes TCP ideal for port scanning: if the target completes the handshake, we know with 100% certainty that the port is open and listening. (UDP, by contrast, is "fire and forget," meaning an open UDP port often won't send any reply at all).

### 2. The TCP Three-Way Handshake
To determine the state of a network service, the script utilizes the OS to perform the following sequence:

| Step | Packet | Sender | Description |
| :--- | :--- | :--- | :--- |
| **1** | `SYN` | Scanner | Requests to synchronize and open a connection to the target port. |
| **2** | `SYN-ACK` | Target | If the port is open, the target acknowledges the request. *(If closed, returns `RST`)* |
| **3** | `ACK` | Scanner | Acknowledges the target's response, completing the connection. |

### 3. Socket Programming Interface
The script interfaces with the OS network stack using Berkeley-style sockets:
*   `AF_INET`: Configures the socket to route over the standard IPv4 addressing architecture.
*   `SOCK_STREAM`: Instructs the operating system to instantiate a TCP socket and natively manage the three-way handshake sequence described above.

---

## Engineering Analysis & Trade-offs

### Resource Management (The `with` Statement)
Operating systems impose strict limits on how many files or network sockets a program can have open simultaneously. In this script, the socket is wrapped in a Python context manager (`with socket.socket(...) as s:`). This guarantees that the network socket is instantly closed and destroyed the moment the port check is finished, preventing resource exhaustion and memory leaks during the loop.

### Exception Handling & User Experience
Standard port scanners can take a long time to run. If a user tries to cancel a standard Python script by pressing `Ctrl+C`, the terminal will usually throw a massive, ugly `KeyboardInterrupt` error trace. This project actively catches that interrupt, safely stops the scan, and prints a clean exit message.

### Time Complexity & Performance
In its current iteration, the application processes ports sequentially in a single thread. 
*   **The Firewall Problem:** If a network firewall drops packets silently, the scanner must wait for the connection attempt to time out. 
*   **The Solution:** A strict `1.0` second timeout is enforced via `s.settimeout(1.0)`. While this prevents the script from hanging indefinitely, scanning thousands of silently dropped ports would still take a long time. This highlights a clear engineering trade-off: keeping the code simple and readable versus optimizing for maximum speed.

---

## Installation & Execution

This project requires **Python 3.6+** (for f-string formatting support). No external dependencies or virtual environments are required.

**1. Clone the repository:**
```bash
git clone https://github.com/SuryanshOps/python-security-automation.git
cd python-security-automation
cd 03-cryptography 

cd simple-port-scanner
```

**2. Execute the script:**
```bash
python3 port_scanner.py
```

**Example Standard Output:**
```text
Scanning target: 127.0.0.1
------------------------------
Port 21: Closed - Service is inactive
Port 22: Closed - Service is inactive
Port 80: OPEN - Service is actively running
Port 443: Closed - Service is inactive
Port 8080: Closed - Service is inactive
```

---

## Source Code Implementation

```python
import socket
import sys

# Target configuration: Defaulted to local loopback address for safe, ethical testing.
TARGET_HOST = "127.0.0.1"
PORTS_TO_SCAN = [21, 22, 80, 443, 8080]

print(f"Scanning target: {TARGET_HOST}\n" + "-" * 30)

try:
    for port in PORTS_TO_SCAN:
        
        # Context manager ('with') ensures system file descriptors (sockets) 
        # are properly released back to the OS after each iteration, preventing memory leaks.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # Enforce a strict 1-second timeout to prevent the thread from 
            # blocking indefinitely on dropped packets (e.g., stealth firewalls).
            s.settimeout(1.0)
            
            # connect_ex() returns a C-level integer indicator (0 for success).
            # This avoids raising a blocking ConnectionRefusedError exception.
            result = s.connect_ex((TARGET_HOST, port))
            
            if result == 0:
                print(f"Port {port}: OPEN - Service is actively running")
            else:
                print(f"Port {port}: Closed - Service is inactive")

except KeyboardInterrupt:
    # Gracefully handle manual termination (Ctrl+C) without leaving background processes hanging.
    print("\nScan cancelled by user. Exiting.")
    sys.exit(0)
```

---

## Future Enhancements

Software applications are continuously improved. The following features are planned to expand the capabilities and performance of this tool as my programming skills advance:

1.  **Multithreading:** Adding concurrent execution so the program can check multiple ports at the exact same time, reducing scan times significantly.
2.  **Service Identification (Banner Grabbing):** Allowing the scanner to not only see if a port is open, but actually identify what specific software is running on it (e.g., detecting if port 80 is running Apache or Nginx).
3.  **Command Line Interface (CLI):** Updating the code to accept terminal arguments (like `-p` for custom port ranges or `-t` for the target IP), so users don't have to hardcode the IP address into the script every time.

---

## Conclusion

This Simple Python Port Scanner serves as a practical demonstration of core networking concepts and Python system programming. By leveraging native socket operations, managing system resources responsibly, and prioritizing clean exception handling, the project provides a reliable, lightweight tool for local network auditing. It successfully establishes a solid coding foundation for building more complex, highly scalable computer science applications in the future.

<br>

<div align="center">
  <em>Developed by SuryanshOps</em>
</div>
