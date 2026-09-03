# Cryptographic File Integrity Monitor (CFIM)

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Concept](https://img.shields.io/badge/concept-Cryptography-purple.svg) ![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Academic Integrity & Cybersecurity Context](#academic-integrity--cybersecurity-context)
3. [Technical Architecture & Theory](#technical-architecture--theory)
4. [Engineering Analysis & Trade-offs](#engineering-analysis--trade-offs)
5. [Installation & Execution](#installation--execution)
6. [Source Code Implementation](#source-code-implementation)
7. [Future Enhancements](#future-enhancements)
8. [Conclusion](#conclusion)

---

## Executive Summary

The **Cryptographic File Integrity Monitor (CFIM)** is a specialized Python utility designed to generate a unique digital fingerprint of a specific file using the SHA-256 cryptographic algorithm. 

Built using Python's standard `hashlib` library, this project serves as a practical application of Data Integrity—a core pillar of information security. By capturing a baseline hash of a critical file (like a system configuration or executable), administrators can periodically re-run the tool to detect unauthorized tampering, data corruption, or malicious modifications at the binary level.

---

## Academic Integrity & Cybersecurity Context

> **Note on the CIA Triad:** 
> In computer science and cybersecurity, the foundation of secure systems relies on the CIA Triad: Confidentiality, **Integrity**, and Availability. This project specifically implements the **Integrity** component. In professional environments, File Integrity Monitoring (FIM) is mandated by security frameworks (like PCI-DSS and HIPAA) to detect malware infections and unauthorized configuration drift. This tool was built to demonstrate a low-level understanding of how those enterprise FIM systems operate under the hood.

---

## Technical Architecture & Theory

### 1. SHA-256 and Cryptographic Hashing
This tool relies on the **Secure Hash Algorithm (SHA-256)**. Unlike encryption (which is a two-way street designed to be decrypted later), hashing is a **one-way mathematical function**. When the script passes the file's data into the algorithm, it generates a fixed-length 64-character hexadecimal string. It is mathematically impossible to reverse-engineer this 64-character string back into the original file.

### 2. The Avalanche Effect
A critical requirement for cryptographic hashing is the "Avalanche Effect." If a malicious actor opens `system_config.txt`, adds a single space at the end of the file, and saves it, the file size might remain almost identical. However, under the SHA-256 algorithm, altering even a single bit of binary data causes a cascading disruption in the mathematical calculation, resulting in an entirely unrecognizable, completely different 64-character hash. This guarantees instant proof of tampering.

---

## Engineering Analysis & Trade-offs

### I/O Design: Binary Mode (`"rb"`) vs. Text Mode (`"r"`)
A deliberate engineering choice in this script is opening the file in **Read-Binary (`"rb"`)** mode rather than standard text mode. 
*   **The Problem:** Different operating systems handle text formatting differently. For example, Windows uses `CRLF` (Carriage Return + Line Feed) for line breaks, while Linux/macOS uses `LF`. If read in text mode, Python might interpret or translate these characters, altering the data fed to the hasher and resulting in a false-positive mismatch across operating systems.
*   **The Solution:** Binary mode bypasses OS-level text formatting entirely. It reads the raw 1s and 0s directly from the physical storage disk. This guarantees that a file hashed on a Linux server will output the exact same fingerprint if transferred to a Windows machine, ensuring cross-platform reliability.

### Data Formatting: `.digest()` vs `.hexdigest()`
The `hashlib` library offers two methods to output the final cryptographic math. Both contain the exact same data, but format it for different audiences (computers vs. humans). This script explicitly uses `.hexdigest()` to ensure the output is human-readable and terminal-safe.

| Feature | `.digest()` | `.hexdigest()` (Used in this project) |
| :--- | :--- | :--- |
| **Data Type** | Raw bytes (`bytes` object) | Text string (`str` object) |
| **Visual Output** | `b'\x2c\x26\xb4\x6b\x68\xff...'` | `'2c26b46b68ff...'` |
| **Length (SHA-256)** | 32 bytes | 64 characters *(2 hex chars per byte)* |
| **Readability** | Unreadable; breaks terminal formatting with unprintable symbols | Clean, human-readable, and copy-pasteable |
| **Primary Use Case** | Storing compactly in databases, or passing to another cryptographic function | Printing to terminals, writing to log files, or manual human verification |

### Space Complexity & Memory Constraints (O(N) Space)
Currently, the script utilizes `file.read()`, which pulls the *entire* file into system RAM before feeding it to the `hasher.update()` function. 
*   **Trade-off:** For a small configuration file (like `system_config.txt`), this is fast, simple, and completely acceptable. However, if tasked with hashing a 50 GB database backup, this architecture would trigger a memory exhaustion error (RAM overflow) and crash the system. Scaling this tool for enterprise use requires addressing this memory constraint.

---

## Installation & Execution

This project requires **Python 3.6+**. No external libraries are required, as `hashlib` is natively built into Python.

**1. Clone the repository & create a dummy target file:**
```bash
git clone https://github.com/SuryanshOps/simple-file-integrity.git

cd simple-file-integrity

# Create a clean configuration file
echo "Database_Port=5432" > system_config.txt
```

**2. Execute the script to establish a baseline:**
```bash
python3 integrity_monitor.py
```
*(Note: If you are on Windows, use `python` instead of `python3`)*

*Output:*
```text
Calculating fingerprint for: system_config.txt
--------------------------------------------------
SHA-256 Fingerprint: [Your Unique 64-Character String]
```

**3. Test the Avalanche Effect:**
Open `system_config.txt`, change `5432` to `5433`, save it, and run the script again. You will see an entirely different 64-character fingerprint, proving the file was altered.

---

## Source Code Implementation

```python
import hashlib
import sys

# this points to the critical file we want to protect from being messed with
TARGET_FILE = "system_config.txt"

print(f"Calculating fingerprint for: {TARGET_FILE}\n" + "-" * 50)

try:
    # opening the file in read-binary ("rb") mode instead of standard text mode
    # reading raw bytes handles everything down to hidden spaces, OS formatting, or tabs
    with open(TARGET_FILE, "rb") as file:
        
        # initialize a completely fresh sha256 calculator from the hashlib library
        hasher = hashlib.sha256()
        
        # pull all the raw binary data (1s and 0s) out of the file
        file_bytes = file.read()
        
        # feed those raw binary bytes directly into our hashing engine
        hasher.update(file_bytes)
        
        # hexdigest finishes the math and turns the raw result into a readable 64-character text string
        file_fingerprint = hasher.hexdigest()
        
        # printing out the unique cryptographic fingerprint of the file at this exact microsecond
        print(f"SHA-256 Fingerprint: {file_fingerprint}")

# basic fallback if you run the script before actually making the system_config.txt file
except FileNotFoundError:
    print(f"Error: The file '{TARGET_FILE}' was not found. Please create it first.")
    sys.exit()
```

---

## Future Enhancements

As my understanding of computer science and software architecture deepens, I plan to expand this foundational script into a more robust monitoring daemon:

1.  **Memory-Optimized Chunking:** To solve the memory constraint mentioned in the engineering analysis, I plan to refactor `file.read()` into a `while` loop that reads the file in 4KB chunks (`file.read(4096)`). This will achieve a constant space complexity, allowing the tool to securely hash infinitely large files (like ISOs or virtual machine disks) without crashing system RAM.
2.  **Automated Baseline Verification:** Instead of manually comparing the old hash to the new hash by staring at the terminal, I plan to have the script save the initial hash into a hidden `.json` file. On subsequent runs, the script will automatically compare the current hash against the stored baseline and print a red `ALERT: TAMPERING DETECTED` or a green `VERIFIED OK` message.
3.  **Command Line Interface (CLI):** Integrating Python's `argparse` to allow users to hash any file dynamically via terminal arguments (e.g., `python3 integrity_monitor.py -f /etc/passwd`).

---

## Conclusion

The Cryptographic File Integrity Monitor bridges theoretical cryptography and applied systems engineering. By leveraging the SHA-256 algorithm, enforcing strict binary I/O handling for cross-platform stability, properly formatting data outputs for human interaction, and utilizing the mathematical properties of the Avalanche Effect, this project demonstrates a concrete understanding of how data integrity is programmatically enforced in modern computing environments. 

<br>

<div align="center">
<em>Developed by SuryanshOps</em>
</div>
