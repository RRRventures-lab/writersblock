"""
Auto-fix engine for Superthink-Code-Analyzer.
Autonomously fixes detected issues and logs all changes.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import subprocess


class Fix:
    """Represents a code fix operation."""

    def __init__(
        self,
        file_path: str,
        line_number: int,
        issue_type: str,
        original_content: str,
        fixed_content: str,
        severity: str,
    ):
        self.file_path = file_path
        self.line_number = line_number
        self.issue_type = issue_type
        self.original_content = original_content
        self.fixed_content = fixed_content
        self.severity = severity
        self.timestamp = datetime.now().isoformat()
        self.success = False
        self.error_message = None

    def to_dict(self) -> Dict:
        """Convert fix to dictionary for logging."""
        return {
            'timestamp': self.timestamp,
            'file': self.file_path,
            'line': self.line_number,
            'type': self.issue_type,
            'severity': self.severity,
            'original': self.original_content[:100],
            'fixed': self.fixed_content[:100],
            'success': self.success,
            'error': self.error_message,
        }


class AutoFixer:
    """Autonomously fixes code issues."""

    def __init__(self, repo_root: str = '.'):
        self.repo_root = repo_root
        self.log_path = os.path.join(repo_root, '.superthink', 'fixes.log')
        self.metrics_path = os.path.join(repo_root, '.superthink', 'metrics.json')
        self.fixes_applied = []
        self.load_existing_log()

    def load_existing_log(self):
        """Load existing fixes log."""
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                try:
                    self.fixes_applied = json.load(f)
                except json.JSONDecodeError:
                    self.fixes_applied = []

    def fix_hardcoded_api_key(
        self,
        file_path: str,
        line_number: int,
        key_name: str,
        original_line: str,
    ) -> Optional[Fix]:
        """Fix hardcoded API key by moving to environment variable."""
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Read file
            with open(file_path, 'r') as f:
                lines = f.readlines()

            if line_number > len(lines):
                raise IndexError(f"Line {line_number} exceeds file length")

            # Get original line
            original = lines[line_number - 1]
            indent = len(original) - len(original.lstrip())
            indent_str = original[:indent]

            # Generate fixed line
            fixed = f"{indent_str}{key_name} = os.getenv('{key_name}')\n"

            # Add import if needed
            if 'import os' not in ''.join(lines[:10]):
                lines.insert(0, 'import os\n')
                line_number += 1  # Adjust line number after import

            # Replace line
            lines[line_number - 1] = fixed

            # Write back
            with open(file_path, 'w') as f:
                f.writelines(lines)

            # Create fix record
            fix = Fix(
                file_path=file_path,
                line_number=line_number,
                issue_type='hardcoded_api_key',
                original_content=original.strip(),
                fixed_content=fixed.strip(),
                severity='critical',
            )
            fix.success = True
            return fix

        except Exception as e:
            fix = Fix(
                file_path=file_path,
                line_number=line_number,
                issue_type='hardcoded_api_key',
                original_content=original_line,
                fixed_content='',
                severity='critical',
            )
            fix.error_message = str(e)
            return fix

    def fix_missing_type_hints(self, file_path: str) -> List[Fix]:
        """Add missing type hints to functions."""
        fixes = []
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            fixed_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                fixed_lines.append(line)

                # Detect function definitions
                if line.strip().startswith('def ') and ':' in line:
                    # Check if it already has type hints
                    if '->' not in line:
                        # Simple case: no return type hint
                        if line.strip().endswith(':'):
                            # Add basic type hint
                            base_line = line.rstrip().rstrip(':')
                            fixed_line = f"{base_line} -> None:\n"
                            fixed_lines[-1] = fixed_line

                            fix = Fix(
                                file_path=file_path,
                                line_number=i + 1,
                                issue_type='missing_type_hint',
                                original_content=line.strip(),
                                fixed_content=fixed_line.strip(),
                                severity='low',
                            )
                            fix.success = True
                            fixes.append(fix)

                i += 1

            # Write back if any fixes applied
            if fixes:
                with open(file_path, 'w') as f:
                    f.writelines(fixed_lines)

        except Exception as e:
            fix = Fix(
                file_path=file_path,
                line_number=0,
                issue_type='missing_type_hint',
                original_content='',
                fixed_content='',
                severity='low',
            )
            fix.error_message = str(e)
            fixes.append(fix)

        return fixes

    def create_git_commit(self, fixes: List[Fix]) -> bool:
        """Create a git commit for auto-fixes."""
        try:
            if not fixes:
                return True

            # Stage all fixed files
            fixed_files = set(f.file_path for f in fixes if f.success)
            for file_path in fixed_files:
                subprocess.run(['git', 'add', file_path], cwd=self.repo_root, check=True)

            # Create commit message
            critical_count = sum(1 for f in fixes if f.severity == 'critical' and f.success)
            high_count = sum(1 for f in fixes if f.severity == 'high' and f.success)
            other_count = sum(1 for f in fixes if f.severity not in ['critical', 'high'] and f.success)

            commit_msg = f"""fix: Apply Superthink auto-fixes

