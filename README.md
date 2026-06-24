# 🎯 Brute-Forcer: Multi-Threaded Brute Force Engine

A professional-grade, multi-threaded brute force engine featuring a live, Rich-powered terminal dashboard. This utility is designed strictly for authorized penetration testing, administrative auditing, and security assessments within isolated laboratory environments.

---

## ✨ Features

* **Multi-Threaded Architecture:** Configurable worker pool for concurrent authentication attempts to maximize I/O throughput.
* **Protocol Support:** Out-of-the-box support for SSH, FTP, HTTP Basic Auth, and HTTP Form-based logins.
* **Live Dashboard:** Real-time metrics displayed via the `Rich` library, tracking attempts, processing rate, overall progress, and the active credential pair.
* **Color-Coded Status System:** Standardized terminal indicators for quick analysis:
  * `[+]` Success / Status update
  * `[-]` Informational telemetry
  * `[!]` Critical errors or network dropouts
  * `[!!!]` Valid credentials discovered
* **ASCII Startup Banner:** Clean, distinct command-line branding on initialization.
* **Rate Limiting:** Configurable sleep delays between authentication attempts to prevent resource exhaustion or Denial of Service (DoS) conditions on target systems.
* **Early Exit Framework:** Intelligent thread synchronization that immediately stops all background operations the moment a valid credential pair is verified.
* **Extensible Design:** Modular architecture allowing developers to easily integrate new protocols by implementing a single connection method.
* **UI/Logic Separation:** Complete decoupling of network input/output functions from visual presentation components for easy long-term maintenance.

---
### Dashbaord
<img width="935" height="608" alt="Screenshot 2026-06-24 at 20 32 12" src="https://github.com/user-attachments/assets/31e11eb3-28ae-4150-ad9d-cd5f3e6aa5b9" />

<img width="1238" height="634" alt="Screenshot 2026-06-24 at 20 30 59" src="https://github.com/user-attachments/assets/a8aeb619-712a-4c99-8fe8-9b4cd8d0faac" />

## 🛠️ Requirements & Dependencies

* Python 3.8+
* Kali Linux (recommended) or any Debian-based Linux distribution

### Executable Commands
# SSH Assessment — 20 concurrent threads
python3 thread.py 192.168.1.100 -p 22 --protocol ssh \
    -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt \
    -P /usr/share/wordlists/rockyou.txt \
    -t 20

# FTP Assessment — Rate-limited enforcement
python3 thread.py 192.168.1.100 -p 21 --protocol ftp \
    -U users.txt \
    -P passwords.txt \
    -t 10 --delay 0.5

# HTTP Basic Authentication — Low-density validation
python3 thread.py 192.168.1.100 -p 8080 --protocol http_basic \
    -U admin_users.txt \
    -P common_passwords.txt \
    -t 5

# HTTP Form-Based Authentication
python3 thread.py 192.168.1.100 -p 80 --protocol http_form \
    -U users.txt \
    -P rockyou.txt \
    -t 8

### Installation

Clone the repository and install the necessary system or Python packages:

```bash
# Clone the repository
git clone [https://github.com/yourusername/brute-forcer.git](https://github.com/yourusername/brute-forcer.git)
cd brute-forcer

# Option A: Install via Python package manager
pip3 install rich requests paramiko

# Option B: Install via native package manager (Kali/Debian systems)
sudo apt update
sudo apt install python3-rich python3-requests python3-paramiko -y

### ⚙️ Operational Boundaries & Limitations
Memory Usage: The engine instantiates credential permutations within an active structural matrix during launch setup. Avoid cross-joining massive username arrays against high-density password files simultaneously on memory-constrained systems.
Network Layers: Standard deployment configurations lack internal SOCKS/Proxy routing mechanisms.
Persistence: Application flows do not include mid-session state recovery or execution breakpoint serialization features.
HTTP Forms: Form-based validation requires programmatic modification to match target-specific input fields, parameter shapes, and validation indicators.

### ⚠️ Legal & Ethical Usage Disclaimer
This tool is intended strictly for authorized security testing and educational research environments only. Running automated authentication sweeps against targets without explicit, prior written permission from the asset owner is unauthorized, highly dangerous, and strictly illegal. The authors assume absolutely no liability and are not responsible for any downstream misuse, security incidents, or damage caused by this utility suite.

### 📄 License
This project is licensed under the terms of the MIT License.

