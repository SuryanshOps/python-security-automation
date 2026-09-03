# Simple Log Analyzer (SLA)

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Concept](https://img.shields.io/badge/concept-Cybersecurity_Defense-purple.svg) ![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Academic Integrity & Defensive Ethics](#academic-integrity--defensive-ethics)
3. [Technical Architecture & Data Structure](#technical-architecture--data-structure)
4. [Engineering Analysis & Trade-offs](#engineering-analysis--trade-offs)
5. [Installation & Execution](#installation--execution)
6. [Source Code Implementation](#source-code-implementation)
7. [Future Enhancements](#future-enhancements)
8. [Conclusion](#conclusion)

---

## Executive Summary

The **Simple Log Analyzer (SLA)** is a lightweight, dependency-free Python utility designed to parse Linux system authentication logs (`auth.log`) and extract the IP addresses of malicious actors attempting unauthorized SSH access. 

Built entirely using Python's standard library, this project serves as a practical application of foundational computer science concepts, specifically focusing on memory-efficient file I/O operations, unstructured data parsing, array manipulation, and defensive cybersecurity (Blue Team) operations.

---

## Academic Integrity & Defensive Ethics

> **Note on Cybersecurity Context:** 
> Unlike offensive security tools, this script represents a **Defensive (Blue Team)** engineering approach. In the real world, scripts like this form the underlying logic for Intrusion Prevention Systems (IPS) like *Fail2Ban*. Understanding how to efficiently parse server logs to identify brute-force attacks is a critical component of building secure, resilient network infrastructure. This project was developed strictly for academic demonstration and local log analysis.

---

## Technical Architecture & Data Structure

### 1. The Syslog Data Format
Linux operating systems write authentication events to unstructured text files. To extract data, the script must understand the syntax of both successful and unsuccessful login attempts:

*   **Successful Login:** `Feb 23 12:10:05 server sshd: Accepted password for james from 192.168.1.50 port 54321 ssh2`
*   **Failed Login:** `Feb 23 12:05:22 server sshd: Failed password for root from 203.0.113.5 port 49211 ssh2`

### 2. The "Anchor Point" Parsing Algorithm
Because unstructured log data has variable lengths (e.g., the username `root` is 4 characters, while `administrator` is 13), hardcoding exact character positions (string slicing) will fail. 

Instead, the script utilizes an **Anchor Point Strategy**:
1.  **Tokenization:** The script uses `.split()` to convert the unstructured string into a structured Array (List) of individual words separated by whitespace.
2.  **Pivot Indexing:** By identifying the static keyword `"from"` (which the OS always places immediately before the IP address), the script determines its exact index position in the array.
3.  **Extraction:** By calculating `index + 1`, the script dynamically guarantees it captures the raw IP address, regardless of how long the username or date strings were.

---

## Engineering Analysis & Trade-offs

### Space Complexity & Memory Management ($O(1)$ Space)
A critical engineering decision in this script is how the file is read. Standard Python methods like `file.read()` or `file.readlines()` load the *entire* file into the system's RAM (Random Access Memory) at once. If an `auth.log` file grows to several gigabytes due to a massive botnet attack, loading it entirely would crash the program and exhaust system memory (an $O(N)$ space complexity).

**The Solution:** The script uses the iterator `for line in file:`. This creates a streaming data pipeline that only loads **one single line of text into RAM at a time**, processes it, and then discards it. This results in a highly efficient **$O(1)$ Space Complexity**, allowing the script to parse infinitely large log files without ever crashing.

### Resource Management (The `with` Statement)
Operating systems impose strict limits on open file descriptors. The script wraps the file operation in a Python context manager (`with open(...) as file:`). This guarantees that the operating system instantly closes the file and releases the memory lock the moment the loop finishes, even if an unexpected error occurs during runtime.

### Exception Handling 
If a system administrator runs this script on a machine that does not have an `auth.log` file, a standard script would throw a terminal-breaking `Traceback` crash. By wrapping the I/O request in a `try / except FileNotFoundError` block, the script gracefully handles missing data and provides a human-readable error instruction instead.

---

## Installation & Execution

This project requires **Python 3.6+** (for f-string formatting). No external libraries are required.

**1. Clone the repository & create a dummy log file:**
```bash
git clone https://github.com/SuryanshOps/python-security-automation.git
cd python-security-automation
cd 02-log-forensics
cd simple-log-analyzer

# Create a sample log file to test the script
echo "Feb 23 12:05:22 server sshd: Failed password for root from 203.0.113.5 port 49211 ssh2" > auth.log
echo "Feb 23 12:10:05 server sshd: Accepted password for james from 192.168.1.50 port 54321 ssh2" >> auth.log
echo "Feb 23 12:15:10 server sshd: Failed password for admin from 198.51.100.22 port 33211 ssh2" >> auth.log
```

**2. Execute the script:**
```bash
python3 auth-log-parser.py
```

**Example Standard Output:**
```text
Parsing log file: auth.log
----------------------------------------
Suspicious IP Found: 203.0.113.5
Suspicious IP Found: 198.51.100.22
```
*(Notice how the script automatically ignored the successful login from 192.168.1.50)*

---

## Source Code Implementation

```python
LOG_FILE = "auth.log"

print(f"Parsing log file: {LOG_FILE}\n" + "-" * 40)

try:
    # open up the log file to read it
    # 'with' handles closing the file automatically so we don't leak system memory
    with open(LOG_FILE, "r") as file:
        
        # loop through the text file line by line 
        # this stops the script from loading a massive file all at once and crashing (O(1) space)
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
            # Our filter strictly looks for "Failed password", so it skips all successful entries
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
```

---

## Future Enhancements

As my understanding of computer science and software engineering grows, I plan to implement the following features to scale this utility:

1.  **Regular Expressions (Regex):** Replacing the array-indexing logic with Python's `re` module to locate IPv4 and IPv6 addresses natively. This would make the parsing engine faster and more mathematically rigorous.
2.  **Frequency Analysis (Hash Maps):** Currently, if an IP address fails 10,000 times, the script prints it 10,000 times. I plan to implement a Python Dictionary (Hash Map) to count how many times each IP appears, and only print the IP if it crosses a specific threshold (e.g., > 5 failed attempts).
3.  **Command Line Interface (CLI):** Updating the code to accept terminal arguments so users can point the script at different log files dynamically without editing the source code.

---

## Conclusion

The Simple Log Analyzer bridges the gap between basic string manipulation and practical cybersecurity defense. By prioritizing memory-efficient file streaming ($O(1)$ space complexity) and dynamic array indexing, the script demonstrates an ability to process unstructured, variable-length system data safely and reliably. It serves as a strong foundation for building more advanced, automated network defense and data-parsing algorithms in the future.

<br>

<div align="center">
  <em>Developed by SuryanshOps</em>
</div>