Applied {len([f for f in fixes if f.success])} automated fixes:
- {critical_count} critical issues
- {high_count} high priority issues
- {other_count} other issues

Generated by Superthink-Code-Analyzer
"""

            subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=self.repo_root,
                check=True,
            )

            return True

        except subprocess.CalledProcessError as e:
            print(f"Git commit failed: {e}")
            return False

    def log_fixes(self, fixes: List[Fix]):
        """Log all fixes to audit trail."""
        self.fixes_applied.extend([f.to_dict() for f in fixes])

        # Write to file
        with open(self.log_path, 'w') as f:
            json.dump(self.fixes_applied, f, indent=2)

        # Update metrics
        self._update_metrics(fixes)

    def _update_metrics(self, fixes: List[Fix]):
        """Update code quality metrics."""
        try:
            if os.path.exists(self.metrics_path):
                with open(self.metrics_path, 'r') as f:
                    metrics = json.load(f)
            else:
                metrics = {
                    'total_fixes': 0,
                    'successful_fixes': 0,
                    'failed_fixes': 0,
                    'by_type': {},
                    'by_severity': {},
                }

            # Update metrics
            metrics['total_fixes'] += len(fixes)
            metrics['successful_fixes'] += sum(1 for f in fixes if f.success)
            metrics['failed_fixes'] += sum(1 for f in fixes if not f.success)

            # By type
            for fix in fixes:
                if fix.issue_type not in metrics['by_type']:
                    metrics['by_type'][fix.issue_type] = 0
                if fix.success:
                    metrics['by_type'][fix.issue_type] += 1

            # By severity
            for fix in fixes:
                if fix.severity not in metrics['by_severity']:
                    metrics['by_severity'][fix.severity] = {'total': 0, 'fixed': 0}
                metrics['by_severity'][fix.severity]['total'] += 1
                if fix.success:
                    metrics['by_severity'][fix.severity]['fixed'] += 1

            metrics['last_update'] = datetime.now().isoformat()

            with open(self.metrics_path, 'w') as f:
                json.dump(metrics, f, indent=2)

        except Exception as e:
            print(f"Failed to update metrics: {e}")

    def apply_fixes(self, fixes: List[Fix]) -> Tuple[int, int]:
        """Apply a batch of fixes. Returns (successful, failed)."""
        successful = 0
        failed = 0

        for fix in fixes:
            if fix.issue_type == 'hardcoded_api_key':
                # This fix was already applied during detection
                successful += 1
            else:
                # Apply other types of fixes
                if fix.success:
                    successful += 1
                else:
                    failed += 1

        self.log_fixes(fixes)
        return successful, failed

    def print_summary(self, fixes: List[Fix]):
        """Print summary of fixes."""
        successful = [f for f in fixes if f.success]
        failed = [f for f in fixes if not f.success]

        print("\n" + "=" * 70)
        print("SUPERTHINK AUTO-FIX SUMMARY")
        print("=" * 70)
        print(f"Total fixes: {len(fixes)}")
        print(f"Successful: {len(successful)} ✅")
        print(f"Failed: {len(failed)} ❌")

        if successful:
            print("\nSuccessful fixes:")
            for fix in successful:
                print(f"  ✅ [{fix.severity}] {fix.file_path}:{fix.line_number} - {fix.issue_type}")

        if failed:
            print("\nFailed fixes:")
            for fix in failed:
                print(f"  ❌ [{fix.severity}] {fix.file_path}:{fix.line_number}")
                print(f"     Error: {fix.error_message}")

        print("=" * 70 + "\n")


def create_auto_fixer(repo_root: str = '.') -> AutoFixer:
    """Factory function to create an AutoFixer instance."""
    return AutoFixer(repo_root)
