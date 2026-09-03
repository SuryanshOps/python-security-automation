# Simple Python Port Scanner (SPPS)

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Concept](https://img.shields.io/badge/concept-Network_Engineering-purple.svg) ![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Academic Integrity & Ethics](#academic-integrity--ethics)
3. [Technical Architecture](#technical-architecture)
4. [Engineering Analysis & Trade-offs](#engineering-analysis--trade-offs)
5. [Installation & Execution](#installation--execution)
6. [Source Code Implementation](#source-code-implementation)
7. [Future Development Scope](#future-development-scope)

---

## Executive Summary

The **Simple Python Port Scanner (SPPS)** is a lightweight, dependency-free network utility designed to identify open TCP ports on a host system. Built entirely using Python's standard library, this project serves as a practical application of computer science concepts, specifically focusing on network engineering, socket programming, and system-level I/O operations. 

By avoiding third-party libraries, the project demonstrates a foundational understanding of how operating systems handle network traffic and resource allocation at the socket level.

---

## Academic Integrity & Ethics

> **Note on Ethical Usage:** 
> This tool was developed strictly for **educational purposes, local environment testing, and academic demonstration**. In the field of computer science, understanding network auditing is essential for building robust, secure systems. However, scanning external networks without explicit, written authorization is a violation of ethical computing standards. This script is configured by default to safely target only the local loopback environment (`127.0.0.1`).

---

## Technical Architecture

### 1. Transport Layer Operations (Layer 4)
This application operates at the Transport Layer of the OSI (Open Systems Interconnection) model. It utilizes the **Transmission Control Protocol (TCP)**, which is connection-oriented and guarantees the delivery and correct ordering of data packets.

### 2. The TCP Three-Way Handshake
To determine the state of a network service, the script initiates a stateful connection rather than a simple ICMP ping. The underlying operating system handles the following sequence:

| Step | Packet | Sender | Description |
| :--- | :--- | :--- | :--- |
| **1** | `SYN` | Scanner | Requests to synchronize and open a connection to the target port. |
| **2** | `SYN-ACK` | Target | If the port is open, the target acknowledges the request. *(If closed, returns `RST`)* |
| **3** | `ACK` | Scanner | Acknowledges the target's response, completing the connection. |

### 3. Socket Programming Interface
The script interfaces with the OS network stack using Berkeley-style sockets:
*   `AF_INET`: Configures the socket to route over IPv4 addressing architecture.
*   `SOCK_STREAM`: Instructs the operating system to instantiate a TCP socket and natively manage the three-way handshake sequence.

---

## Engineering Analysis & Trade-offs

### Time Complexity & Performance
In its current iteration, the application processes ports sequentially in a single thread, resulting in a time complexity of **$O(n)$**, where *n* is the number of ports scanned. 
*   **The Firewall Problem:** If a network firewall drops packets silently, the scanner must wait for the connection attempt to time out. 
*   **The Solution:** A strict `1.0` second timeout is enforced via `s.settimeout(1.0)`. While this prevents indefinite hanging, scanning 1,000 silently dropped ports still takes ~16 minutes. This highlights the architectural necessity of concurrent programming for network-bound I/O tasks.

### Connection Method: `connect_ex()` vs Raw Sockets
The script utilizes the `connect_ex()` method instead of standard raw sockets.
*   **Advantage (Safety & Portability):** It does not require elevated (root/administrator) privileges to execute, ensuring the script runs safely in standard user-space across Windows, macOS, and Linux. Furthermore, it returns a C-level integer status code (0 for success) rather than raising blocking exceptions, allowing for cleaner control flow.
*   **Trade-off:** Because it completes a full TCP connection, it generates standard connection logs on the target server, making it less stealthy than raw-socket SYN scanning.

---

## Installation & Execution

This project requires **Python 3.6+** (for f-string formatting support). No external dependencies or virtual environments are required.

**1. Clone the repository:**
```bash
git clone [https://github.com/yourusername/simple-port-scanner.git](https://github.com/yourusername/simple-port-scanner.git)
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

## Future Development Scope

As part of my ongoing academic progression, I intend to refactor this architecture to incorporate more advanced computer science paradigms:

1.  **Asynchronous Concurrency (Multithreading):** Implementing `concurrent.futures.ThreadPoolExecutor` to unblock network I/O wait times, processing multiple sockets concurrently to reduce large-scale scan times from minutes to seconds.
2.  **Application Layer (Layer 7) Analysis:** Extending functionality to send basic protocol-specific payloads (e.g., HTTP `GET` requests) to open ports, analyzing the returned byte stream to identify the underlying software daemon and version.
3.  **Dynamic CLI Integration:** Integrating Python's `argparse` module to parameterize target IPs, port ranges, and timeout lengths dynamically at runtime.
