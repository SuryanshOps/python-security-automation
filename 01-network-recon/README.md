# Simple Python Port Scanner (SPPS)

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)

## Table of Contents
1. [Project Overview](#project-overview)
2. [Important Legal Disclaimer](#important-legal-disclaimer)
3. [Features](#features)
4. [Prerequisites & Requirements](#prerequisites--requirements)
5. [Installation Guide](#installation-guide)
6. [Usage Instructions](#usage-instructions)
7. [Architecture & Technical Deep Dive](#architecture--technical-deep-dive)
    - [The OSI Model & Transport Layer](#the-osi-model--transport-layer)
    - [The TCP Three-Way Handshake](#the-tcp-three-way-handshake)
    - [Socket Programming in Python](#socket-programming-in-python)
8. [Code Breakdown](#code-breakdown)
9. [Security Considerations](#security-considerations)
10. [Roadmap & Future Enhancements](#roadmap--future-enhancements)
11. [Contributing](#contributing)
12. [License](#license)

---

## Project Overview

The **Simple Python Port Scanner (SPPS)** is a lightweight, dependency-free network utility designed to identify open TCP ports on a target host. Built entirely using Python's standard library, this project serves as both a functional network diagnostic tool and an educational resource for understanding foundational networking concepts, socket programming, and system-level I/O operations.

By default, the scanner is configured to audit the local loopback address (`127.0.0.1`) against a predefined list of commonly targeted ports (FTP, SSH, HTTP, HTTPS, and HTTP-Alternate). It gracefully handles connection timeouts and user interrupts, ensuring a clean and stable execution environment.

---

## Important Legal Disclaimer

**🚨 READ BEFORE USE 🚨**

This tool is provided strictly for **educational purposes and authorized auditing only**. 

Port scanning is a technique used to identify open doors into a network or computer system. Scanning networks or hosts without explicit, written permission from the network owner is illegal in many jurisdictions and may be interpreted as a malicious attack or a precursor to unauthorized access. 

The author(s) and contributor(s) of this repository assume no liability and are not responsible for any misuse, damage, or legal consequences caused by this tool. **Never point this tool at a target you do not own or have explicit authorization to test.**

---

## Features

- **Zero Dependencies:** Relies purely on Python's built-in `socket` and `sys` modules. No need for `pip install` or virtual environments.
- **TCP Connect Scanning:** Utilizes full TCP three-way handshakes to accurately determine port states.
- **Non-Crashing Error Handling:** Uses `connect_ex` instead of `connect` to return C-style error codes rather than throwing unhandled exceptions.
- **Configurable Timeouts:** Implements a strict 1-second timeout per port to prevent the application from hanging indefinitely on stealth-filtered or drop-configured firewalls.
- **Graceful Interruptions:** Safely catches `KeyboardInterrupt` (Ctrl+C) to allow users to abort scans mid-flight without leaving hanging background processes.

---

## Prerequisites & Requirements

Because SPPS is built using standard libraries, the barrier to entry is extremely low.

- **Operating System:** Compatible with any OS capable of running Python (Windows, macOS, Linux, BSD).
- **Python Version:** Python 3.6 or higher is required (due to the use of f-strings for terminal output).
- **Network Permissions:** To scan `localhost`, standard user privileges are sufficient. Note that scanning low-numbered ports (under 1024) on external networks using raw sockets sometimes requires elevated privileges depending on the OS, but standard TCP connect scans generally do not.

---

## Installation Guide

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/yourusername/simple-port-scanner.git](https://github.com/yourusername/simple-port-scanner.git)
   cd simple-port-scanner
   ```

2. **Verify Python Installation:**
   Ensure you have a compatible version of Python installed.
   ```bash
   python3 --version
   ```

3. **No additional installation required:** 
   You are ready to run the script.

---

## Usage Instructions

To execute the default scan against your local machine:

```bash
python3 port_scanner.py
```

### Expected Output

If you have a local web server (like Apache or Nginx) running on port 80, but no FTP or SSH servers active, your output will look like this:

```text
Scanning target: 127.0.0.1
------------------------------
Port 21: Closed - Service is inactive
Port 22: Closed - Service is inactive
Port 80: OPEN - This protocol service is actively running right now
Port 443: Closed - Service is inactive
Port 8080: Closed - Service is inactive
```

To stop a scan while it is running, simply press `Ctrl + C`.

```text
Scan cancelled by user. Exiting.
```

---

## Architecture & Technical Deep Dive

To fully appreciate how this simple script works, it is essential to understand the networking architecture it interacts with.

### The OSI Model & Transport Layer
This scanner operates primarily at **Layer 4 (The Transport Layer)** of the OSI (Open Systems Interconnection) model. The Transport Layer is responsible for end-to-end communication and error recovery. We are specifically utilizing **TCP (Transmission Control Protocol)**, which is a connection-oriented protocol ensuring reliable data delivery.

### The TCP Three-Way Handshake
When the scanner checks a port, it does not simply send a ping. It attempts to establish a formal TCP connection. This involves a three-step process:

1. **SYN (Synchronize):** Our scanner sends a SYN packet to the target IP and Port, effectively asking, "Are you open and accepting connections?"
2. **SYN-ACK (Synchronize-Acknowledge):** If a service is actively listening on that port (e.g., an Apache server), it replies with a SYN-ACK packet, saying, "Yes, I am open, let's connect."
3. **ACK (Acknowledge):** Our system automatically responds with an ACK packet, completing the connection.

*Note: If the port is closed, the target machine responds with an **RST (Reset)** packet in step 2. If the port is filtered by a firewall, the packet is simply dropped, and our scanner relies on the 1-second timeout to realize the port is unresponsive.*

### Socket Programming in Python
A "socket" is one endpoint of a two-way communication link between two programs running on the network. 
- `AF_INET`: This specifies the Address Family. `AF_INET` dictates that we are using IPv4 addressing (e.g., `192.168.1.1`).
- `SOCK_STREAM`: This dictates the socket type. `SOCK_STREAM` specifies that we are creating a TCP socket. (If we were making a UDP scanner, we would use `SOCK_DGRAM`).

---

## Code Breakdown

Here is a detailed explanation of the core logic powering the scanner:

```python
# Context manager 'with' ensures the socket is properly closed after use, 
# freeing up system file descriptors and preventing memory leaks.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # 1.0 second timeout. Without this, a firewall silently dropping packets 
    # would cause the default OS timeout to trigger, which can take up to 2 minutes per port.
    s.settimeout(1.0)
    
    # connect_ex is a crucial design choice. 
    # standard s.connect() throws a blocking exception (ConnectionRefusedError) if closed.
    # s.connect_ex() returns a C-level integer indicator. 0 means success.
    result = s.connect_ex((TARGET_HOST, port))
    
    if result == 0:
        print(f"Port {port}: OPEN - This protocol service is actively running right now")
```

---

## Security Considerations

### Detection by Target
Because this script uses a full TCP Connect method (`connect_ex`), it is a very "loud" type of scan. 
- The full three-way handshake is completed.
- Because the connection is completed, the target service (like a web server) will likely log the connection attempt in its access or error logs.
- Intrusion Detection Systems (IDS) and firewalls will easily flag this activity if deployed across a wide range of ports.

### Concurrency Limits
Currently, the script is single-threaded. It iterates through `PORTS_TO_SCAN` one by one. If a firewall drops packets and triggers the 1-second timeout on every port, scanning 1,000 ports would take 1,000 seconds (~16 minutes). This is a limitation designed for simplicity and safety, but it makes the scanner unsuited for large-scale enterprise network mapping.

---

## Roadmap & Future Enhancements

While currently designed for simplicity, the project architecture allows for several advanced features to be implemented in the future:

1. **Command Line Interface (CLI) Arguments:**
   Integrate Python's `argparse` module to allow users to specify targets and ports dynamically via the terminal (e.g., `python port_scanner.py -t 192.168.1.5 -p 1-1000`).

2. **Multithreading for Speed:**
   Implement `concurrent.futures.ThreadPoolExecutor` to scan dozens of ports simultaneously, reducing scan times for large port ranges from minutes to seconds.

3. **Service Banner Grabbing:**
   Once a port is identified as open, the scanner could send a basic payload and read the initial bytes returned to identify the exact software and version running on that port (e.g., identifying `OpenSSH 8.2p1`).

4. **Port Number to Service Mapping:**
   Implement a dictionary lookup to translate port numbers to their common names (e.g., mapping port `22` to output `SSH` dynamically rather than just `22`).

---

## Contributing

Contributions are welcome! Whether you are a beginner looking to make your first open-source pull request or an expert wanting to add multithreading, your help is appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 styling guidelines and includes appropriate comments explaining complex network logic.

---

## License

Distributed under the MIT License. See `LICENSE.md` for more information.
