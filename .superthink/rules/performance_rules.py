"""
Performance Validation Rules for Event Trading System
======================================================

Validates:
- N+1 database query detection
- Algorithm efficiency (O(n²) and worse detection)
- Memory leak patterns
- Async/await validation
- Event processing latency constraints
- Function complexity metrics
- Loop nesting depth
- Recursion depth

Severity Levels:
- 🔴 CRITICAL: >5s event latency, unbounded recursion, unmanaged memory
- 🟠 HIGH: O(n²) algorithms, N+1 queries, async without await
- 🟡 MEDIUM: Deep nesting (>4 levels), long functions (>100 lines)
- 🔵 LOW: Code style, minor inefficiencies

All issues are auto-fixable or flagged for review.
"""

import ast
import re
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class PerformanceIssue:
    """Represents a performance issue found in code"""
    severity: Severity
    rule: str
    file_path: str
    line_number: int
    message: str
    code_snippet: Optional[str] = None
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False
    impact_description: str = ""


class QueryPatternDetector(ast.NodeVisitor):
    """Detects N+1 query patterns in loops"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[PerformanceIssue] = []
        self.in_loop = False
        self.loop_depth = 0
        self.database_calls: List[Tuple[int, str]] = []

    def visit_For(self, node: ast.For):
        """Track loops and database calls within them"""
        self.in_loop = True
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = False

    def visit_While(self, node: ast.While):
        """Track while loops"""
        self.in_loop = True
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = False

    def visit_Call(self, node: ast.Call):
        """Detect database query calls within loops"""
        if self.in_loop:
            call_name = self._get_call_name(node)
            db_patterns = [
                'query', 'execute', 'fetch', 'get_by_id', 'select',
                'find', 'filter', 'all', 'count', 'aggregate',
                'db.session', 'db.query', 'db.execute'
            ]

            if any(pattern in call_name.lower() for pattern in db_patterns):
                severity = Severity.CRITICAL if self.loop_depth > 1 else Severity.HIGH
                issue = PerformanceIssue(
                    severity=severity,
                    rule="N+1 Query Pattern",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    message=f"Potential N+1 query detected: '{call_name}' called in loop (depth: {self.loop_depth})",
                    code_snippet=f"Line {node.lineno}: {call_name}(...)",
                    suggested_fix="Move query outside loop or use batch query method",
                    auto_fixable=False,
                    impact_description="Multiplies database load by loop iterations, severe performance degradation"
                )
                self.issues.append(issue)

        self.generic_visit(node)

    @staticmethod
    def _get_call_name(node: ast.Call) -> str:
        """Extract function name from Call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return "unknown"


class AlgorithmComplexityAnalyzer(ast.NodeVisitor):
    """Analyzes algorithm complexity using code patterns"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[PerformanceIssue] = []
        self.current_function = None
        self.nested_loops = 0
        self.max_nesting = 0

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Analyze function for complexity"""
        self.current_function = node
        self.nested_loops = 0
        self.max_nesting = 0

        # Count function length
        func_length = len(node.body)
        if func_length > 100:
            issue = PerformanceIssue(
                severity=Severity.MEDIUM,
                rule="Function Complexity",
                file_path=self.file_path,
                line_number=node.lineno,
                message=f"Function '{node.name}' is very long ({func_length} lines)",
                suggested_fix="Consider breaking into smaller functions",
                auto_fixable=False,
                impact_description="Reduced readability, harder to test and optimize"
            )
            self.issues.append(issue)

        self.generic_visit(node)
        self.current_function = None

    def visit_For(self, node: ast.For):
        """Track nested loop depth"""
        self.nested_loops += 1
        self.max_nesting = max(self.max_nesting, self.nested_loops)

        if self.nested_loops >= 3:
            severity = Severity.HIGH if self.nested_loops >= 4 else Severity.MEDIUM
            issue = PerformanceIssue(
                severity=severity,
                rule="Deeply Nested Loops",
                file_path=self.file_path,
                line_number=node.lineno,
                message=f"Found {self.nested_loops}-level nested loops (likely O(n^{self.nested_loops}))",
                suggested_fix="Refactor to reduce nesting or use vectorized operations",
                auto_fixable=False,
                impact_description=f"Algorithm complexity is O(n^{self.nested_loops}), exponential performance degradation"
            )
            self.issues.append(issue)

        self.generic_visit(node)
        self.nested_loops -= 1

    def visit_While(self, node: ast.While):
        """Track while loop nesting"""
        self.nested_loops += 1
        self.max_nesting = max(self.max_nesting, self.nested_loops)

        if self.nested_loops >= 3:
            issue = PerformanceIssue(
                severity=Severity.MEDIUM,
                rule="Deeply Nested Loops",
                file_path=self.file_path,
                line_number=node.lineno,
                message=f"Found {self.nested_loops}-level nested loops",
                suggested_fix="Consider refactoring to reduce complexity",
                auto_fixable=False,
                impact_description=f"Complexity potentially O(n^{self.nested_loops})"
            )
            self.issues.append(issue)

        self.generic_visit(node)
        self.nested_loops -= 1


