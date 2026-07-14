import os
import sys
import time
import subprocess
import requests
from datetime import datetime

GITHUB_USER = "MILKAA-55"
GITHUB_REPO = "trash-autonomous"
BRANCH = "main"
VERSION_FILE = ".trash_version"

RESET   = "\033[0m"
BOLD    = "\033[1m"
ACCENT  = "\033[38;5;69m"   # bleu
GREEN   = "\033[38;5;78m"
YELLOW  = "\033[38;5;221m"
RED     = "\033[38;5;203m"
TEXT    = "\033[38;5;253m"
DIM     = "\033[38;5;240m"

COLORS = {
    "info": TEXT,
    "success": GREEN,
    "warning": YELLOW,
    "error": RED,
    "dim": DIM,
    "accent": ACCENT,
}


class Updater:
    def __init__(self):
        self._updating = False

    def log_print(self, message: str, level: str = "info"):
        ts = datetime.now().strftime("%H:%M:%S")
        color = COLORS.get(level, TEXT)
        print(f"{DIM}[{ts}]{RESET} {color}{message}{RESET}")

    def print_status(self, text: str, level: str = "info"):
        color = COLORS.get(level, TEXT)
        print(f"{color}{BOLD}● {text}{RESET}")

    def start_progress(self):
        self._updating = True
        self.print_status("Updating...", "warning")

    def stop_progress(self, success: bool = True):
        self._updating = False
        if success:
            self.print_status("Updated", "success")
        else:
            self.print_status("Error", "error")

    def get_remote_sha(self):
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/commits/{BRANCH}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.json()["sha"]
        except Exception as e:
            self.log_print(f"Unable to contact GitHub: {e}", "error")
            return None

    def get_local_sha(self):
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE) as f:
                return f.read().strip()
        return None

    def save_sha(self, sha):
        with open(VERSION_FILE, "w") as f:
            f.write(sha)

    def pull_updates(self):
        result = subprocess.run(
            ["git", "pull", "origin", BRANCH],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            for line in result.stdout.strip().splitlines():
                self.log_print(line, "accent")
            return True
        else:
            for line in result.stderr.strip().splitlines():
                self.log_print(line, "error")
            return False

    def update_loop(self):
        self.log_print("Check for updates...", "dim")
        remote = self.get_remote_sha()
        local = self.get_local_sha()

        if remote is None:
            self.log_print("Cannot reach GitHub. Skipping update.", "warning")
            return

        if remote == local:
            self.log_print(f"No updates. (SHA: {remote[:7]})", "success")
            return

        self.log_print(f"New commit detected! ({remote[:7]})", "warning")
        self.start_progress()
        ok = self.pull_updates()
        if ok:
            self.save_sha(remote)
            self.log_print("Update successful ✓", "success")
            self.stop_progress(True)
            time.sleep(1)
            self.log_print("Reboot of the Trash...", "accent")
            time.sleep(1)
            os.execv(sys.executable, [sys.executable] + sys.argv + ["--skip-boot"])
        else:
            self.log_print("Update failure.", "error")
            self.stop_progress(False)

    def run(self):
        self.log_print("The Trash Autonomous Updater started.", "accent")
        self.log_print(f"Repo watched: {GITHUB_USER}/{GITHUB_REPO} ({BRANCH})", "dim")
        self.update_loop()


def show_updater():
    Updater().run()


if __name__ == "__main__":
    Updater().run()
