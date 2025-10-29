"""
Security validation rules for Superthink-Code-Analyzer.
Detects and auto-fixes security vulnerabilities in the trading system.
"""

import re
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class SecurityIssue:
    """Represents a detected security issue."""
    severity: str  # critical, high, medium, low
    rule: str
    file_path: str
    line_number: int
    message: str
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False


class SecurityValidator:
    """Validates code for security vulnerabilities."""

    # Patterns for detecting hardcoded API keys
    API_KEY_PATTERNS = {
        'COINBASE_API_KEY': r'COINBASE_API_KEY\s*=\s*["\']([^"\']+)["\']',
        'BINANCE_API_KEY': r'BINANCE_API_KEY\s*=\s*["\']([^"\']+)["\']',
        'KRAKEN_API_KEY': r'KRAKEN_API_KEY\s*=\s*["\']([^"\']+)["\']',
        'ANTHROPIC_API_KEY': r'ANTHROPIC_API_KEY\s*=\s*["\']([^"\']+)["\']',
        'POLYGON_API_KEY': r'POLYGON_API_KEY\s*=\s*["\']([^"\']+)["\']',
        'SUPABASE_KEY': r'SUPABASE_.*_KEY\s*=\s*["\']([^"\']+)["\']',
        'aws_access_key': r'aws_access_key_id\s*=\s*["\']([^"\']+)["\']',
        'generic_api_key': r'["\'][a-zA-Z0-9]{40,}["\']',
    }

    # SQL injection patterns
    SQL_PATTERNS = {
        'string_interpolation': r'f["\'].*?{.*?}.*?["\']',
        'format_method': r'.*\.format\(.*\)',
        'percent_formatting': r'%\s*([a-zA-Z0-9_]+)',
    }

    # Sensitive data patterns that shouldn't be logged
    SENSITIVE_PATTERNS = {
        'password_log': r'password\s*[:=]\s*["\'].*["\']',
        'api_key_log': r'api_key\s*[:=]\s*["\'].*["\']',
        'private_key_log': r'private_key\s*[:=]\s*["\'].*["\']',
        'position_data': r'position.*?\{.*?["\']price["\']',
    }

    # Insider trading prevention patterns
    INSIDER_TRADING_PATTERNS = {
        'suspicious_sources': [
            'corporate_insider',
            'executive_communication',
            'confidential_email',
            'private_message',
            'internal_only',
        ],
        'mnpi_keywords': [
            'material_nonpublic',
            'mnpi',
            'confidential_business',
            'insider',
            'undisclosed',
        ],
    }

    def validate_api_key_exposure(self, file_path: str, content: str) -> List[SecurityIssue]:
        """Check for hardcoded API keys."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Skip comments and environment variable definitions
            if line.strip().startswith('#') or '.env' in file_path:
                continue

            for key_name, pattern in self.API_KEY_PATTERNS.items():
                matches = re.finditer(pattern, line)
                for match in matches:
                    api_value = match.group(1) if match.groups() else match.group(0)

                    # Don't flag environment variable references
                    if 'os.getenv' in line or 'environ' in line or '${' in line:
                        continue

                    issue = SecurityIssue(
                        severity='critical',
                        rule='api_key_exposure',
                        file_path=file_path,
                        line_number=i,
                        message=f'Hardcoded {key_name} detected: {api_value[:20]}...',
                        suggested_fix=self._fix_api_key_exposure(line, key_name),
                        auto_fixable=True,
                    )
                    issues.append(issue)

        return issues

    def validate_sql_injection(self, file_path: str, content: str) -> List[SecurityIssue]:
        """Check for SQL injection vulnerabilities."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue

            # Skip properly parameterized queries
            if '?' in line or '%s' in line and ',' in line:
                continue

            for vuln_type, pattern in self.SQL_PATTERNS.items():
                if 'query' in line.lower() or 'sql' in line.lower():
                    if re.search(pattern, line):
                        issue = SecurityIssue(
                            severity='critical',
                            rule='sql_injection_risk',
                            file_path=file_path,
                            line_number=i,
                            message=f'Potential SQL injection via {vuln_type}: {line.strip()}',
                            suggested_fix='Use parameterized queries with ? or %s placeholders',
                            auto_fixable=False,
                        )
                        issues.append(issue)

        return issues

    def validate_sensitive_data_logging(self, file_path: str, content: str) -> List[SecurityIssue]:
        """Check for sensitive data being logged."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check if line contains logging
            if not ('print' in line or 'log' in line or 'logger' in line):
                continue

            for data_type, pattern in self.SENSITIVE_PATTERNS.items():
                if re.search(pattern, line):
                    issue = SecurityIssue(
                        severity='high',
                        rule='sensitive_data_exposure',
                        file_path=file_path,
                        line_number=i,
                        message=f'Sensitive {data_type} may be logged: {line.strip()[:60]}...',
                        suggested_fix='Remove sensitive data from logs or redact before logging',
                        auto_fixable=False,
                    )
                    issues.append(issue)

        return issues

    def validate_insider_trading_prevention(self, file_path: str, content: str) -> List[SecurityIssue]:
        """Check for insider trading compliance."""
        issues = []
        lines = content.split('\n')

        # Only check event processing and data ingestion files
        if 'events' not in file_path and 'data' not in file_path:
            return issues

        for i, line in enumerate(lines, 1):
            line_lower = line.lower()

            # Flag suspicious information sources
            for source in self.INSIDER_TRADING_PATTERNS['suspicious_sources']:
                if source in line_lower:
                    issue = SecurityIssue(
                        severity='critical',
                        rule='insider_trading_risk',
                        file_path=file_path,
                        line_number=i,
                        message=f'Potential insider trading: {source} detected',
                        suggested_fix='Only use publicly available information sources',
                        auto_fixable=False,
                    )
                    issues.append(issue)

        return issues

    def validate_authentication(self, file_path: str, content: str) -> List[SecurityIssue]:
        """Check for authentication weaknesses."""
        issues = []
        lines = content.split('\n')

        # Check for API endpoints without authentication
        if 'app.route' in content or 'def ' in content:
            in_function = False
            for i, line in enumerate(lines, 1):
                if 'def ' in line and ('api' in line.lower() or 'endpoint' in line.lower()):
                    in_function = True
                    func_name = line.split('def ')[1].split('(')[0]

                    # Check next few lines for auth
                    auth_found = False
                    for j in range(i, min(i+10, len(lines))):
                        if 'auth' in lines[j].lower() or 'token' in lines[j].lower():
                            auth_found = True
                            break

                    if not auth_found:
                        issue = SecurityIssue(
                            severity='high',
                            rule='missing_authentication',
                            file_path=file_path,
                            line_number=i,
                            message=f'API endpoint {func_name} may lack authentication check',
                            suggested_fix='Add authentication validation before processing request',
                            auto_fixable=False,
                        )
                        issues.append(issue)

        return issues

    def _fix_api_key_exposure(self, line: str, key_name: str) -> str:
        """Generate fix for hardcoded API key."""
        if '=' in line:
            indent = len(line) - len(line.lstrip())
            return f"{'    ' * (indent//4)}{key_name} = os.getenv('{key_name}')\n" \
                   f"{'    ' * (indent//4)}if not {key_name}:\n" \
                   f"{'    ' * ((indent//4)+1)}raise ValueError(f'{key_name} environment variable not set')"
        return None

    def run_all_validations(self, file_path: str, content: str) -> List[SecurityIssue]:
        """Run all security validations on a file."""
        all_issues = []

        all_issues.extend(self.validate_api_key_exposure(file_path, content))
        all_issues.extend(self.validate_sql_injection(file_path, content))
        all_issues.extend(self.validate_sensitive_data_logging(file_path, content))
        all_issues.extend(self.validate_insider_trading_prevention(file_path, content))
        all_issues.extend(self.validate_authentication(file_path, content))

        return all_issues


def validate_security(file_path: str, content: str) -> List[SecurityIssue]:
    """Main entry point for security validation."""
    validator = SecurityValidator()
    return validator.run_all_validations(file_path, content)
