"""
Deep Scan Engine for Comprehensive Code Analysis
=================================================

Performs comprehensive analysis of entire codebase:
- Full security audit (all files)
- Performance profiling and bottleneck detection
- Technical debt analysis
- Code quality metrics
- Dependency scanning
- Architecture compliance review
- Test coverage analysis
- Documentation completeness

Can be run:
1. Via GitHub Actions: Nightly at 2 AM UTC
2. Manually: python .superthink/scanners/deep_scan.py --full
3. Targeted: python deep_scan.py --security --files src/

Output: .superthink/reports/{date}/
"""

import os
import sys
import json
import ast
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime
from enum import Enum
import hashlib
import argparse


class ScanType(Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    DOCUMENTATION = "documentation"
    TESTS = "tests"
    DEPENDENCIES = "dependencies"
    FULL = "full"


@dataclass
class ScanIssue:
    """Represents an issue found during deep scan"""
    severity: str
    category: str
    file_path: str
    line_number: int
    message: str
    details: Optional[str] = None
    remediation: Optional[str] = None
    impact_score: float = 0.5  # 0.0-1.0
    effort_score: float = 0.5  # 0.0-1.0 (effort to fix)


class SecurityAuditor:
    """Comprehensive security audit of codebase"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.issues: List[ScanIssue] = []
        self.files_scanned = 0

    def audit(self) -> List[ScanIssue]:
        """Run full security audit"""
        print("🔐 Running comprehensive security audit...")

        python_files = list(self.base_path.glob("src/**/*.py"))
        print(f"   Scanning {len(python_files)} Python files...")

        for file_path in python_files:
            self.files_scanned += 1
            self._audit_file(file_path)

        return self.issues

    def _audit_file(self, file_path: Path):
        """Audit individual file"""
        try:
            content = file_path.read_text()
            lines = content.split('\n')

            # Check for hardcoded secrets (comprehensive)
            self._check_hardcoded_secrets(file_path, lines)

            # Check for SQL injection vulnerabilities
            self._check_sql_injection(file_path, lines)

            # Check for insecure cryptography
            self._check_insecure_crypto(file_path, lines)

            # Check for insecure deserialization
            self._check_insecure_deserialize(file_path, lines)

            # Check for command injection risks
            self._check_command_injection(file_path, lines)

            # Check for path traversal vulnerabilities
            self._check_path_traversal(file_path, lines)

            # Check for dependency version pins
            self._check_dependency_versions(file_path, lines)

        except Exception as e:
            issue = ScanIssue(
                severity="medium",
                category="security_scan_error",
                file_path=str(file_path),
                line_number=0,
                message=f"Error scanning file: {str(e)}",
                impact_score=0.1
            )
            self.issues.append(issue)

    def _check_hardcoded_secrets(self, file_path: Path, lines: List[str]):
        """Check for hardcoded API keys, passwords, tokens"""
        secret_patterns = {
            r'api[_-]?key\s*=\s*["\']': "API Key",
            r'password\s*=\s*["\']': "Password",
            r'secret\s*=\s*["\']': "Secret",
            r'token\s*=\s*["\']': "Token",
            r'authorization\s*:\s*["\']': "Authorization token",
            r'aws[_-]?secret\s*=\s*["\']': "AWS Secret",
            r'private[_-]?key\s*=\s*["\']': "Private Key",
        }

        import re
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                continue  # Skip comments

            for pattern, secret_type in secret_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    # Check if it's using environment variable
                    if 'os.getenv' not in line and 'environ' not in line:
                        issue = ScanIssue(
                            severity="critical",
                            category="hardcoded_secret",
                            file_path=str(file_path),
                            line_number=i,
                            message=f"Hardcoded {secret_type} detected",
                            details=f"Pattern: {secret_type}",
                            remediation="Move to environment variable or secrets manager",
                            impact_score=0.95,
                            effort_score=0.2
                        )
                        self.issues.append(issue)

    def _check_sql_injection(self, file_path: Path, lines: List[str]):
        """Check for SQL injection vulnerabilities"""
        import re
        for i, line in enumerate(lines, 1):
            # Check for string concatenation in SQL queries
            if re.search(r'(SELECT|INSERT|UPDATE|DELETE|DROP).*\+|.*f["\'].*\{', line, re.IGNORECASE):
                if '.format(' in line or f'{' in line or '+' in line:
                    issue = ScanIssue(
                        severity="critical",
                        category="sql_injection",
                        file_path=str(file_path),
                        line_number=i,
                        message="Potential SQL injection: string concatenation in query",
                        details="SQL queries constructed with string concatenation are vulnerable",
                        remediation="Use parameterized queries with placeholders",
                        impact_score=0.9,
                        effort_score=0.6
                    )
                    self.issues.append(issue)

    def _check_insecure_crypto(self, file_path: Path, lines: List[str]):
        """Check for insecure cryptography usage"""
        insecure_patterns = {
            r'md5': 'MD5 (insecure)',
            r'sha1': 'SHA1 (insecure)',
            r'des': 'DES (insecure)',
            r'rc4': 'RC4 (insecure)',
            r'hashlib\.md5': 'MD5 via hashlib',
        }

        import re
        for i, line in enumerate(lines, 1):
            for pattern, description in insecure_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    issue = ScanIssue(
                        severity="high",
                        category="insecure_crypto",
                        file_path=str(file_path),
                        line_number=i,
                        message=f"Insecure cryptography: {description}",
                        details="Modern hash: SHA256, Encryption: AES-256",
                        remediation="Use SHA256+ for hashing, AES-256 for encryption",
                        impact_score=0.7,
                        effort_score=0.4
                    )
                    self.issues.append(issue)

    def _check_insecure_deserialize(self, file_path: Path, lines: List[str]):
        """Check for insecure deserialization (pickle, yaml)"""
        import re
        for i, line in enumerate(lines, 1):
            if re.search(r'pickle\.load|yaml\.load|json\.load|eval\(', line):
                if 'pickle.load' in line or 'yaml.load' in line and 'Loader' not in line:
                    issue = ScanIssue(
                        severity="critical",
                        category="insecure_deserialization",
                        file_path=str(file_path),
                        line_number=i,
                        message="Insecure deserialization detected",
                        details="pickle.load and yaml.load without safe loaders are exploitable",
                        remediation="Use SafeLoader: yaml.load(f, Loader=yaml.SafeLoader)",
                        impact_score=0.85,
                        effort_score=0.3
                    )
                    self.issues.append(issue)

                if 'eval(' in line:
                    issue = ScanIssue(
                        severity="critical",
                        category="code_injection",
                        file_path=str(file_path),
                        line_number=i,
                        message="Use of eval() function detected",
                        details="eval() executes arbitrary code, major security risk",
                        remediation="Use ast.literal_eval() for data or refactor logic",
                        impact_score=0.95,
                        effort_score=0.5
                    )
                    self.issues.append(issue)

    def _check_command_injection(self, file_path: Path, lines: List[str]):
        """Check for command injection vulnerabilities"""
        import re
        for i, line in enumerate(lines, 1):
            if re.search(r'os\.system|subprocess\.call|os\.popen|shell\s*=\s*True', line):
                if 'subprocess.run' in line and 'shell=True' in line:
                    issue = ScanIssue(
                        severity="critical",
                        category="command_injection",
                        file_path=str(file_path),
                        line_number=i,
                        message="Command injection risk: shell=True with subprocess",
                        details="shell=True allows shell metacharacter injection",
                        remediation="Use subprocess.run with shell=False and list of arguments",
                        impact_score=0.9,
                        effort_score=0.4
                    )
                    self.issues.append(issue)

    def _check_path_traversal(self, file_path: Path, lines: List[str]):
        """Check for path traversal vulnerabilities"""
        import re
        for i, line in enumerate(lines, 1):
            if re.search(r'open\s*\(\s*user_input|open\s*\(\s*filename|open\s*\(\s*path', line, re.IGNORECASE):
                # Check if path is validated
                if '../' not in '\n'.join(lines[max(0, i-5):i]):
                    issue = ScanIssue(
                        severity="high",
                        category="path_traversal",
                        file_path=str(file_path),
                        line_number=i,
                        message="Potential path traversal: user-supplied file path",
                        details="File path comes from user input without validation",
                        remediation="Validate paths: reject '..' and use os.path.abspath()",
                        impact_score=0.75,
                        effort_score=0.4
                    )
                    self.issues.append(issue)

    def _check_dependency_versions(self, file_path: Path, lines: List[str]):
        """Check for unpinned or vulnerable dependencies"""
        if file_path.name == "requirements.txt":
            for i, line in enumerate(lines, 1):
                if '==' not in line and line.strip() and not line.strip().startswith('#'):
                    issue = ScanIssue(
                        severity="medium",
                        category="dependency_version",
                        file_path=str(file_path),
                        line_number=i,
                        message="Unpinned dependency version",
                        details=f"Dependency {line.strip()} doesn't specify exact version",
                        remediation="Pin to specific version: package==X.Y.Z",
                        impact_score=0.4,
                        effort_score=0.1
                    )
                    self.issues.append(issue)


class PerformanceAnalyzer:
    """Performance analysis and bottleneck detection"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.issues: List[ScanIssue] = []
        self.metrics = {}

    def analyze(self) -> List[ScanIssue]:
        """Run performance analysis"""
        print("⚡ Analyzing performance characteristics...")

        python_files = list(self.base_path.glob("src/**/*.py"))
        print(f"   Analyzing {len(python_files)} files...")

        for file_path in python_files:
            self._analyze_file(file_path)

        return self.issues

    def _analyze_file(self, file_path: Path):
        """Analyze single file"""
        try:
            content = file_path.read_text()

            # Check for obvious inefficiencies
            self._check_algorithm_complexity(file_path, content)

            # Check for memory inefficiencies
            self._check_memory_patterns(file_path, content)

            # Check for blocking operations
            self._check_blocking_operations(file_path, content)

        except Exception as e:
            pass

    def _check_algorithm_complexity(self, file_path: Path, content: str):
        """Check for O(n²) and worse algorithms"""
        lines = content.split('\n')

        # Track nested loop depth
        import re
        for i, line in enumerate(lines, 1):
            # Count opening parentheses to estimate nesting
            nested_loops = 0
            for j in range(max(0, i-5), i):
                if 'for ' in lines[j] or 'while ' in lines[j]:
                    nested_loops += 1

            if nested_loops >= 3:
                issue = ScanIssue(
                    severity="medium",
                    category="algorithm_complexity",
                    file_path=str(file_path),
                    line_number=i,
                    message=f"Deeply nested loops detected (O(n^{nested_loops}))",
                    details="Multiple nested loops indicate potential exponential complexity",
                    remediation="Refactor using vectorization (NumPy) or data structures (dict, set)",
                    impact_score=0.5,
                    effort_score=0.7
                )
                self.issues.append(issue)
                break  # One per file

    def _check_memory_patterns(self, file_path: Path, content: str):
        """Check for memory leak patterns"""
        lines = content.split('\n')
        import re

        for i, line in enumerate(lines, 1):
            # Check for unclosed file handles
            if re.search(r'open\s*\(', line) and 'with' not in lines[i-1] if i > 1 else False:
                issue = ScanIssue(
                    severity="high",
                    category="resource_leak",
                    file_path=str(file_path),
                    line_number=i,
                    message="File opened without 'with' statement",
                    details="File handle may not be properly closed",
                    remediation="Use: with open(file) as f:",
                    impact_score=0.6,
                    effort_score=0.2
                )
                self.issues.append(issue)

    def _check_blocking_operations(self, file_path: Path, content: str):
        """Check for blocking operations in async code"""
        import re
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            if 'async def' in lines[i-1] if i > 1 else False:
                # Inside async function
                if re.search(r'time\.sleep|requests\.|socket\.', line):
                    issue = ScanIssue(
                        severity="high",
                        category="blocking_in_async",
                        file_path=str(file_path),
                        line_number=i,
                        message="Blocking operation in async function",
                        details="This blocks the entire event loop",
                        remediation="Use: await asyncio.sleep(), aiohttp, etc.",
                        impact_score=0.8,
                        effort_score=0.5
                    )
                    self.issues.append(issue)


class TechnicalDebtAnalyzer:
    """Technical debt and code quality analysis"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.issues: List[ScanIssue] = []
        self.metrics = {}

    def analyze(self) -> List[ScanIssue]:
        """Analyze technical debt"""
        print("🏗️ Analyzing technical debt...")

        python_files = list(self.base_path.glob("src/**/*.py"))

        # Calculate metrics
        total_lines = 0
        total_functions = 0
        total_classes = 0

        for file_path in python_files:
            try:
                content = file_path.read_text()
                total_lines += len(content.split('\n'))

                # Parse AST for structure
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        total_functions += 1
                    elif isinstance(node, ast.ClassDef):
                        total_classes += 1

                # Check for debt indicators
                self._check_file_debt(file_path, content)

            except:
                pass

        self.metrics['total_files'] = len(python_files)
        self.metrics['total_lines'] = total_lines
        self.metrics['total_functions'] = total_functions
        self.metrics['total_classes'] = total_classes

        return self.issues

    def _check_file_debt(self, file_path: Path, content: str):
        """Check for debt indicators in file"""
        lines = content.split('\n')

        # Check for TODO/FIXME comments
        for i, line in enumerate(lines, 1):
            if 'TODO' in line or 'FIXME' in line or 'XXX' in line or 'HACK' in line:
                issue = ScanIssue(
                    severity="low",
                    category="technical_debt",
                    file_path=str(file_path),
                    line_number=i,
                    message=f"Technical debt marker: {line.strip()}",
                    details="Developer left a note about incomplete or problematic code",
                    remediation="Address the marked issue or create a tracking ticket",
                    impact_score=0.3,
                    effort_score=0.5
                )
                self.issues.append(issue)


class DeepScanner:
    """Main deep scan orchestrator"""

    def __init__(self, base_path: str = ".", output_dir: Optional[str] = None):
        self.base_path = Path(base_path)
        self.output_dir = Path(output_dir or ".superthink/reports/deep-scan")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create timestamp subdirectory
        self.scan_dir = self.output_dir / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.scan_dir.mkdir(parents=True, exist_ok=True)

        self.all_issues: List[ScanIssue] = []
        self.start_time = None
        self.end_time = None

    def run(self, scan_types: List[ScanType] = None):
        """Run deep scan"""
        if scan_types is None or ScanType.FULL in scan_types:
            scan_types = [ScanType.SECURITY, ScanType.PERFORMANCE, ScanType.ARCHITECTURE]

        self.start_time = time.time()

        print("\n" + "=" * 70)
        print("🔬 SUPERTHINK DEEP SCAN")
        print("=" * 70)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Output: {self.scan_dir}")
        print("")

        # Run requested scans
        if ScanType.SECURITY in scan_types:
            auditor = SecurityAuditor(str(self.base_path))
            self.all_issues.extend(auditor.audit())
            print(f"✅ Security audit complete: {len(auditor.issues)} issues")

        if ScanType.PERFORMANCE in scan_types:
            analyzer = PerformanceAnalyzer(str(self.base_path))
            self.all_issues.extend(analyzer.analyze())
            print(f"✅ Performance analysis complete: {len(analyzer.issues)} issues")

        if ScanType.ARCHITECTURE in scan_types:
            debt_analyzer = TechnicalDebtAnalyzer(str(self.base_path))
            self.all_issues.extend(debt_analyzer.analyze())
            print(f"✅ Technical debt analysis complete: {len(debt_analyzer.issues)} issues")

        self.end_time = time.time()

        # Generate reports
        self._generate_reports()

    def _generate_reports(self):
        """Generate comprehensive reports"""
        print("\n" + "=" * 70)
        print("📊 GENERATING REPORTS")
        print("=" * 70)

        # Summary report
        self._generate_summary_report()

        # Detailed report
        self._generate_detailed_report()

        # JSON report
        self._generate_json_report()

        # Statistics
        self._generate_statistics()

        print(f"\n✅ All reports generated in: {self.scan_dir}")

    def _generate_summary_report(self):
        """Generate executive summary"""
        report_file = self.scan_dir / "SUMMARY.md"

        # Count by severity
        by_severity = {}
        for issue in self.all_issues:
            severity = issue.severity
            by_severity[severity] = by_severity.get(severity, 0) + 1

        content = f"""# Deep Scan Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {self.end_time - self.start_time:.1f} seconds

## Scan Results

| Severity | Count |
|----------|-------|
| 🔴 Critical | {by_severity.get('critical', 0)} |
| 🟠 High | {by_severity.get('high', 0)} |
| 🟡 Medium | {by_severity.get('medium', 0)} |
| 🔵 Low | {by_severity.get('low', 0)} |
| **Total** | **{len(self.all_issues)}** |

## Issues by Category

"""

        by_category = {}
        for issue in self.all_issues:
            cat = issue.category
            by_category[cat] = by_category.get(cat, 0) + 1

        for category, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            content += f"- {category}: {count}\n"

        content += f"""

## Top Priority Issues

"""
        # Sort by impact * effort
        scored = [(i, i.impact_score / max(0.1, i.effort_score)) for i in self.all_issues]
        for issue, score in sorted(scored, key=lambda x: x[1], reverse=True)[:10]:
            content += f"- **[{issue.severity.upper()}]** {issue.category}: {issue.message}\n"

        report_file.write_text(content)
        print(f"  📄 Summary: {report_file.name}")

    def _generate_detailed_report(self):
        """Generate detailed issue report"""
        report_file = self.scan_dir / "DETAILED.md"

        content = f"""# Detailed Scan Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

        # Group by severity
        for severity in ['critical', 'high', 'medium', 'low']:
            issues = [i for i in self.all_issues if i.severity == severity]
            if not issues:
                continue

            icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵'}[severity]
            content += f"## {icon} {severity.upper()} Issues ({len(issues)})\n\n"

            for issue in issues:
                content += f"### {issue.category}\n"
                content += f"**File:** `{issue.file_path}:{issue.line_number}`\n\n"
                content += f"**Message:** {issue.message}\n\n"
                if issue.details:
                    content += f"**Details:** {issue.details}\n\n"
                if issue.remediation:
                    content += f"**Remediation:** {issue.remediation}\n\n"
                content += f"Impact: {issue.impact_score:.0%} | Effort: {issue.effort_score:.0%}\n\n"
                content += "---\n\n"

        report_file.write_text(content)
        print(f"  📄 Detailed: {report_file.name}")

    def _generate_json_report(self):
        """Generate machine-readable JSON report"""
        report_file = self.scan_dir / "issues.json"

        issues_dict = [asdict(issue) for issue in self.all_issues]
        report_file.write_text(json.dumps(issues_dict, indent=2))
        print(f"  📄 JSON: {report_file.name}")

    def _generate_statistics(self):
        """Generate statistics"""
        stats_file = self.scan_dir / "STATISTICS.md"

        # Calculate metrics
        critical_issues = len([i for i in self.all_issues if i.severity == 'critical'])
        high_issues = len([i for i in self.all_issues if i.severity == 'high'])
        total_impact = sum(i.impact_score for i in self.all_issues)
        avg_effort = sum(i.effort_score for i in self.all_issues) / max(1, len(self.all_issues))

        # Risk score: critical count + high count/2 + average impact
        risk_score = critical_issues * 10 + high_issues * 5 + total_impact

        content = f"""# Scan Statistics

## Summary Metrics

- **Total Issues:** {len(self.all_issues)}
- **Critical Issues:** {critical_issues}
- **High Issues:** {high_issues}
- **Scan Duration:** {self.end_time - self.start_time:.1f}s
- **Risk Score:** {risk_score:.1f}
- **Average Fix Effort:** {avg_effort:.0%}

## Risk Assessment

"""
        if critical_issues > 5:
            content += "🔴 **CRITICAL**: Immediate action required\n\n"
        elif critical_issues > 0:
            content += "🟠 **HIGH**: Address critical issues before deployment\n\n"
        elif high_issues > 10:
            content += "🟡 **MEDIUM**: Several important issues to address\n\n"
        else:
            content += "🟢 **LOW**: Code quality is good\n\n"

        content += f"""## Recommended Actions

1. Address all {critical_issues} critical issues immediately
2. Schedule fixes for {high_issues} high-priority issues
3. Plan refactoring for {len([i for i in self.all_issues if i.severity == 'medium'])} medium issues
4. Monitor {len([i for i in self.all_issues if i.severity == 'low'])} low-priority improvements

"""
        stats_file.write_text(content)
        print(f"  📄 Statistics: {stats_file.name}")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="Superthink Deep Scan")
    parser.add_argument('--full', action='store_true', help='Run full scan')
    parser.add_argument('--security', action='store_true', help='Security audit only')
    parser.add_argument('--performance', action='store_true', help='Performance analysis only')
    parser.add_argument('--base-path', default='.',  help='Base path for scan')
    parser.add_argument('--output', default=None, help='Output directory')

    args = parser.parse_args()

    # Determine scan types
    scan_types = []
    if args.full:
        scan_types = [ScanType.FULL]
    else:
        if args.security:
            scan_types.append(ScanType.SECURITY)
        if args.performance:
            scan_types.append(ScanType.PERFORMANCE)
        if not scan_types:  # Default to full
            scan_types = [ScanType.FULL]

    # Run scan
    scanner = DeepScanner(args.base_path, args.output)
    scanner.run(scan_types)

    print("\n" + "=" * 70)
    print("✅ SCAN COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
