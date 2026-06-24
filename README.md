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

## 🛠️ Requirements & Dependencies

* Python 3.8+
* Kali Linux (recommended) or any Debian-based Linux distribution

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

<img width="935" height="608" alt="Screenshot 2026-06-24 at 20 32 12" src="https://github.com/user-attachments/assets/43782329-5901-4949-bed7-fe3d2b97dc6d" />

<img width="1238" height="634" alt="Screenshot 2026-06-24 at 20 30 59" src="https://github.com/user-attachments/assets/d1c797f5-1e64-4ecb-913c-5fed13028996" />