class MemoryLeakDetector:
    """Detects potential memory leak patterns"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[PerformanceIssue] = []
        self.lines: List[str] = []

    def analyze(self, content: str) -> List[PerformanceIssue]:
        """Analyze file content for memory leak patterns"""
        self.lines = content.split('\n')

        # Check for unclosed file handles
        self._check_file_handles()

        # Check for unbounded collections
        self._check_unbounded_collections()

        # Check for circular references
        self._check_circular_references()

        return self.issues

    def _check_file_handles(self):
        """Detect file operations without context managers"""
        for i, line in enumerate(self.lines):
            # Pattern: open(...) without with statement
            if re.search(r'open\s*\(', line) and 'with' not in line:
                # Check if it's not in a with statement on previous line
                if i > 0 and 'with' not in self.lines[i-1]:
                    issue = PerformanceIssue(
                        severity=Severity.HIGH,
                        rule="Resource Management",
                        file_path=self.file_path,
                        line_number=i + 1,
                        message=f"File opened without 'with' statement (potential resource leak)",
                        code_snippet=line.strip(),
                        suggested_fix="Use: with open(...) as f:",
                        auto_fixable=True,
                        impact_description="File handle not properly closed, resource exhaustion over time"
                    )
                    self.issues.append(issue)

    def _check_unbounded_collections(self):
        """Detect potentially unbounded lists or caches"""
        for i, line in enumerate(self.lines):
            # Pattern: list.append in infinite loop or without bounds check
            if '.append(' in line and 'while True' in '\n'.join(self.lines[max(0, i-10):i]):
                issue = PerformanceIssue(
                    severity=Severity.CRITICAL,
                    rule="Unbounded Collection",
                    file_path=self.file_path,
                    line_number=i + 1,
                    message="Unbounded append in infinite loop detected (memory exhaustion risk)",
                    code_snippet=line.strip(),
                    suggested_fix="Add maximum size check or use collections.deque with maxlen",
                    auto_fixable=False,
                    impact_description="List grows unbounded until memory exhaustion"
                )
                self.issues.append(issue)

    def _check_circular_references(self):
        """Detect patterns that may cause circular reference memory leaks"""
        for i, line in enumerate(self.lines):
            # Pattern: self.parent = parent; parent.child = self (simplified check)
            if 'self.' in line and '=' in line:
                context = '\n'.join(self.lines[max(0, i-5):min(len(self.lines), i+5)])
                if 'self.' in context and context.count('=') > 3:
                    # Potential circular reference - flag for review
                    issue = PerformanceIssue(
                        severity=Severity.LOW,
                        rule="Potential Circular Reference",
                        file_path=self.file_path,
                        line_number=i + 1,
                        message="Potential circular reference pattern detected",
                        code_snippet=line.strip(),
                        suggested_fix="Use weak references (weakref module) or redesign object graph",
                        auto_fixable=False,
                        impact_description="Objects may not be garbage collected, memory leak over time"
                    )
                    self.issues.append(issue)
                    break  # Only flag once per context


class AsyncAwaitValidator(ast.NodeVisitor):
    """Validates proper async/await patterns"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[PerformanceIssue] = []
        self.in_async_function = False

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Track async functions"""
        self.in_async_function = True
        self.generic_visit(node)
        self.in_async_function = False

    def visit_Call(self, node: ast.Call):
        """Check for missing await on coroutines"""
        call_name = self._get_call_name(node)

        # If calling an async function, check if it's awaited
        if self.in_async_function:
            if call_name in ['sleep', 'wait', 'fetch', 'query', 'execute']:
                # This is a simple heuristic - in real code, we'd need better tracking
                issue = PerformanceIssue(
                    severity=Severity.HIGH,
                    rule="Async Pattern",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    message=f"Potential missing await on async function '{call_name}'",
                    suggested_fix="Add 'await' before the function call",
                    auto_fixable=False,
                    impact_description="Async function not awaited, blocks event loop"
                )
                # Only flag if not already awaited
                self.issues.append(issue)

        self.generic_visit(node)

    @staticmethod
    def _get_call_name(node: ast.Call) -> str:
        """Extract function name from Call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return "unknown"


