"""
Real-time file monitoring for Superthink-Code-Analyzer.
Continuously watches for file changes and triggers immediate analysis.
"""

import os
import sys
import json
import time
import fnmatch
from pathlib import Path
from typing import List, Set, Callable
from datetime import datetime


class FileMonitor:
    """Monitors file changes in real-time."""

    def __init__(self, repo_root: str = '.', config_path: str = '.superthink/config.json'):
        self.repo_root = repo_root
        self.config_path = os.path.join(repo_root, config_path)
        self.config = self._load_config()

        self.watched_files: Set[str] = set()
        self.last_check_time = {}
        self.file_hashes = {}

    def _load_config(self) -> dict:
        """Load configuration from JSON."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {self.config_path}")
            return {'file_patterns': {'monitor': ['src/**/*.py'], 'ignore': []}}

    def get_monitored_patterns(self) -> List[str]:
        """Get file patterns to monitor."""
        return self.config.get('file_patterns', {}).get('monitor', ['src/**/*.py'])

    def get_ignore_patterns(self) -> List[str]:
        """Get patterns to ignore."""
        return self.config.get('file_patterns', {}).get('ignore', [])

    def should_monitor_file(self, file_path: str) -> bool:
        """Check if file should be monitored."""
        # Check ignore patterns first
        for ignore_pattern in self.get_ignore_patterns():
            if fnmatch.fnmatch(file_path, ignore_pattern):
                return False

        # Check if matches any monitor pattern
        for monitor_pattern in self.get_monitored_patterns():
            if fnmatch.fnmatch(file_path, monitor_pattern):
                return True

        return False

    def discover_files(self) -> Set[str]:
        """Discover all files to monitor."""
        monitored = set()

        for root, dirs, files in os.walk(self.repo_root):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.repo_root)

                if self.should_monitor_file(rel_path):
                    monitored.add(file_path)

        return monitored

    def get_file_hash(self, file_path: str) -> str:
        """Get hash of file content (simple version)."""
        try:
            with open(file_path, 'rb') as f:
                import hashlib
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def check_for_changes(self) -> List[str]:
        """Check which files have changed since last check."""
        changed_files = []

        # Get current files
        current_files = self.discover_files()

        # Check for new or modified files
        for file_path in current_files:
            current_hash = self.get_file_hash(file_path)

            if file_path not in self.file_hashes:
                # New file
                changed_files.append(file_path)
                self.file_hashes[file_path] = current_hash
            elif self.file_hashes[file_path] != current_hash:
                # Modified file
                changed_files.append(file_path)
                self.file_hashes[file_path] = current_hash

        # Check for deleted files
        deleted_files = set(self.file_hashes.keys()) - current_files
        for file_path in deleted_files:
            del self.file_hashes[file_path]

        return changed_files

    def start_monitoring(self, on_change_callback: Callable, check_interval: int = 2):
        """Start continuous monitoring loop."""
        print(f"🔍 Superthink Real-Time Monitor started")
        print(f"   Watching: {self.get_monitored_patterns()}")
        print(f"   Check interval: {check_interval}s")
        print(f"   Press Ctrl+C to stop\n")

        # Initial discovery
        self.file_hashes = {
            f: self.get_file_hash(f) for f in self.discover_files()
        }
        print(f"✅ Monitoring {len(self.file_hashes)} files\n")

        try:
            while True:
                time.sleep(check_interval)

                # Check for changes
                changed_files = self.check_for_changes()

                if changed_files:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Detected {len(changed_files)} change(s):")
                    for file_path in changed_files:
                        print(f"  📝 {os.path.relpath(file_path, self.repo_root)}")

                    # Trigger callback
                    if on_change_callback:
                        on_change_callback(changed_files)

                    print()

        except KeyboardInterrupt:
            print("\n⏹️  Monitor stopped")

    def get_file_content(self, file_path: str) -> str:
        """Read file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def print_file_status(self):
        """Print status of monitored files."""
        print("\n" + "=" * 70)
        print("SUPERTHINK FILE MONITOR STATUS")
        print("=" * 70)
        print(f"Repository root: {self.repo_root}")
        print(f"Monitored files: {len(self.file_hashes)}")
        print(f"Last check: {datetime.now().isoformat()}")

        if self.file_hashes:
            print("\nMonitored files:")
            for file_path in sorted(self.file_hashes.keys())[:10]:
                rel_path = os.path.relpath(file_path, self.repo_root)
                print(f"  ✅ {rel_path}")

            if len(self.file_hashes) > 10:
                print(f"  ... and {len(self.file_hashes) - 10} more")

        print("=" * 70 + "\n")


def create_monitor(repo_root: str = '.') -> FileMonitor:
    """Factory function to create a FileMonitor."""
    return FileMonitor(repo_root)


# Example usage and testing
if __name__ == '__main__':
    # For testing: basic monitor that just prints changes
    def on_change(changed_files):
        print(f"  → Would analyze {len(changed_files)} file(s)")
        for f in changed_files:
            print(f"    - {f}")

    monitor = create_monitor('.')
    monitor.print_file_status()

    # Uncomment to start monitoring:
    # monitor.start_monitoring(on_change_callback=on_change)