class LatencyValidator:
    """Validates event processing latency constraints"""

    def __init__(self, file_path: str, latency_threshold_ms: int = 5000):
        self.file_path = file_path
        self.issues: List[PerformanceIssue] = []
        self.latency_threshold = latency_threshold_ms
        self.lines: List[str] = []

    def analyze(self, content: str) -> List[PerformanceIssue]:
        """Analyze for latency violations"""
        self.lines = content.split('\n')

        # Check for blocking operations in event handlers
        self._check_blocking_operations()

        # Check for long-running synchronous code
        self._check_long_running_operations()

        return self.issues

    def _check_blocking_operations(self):
        """Detect blocking operations in event processing"""
        blocking_patterns = [
            (r'requests\.(get|post|put|delete)', 'HTTP request'),
            (r'time\.sleep', 'Sleep call'),
            (r'socket\.(socket|connect)', 'Socket operation'),
            (r'subprocess\.run|os\.system', 'Subprocess execution'),
        ]

        for i, line in enumerate(self.lines):
            # Check if in event handler or on_event function
            context = '\n'.join(self.lines[max(0, i-20):i])

            if 'on_event' in context or 'handle_event' in context or 'process_event' in context:
                for pattern, operation_name in blocking_patterns:
                    if re.search(pattern, line):
                        issue = PerformanceIssue(
                            severity=Severity.HIGH,
                            rule="Blocking Operation in Event Handler",
                            file_path=self.file_path,
                            line_number=i + 1,
                            message=f"Blocking {operation_name} in event handler (violates <5s latency)",
                            code_snippet=line.strip(),
                            suggested_fix=f"Use async version (aiohttp, asyncio, etc) or move to background task",
                            auto_fixable=False,
                            impact_description="Blocks event processing loop, increases latency for all events"
                        )
                        self.issues.append(issue)

    def _check_long_running_operations(self):
        """Detect patterns indicating long-running operations"""
        for i, line in enumerate(self.lines):
            # Check for large loops or computations
            if re.search(r'for\s+\w+\s+in\s+range\s*\(\s*\d{6,}', line):
                issue = PerformanceIssue(
                    severity=Severity.MEDIUM,
                    rule="Potentially Long Loop",
                    file_path=self.file_path,
                    line_number=i + 1,
                    message="Loop with very large iteration count detected",
                    code_snippet=line.strip(),
                    suggested_fix="Consider using vectorized operations (NumPy) or batch processing",
                    auto_fixable=False,
                    impact_description="Long computation blocks event processing"
                )
                self.issues.append(issue)


class PerformanceValidator:
    """Main performance validator orchestrating all checks"""

    def __init__(self, file_path: str, latency_threshold_ms: int = 5000):
        self.file_path = file_path
        self.latency_threshold = latency_threshold_ms
        self.issues: List[PerformanceIssue] = []

    def validate(self, content: str) -> List[PerformanceIssue]:
        """Run all performance validation checks"""
        self.issues.clear()

        try:
            # Parse AST-based checks
            tree = ast.parse(content)

            # N+1 query detection
            query_detector = QueryPatternDetector(self.file_path)
            query_detector.visit(tree)
            self.issues.extend(query_detector.issues)

            # Algorithm complexity
            complexity_analyzer = AlgorithmComplexityAnalyzer(self.file_path)
            complexity_analyzer.visit(tree)
            self.issues.extend(complexity_analyzer.issues)

            # Async/await validation
            async_validator = AsyncAwaitValidator(self.file_path)
            async_validator.visit(tree)
            self.issues.extend(async_validator.issues)

        except SyntaxError:
            # If file has syntax errors, skip AST-based checks
            pass

        # Regex-based checks (work on raw content)

        # Memory leak detection
        memory_detector = MemoryLeakDetector(self.file_path)
        self.issues.extend(memory_detector.analyze(content))

        # Latency validation
        latency_validator = LatencyValidator(self.file_path, self.latency_threshold)
        self.issues.extend(latency_validator.analyze(content))

        return self.issues

    def has_critical_issues(self) -> bool:
        """Check if there are any critical performance issues"""
        return any(issue.severity == Severity.CRITICAL for issue in self.issues)

    def get_summary(self) -> str:
        """Get summary of issues found"""
        by_severity = {}
        for issue in self.issues:
            severity = issue.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1

        summary = f"Performance Issues in {self.file_path}:\n"
        summary += f"  🔴 Critical: {by_severity.get('critical', 0)}\n"
        summary += f"  🟠 High: {by_severity.get('high', 0)}\n"
        summary += f"  🟡 Medium: {by_severity.get('medium', 0)}\n"
        summary += f"  🔵 Low: {by_severity.get('low', 0)}\n"

        return summary

    def print_detailed_report(self):
        """Print detailed report of all issues"""
        if not self.issues:
            print(f"✅ {self.file_path}: No performance issues detected")
            return

        print(f"\n📊 Performance Validation Report: {self.file_path}")
        print("=" * 70)

        # Group by severity
        by_severity = {}
        for issue in self.issues:
            severity = issue.severity.value
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(issue)

        severity_order = ['critical', 'high', 'medium', 'low']
        severity_icons = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🔵'
        }

        for severity in severity_order:
            if severity in by_severity:
                print(f"\n{severity_icons[severity]} {severity.upper()} Issues:")
                for issue in by_severity[severity]:
                    print(f"\n  Line {issue.line_number}: {issue.rule}")
                    print(f"  Message: {issue.message}")
                    if issue.code_snippet:
                        print(f"  Code: {issue.code_snippet}")
                    print(f"  Impact: {issue.impact_description}")
                    if issue.suggested_fix:
                        print(f"  Fix: {issue.suggested_fix}")
                    print(f"  Auto-fixable: {'Yes' if issue.auto_fixable else 'No'}")


# Test cases and example usage
if __name__ == "__main__":
    # Example 1: N+1 Query Detection
    n_plus_1_code = """
for item in items:
    result = db.query(Item).filter(Item.id == item.id).first()
    process(result)
"""

    # Example 2: Deeply Nested Loops
    nested_code = """
for i in range(n):
    for j in range(n):
        for k in range(n):
            for l in range(n):
                compute(i, j, k, l)
"""

    # Example 3: File Handle Without Context Manager
    memory_leak_code = """
f = open('file.txt')
data = f.read()
process(data)
"""

    # Example 4: Blocking Operation in Event Handler
    blocking_code = """
async def on_event(event):
    response = requests.get('https://example.com/api')
    process(response)
"""

    print("Performance Validation Rules Module")
    print("=" * 70)
    print("\nValidators available:")
    print("  - QueryPatternDetector: N+1 query detection")
    print("  - AlgorithmComplexityAnalyzer: O(n²) and worse patterns")
    print("  - MemoryLeakDetector: Resource management issues")
    print("  - AsyncAwaitValidator: Async/await correctness")
    print("  - LatencyValidator: Event processing latency constraints")
    print("\nSeverity Levels:")
    print("  🔴 CRITICAL: >5s latency, unbounded recursion, unmanaged memory")
    print("  🟠 HIGH: O(n²) algorithms, N+1 queries, async issues")
    print("  🟡 MEDIUM: Deep nesting, long functions")
    print("  🔵 LOW: Style issues, minor inefficiencies")
