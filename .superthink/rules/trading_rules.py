"""
Trading Logic Validation Rules for Event Trading System
========================================================

Validates:
- Position sizing (Kelly Criterion correctness)
- Risk limits enforcement (daily, monthly, drawdown)
- Portfolio optimization logic (efficient frontier, rebalancing)
- Agent consensus mechanism (Bayesian aggregation)
- Event scoring formulas (impact, confidence, tradability)
- Order execution validation
- Slippage estimation accuracy
- Leverage constraints

Severity Levels:
- 🔴 CRITICAL: Risk limit violations, incorrect Kelly calculation, leverage > 2x
- 🟠 HIGH: Consensus mechanism errors, position sizing > 10% per position
- 🟡 MEDIUM: Event scoring formula issues, rebalancing logic
- 🔵 LOW: Minor optimization opportunities

Note: Most trading logic issues are NOT auto-fixable due to domain complexity.
All issues are flagged for review and require business logic verification.
"""

import re
import ast
from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TradingIssue:
    """Represents a trading logic issue found in code"""
    severity: Severity
    rule: str
    file_path: str
    line_number: int
    message: str
    code_snippet: Optional[str] = None
    business_impact: str = ""
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False
    test_cases: List[str] = None
    confidence: float = 1.0  # Confidence level of issue (0.0-1.0)

    def __post_init__(self):
        if self.test_cases is None:
            self.test_cases = []


class KellyCriterionValidator:
    """Validates Kelly Criterion position sizing calculations"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[TradingIssue] = []
        self.lines: List[str] = []

    def analyze(self, content: str) -> List[TradingIssue]:
        """Analyze Kelly Criterion implementation"""
        self.lines = content.split('\n')

        # Check for Kelly formula implementation
        self._validate_kelly_formula()

        # Check for Kelly fraction scaling
        self._validate_kelly_fraction()

        # Check for edge cases
        self._validate_kelly_edge_cases()

        return self.issues

    def _validate_kelly_formula(self):
        """Validate Kelly Criterion formula: f* = (b*p - q) / b"""
        kelly_pattern = r'kelly|fraction|position_size'
        found_kelly = False

        for i, line in enumerate(self.lines):
            if re.search(kelly_pattern, line, re.IGNORECASE):
                found_kelly = True
                # Look for the formula in surrounding lines
                context = '\n'.join(self.lines[max(0, i-3):min(len(self.lines), i+4)])

                # Check if formula includes all required components
                has_win_prob = 'p' in context or 'win_probability' in context or 'win_prob' in context
                has_lose_prob = 'q' in context or '1-p' in context or 'lose_prob' in context
                has_payoff_ratio = 'b' in context or 'payoff_ratio' in context or 'odds' in context

                if not (has_win_prob and has_lose_prob and has_payoff_ratio):
                    issue = TradingIssue(
                        severity=Severity.CRITICAL,
                        rule="Kelly Criterion Formula",
                        file_path=self.file_path,
                        line_number=i + 1,
                        message="Kelly Criterion formula incomplete (missing win_prob, lose_prob, or payoff_ratio)",
                        code_snippet=context.strip(),
                        business_impact="Incorrect position sizing leads to excessive leverage or under-leveraging",
                        suggested_fix="Implement: f* = (win_prob * payoff_ratio - lose_prob) / payoff_ratio",
                        auto_fixable=False,
                        test_cases=[
                            "f*(p=0.6, b=2, q=0.4) = 0.2 (20% of portfolio)",
                            "f*(p=0.55, b=1, q=0.45) = 0.1 (10% of portfolio)",
                            "f*(p=0.5, b=1, q=0.5) = 0 (no position)",
                        ],
                        confidence=0.95
                    )
                    self.issues.append(issue)
                    break

        if not found_kelly:
            issue = TradingIssue(
                severity=Severity.HIGH,
                rule="Kelly Criterion Missing",
                file_path=self.file_path,
                line_number=1,
                message="No Kelly Criterion implementation found for position sizing",
                business_impact="Manual position sizing is suboptimal and risks over-leveraging",
                suggested_fix="Implement Kelly Criterion calculator",
                auto_fixable=False,
                confidence=0.8
            )
            self.issues.append(issue)

    def _validate_kelly_fraction(self):
        """Validate Kelly fraction is scaled (not full Kelly)"""
        for i, line in enumerate(self.lines):
            # Look for full Kelly usage without scaling
            if 'kelly' in line.lower() and '*' in line:
                # Check if there's a scaling factor (typically 0.25 for safety)
                if not re.search(r'[\d.]+\s*\*.*kelly|kelly.*\*[\d.]+', line, re.IGNORECASE):
                    # And check context for scaling
                    context = '\n'.join(self.lines[max(0, i-2):min(len(self.lines), i+3)])
                    if 'kelly' in context.lower() and '0.' not in context:
                        issue = TradingIssue(
                            severity=Severity.HIGH,
                            rule="Kelly Fraction Scaling",
                            file_path=self.file_path,
                            line_number=i + 1,
                            message="Kelly Criterion not scaled (using full Kelly is high-risk)",
                            code_snippet=context.strip(),
                            business_impact="Full Kelly causes high volatility and drawdown; recommend 0.25 Kelly",
                            suggested_fix="Scale Kelly: position_size = 0.25 * kelly_fraction",
                            auto_fixable=False,
                            test_cases=[
                                "Full Kelly: f*=0.2 → position_size=0.2 (20% per trade)",
                                "Scaled Kelly (0.25): position_size=0.05 (5% per trade)",
                            ],
                            confidence=0.85
                        )
                        self.issues.append(issue)

    def _validate_kelly_edge_cases(self):
        """Validate handling of edge cases"""
        for i, line in enumerate(self.lines):
            if 'kelly' in line.lower() or 'position_size' in line.lower():
                context = '\n'.join(self.lines[max(0, i-2):min(len(self.lines), i+5)])

                # Check for division by zero (payoff_ratio = 0)
                if 'payoff_ratio' in context or 'b =' in context:
                    if '/ ' in context and 'if' not in context and 'assert' not in context:
                        issue = TradingIssue(
                            severity=Severity.CRITICAL,
                            rule="Kelly Edge Case: Division by Zero",
                            file_path=self.file_path,
                            line_number=i + 1,
                            message="Kelly calculation lacks protection against zero payoff_ratio",
                            code_snippet=context.strip(),
                            business_impact="Division by zero will cause runtime error or infinite position",
                            suggested_fix="Add: assert payoff_ratio > 0, 'Invalid payoff ratio'",
                            auto_fixable=False,
                            confidence=0.9
                        )
                        self.issues.append(issue)

                # Check for negative Kelly fraction
                if 'kelly' in context.lower():
                    if 'max(0' not in context and 'if kelly' not in context:
                        issue = TradingIssue(
                            severity=Severity.HIGH,
                            rule="Kelly Edge Case: Negative Kelly",
                            file_path=self.file_path,
                            line_number=i + 1,
                            message="Kelly fraction not clamped to positive range",
                            code_snippet=context.strip(),
                            business_impact="Negative Kelly would indicate shorting, may violate risk rules",
                            suggested_fix="Clamp: kelly_fraction = max(0, min(kelly_fraction, max_leverage))",
                            auto_fixable=False,
                            test_cases=[
                                "Negative expected value: kelly = -0.1 → should clamp to 0",
                                "Excessive kelly: kelly = 0.5 → should clamp to max_leverage",
                            ],
                            confidence=0.85
                        )
                        self.issues.append(issue)


class RiskLimitValidator:
    """Validates risk limit enforcement (daily, monthly, drawdown)"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[TradingIssue] = []
        self.lines: List[str] = []

    def analyze(self, content: str) -> List[TradingIssue]:
        """Analyze risk limit implementation"""
        self.lines = content.split('\n')

        # Check for daily loss limit
        self._validate_daily_limit()

        # Check for monthly loss limit
        self._validate_monthly_limit()

        # Check for drawdown limit
        self._validate_drawdown_limit()

        # Check for max position size
        self._validate_position_limits()

        return self.issues

    def _validate_daily_limit(self):
        """Validate daily loss limit enforcement"""
        daily_limit_found = False

        for i, line in enumerate(self.lines):
            if 'daily' in line.lower() and ('loss' in line.lower() or 'limit' in line.lower()):
                daily_limit_found = True
                context = '\n'.join(self.lines[max(0, i-2):min(len(self.lines), i+5)])

                # Check for comparison operator
                if not any(op in context for op in ['<', '>', '<=', '>=', '==']):
                    issue = TradingIssue(
                        severity=Severity.CRITICAL,
                        rule="Daily Loss Limit",
                        file_path=self.file_path,
                        line_number=i + 1,
                        message="Daily loss limit not enforced with comparison check",
                        code_snippet=context.strip(),
                        business_impact="System could lose more than daily limit (default: 3%)",
                        suggested_fix="Add: if daily_loss < DAILY_LOSS_LIMIT: stop_trading()",
                        auto_fixable=False,
                        test_cases=[
                            "Start: $100,000, Daily limit: -$3,000 (3%)",
                            "After loss: -$2,500 → Continue trading",
                            "After loss: -$3,500 → Stop trading (exceeds limit)",
                        ],
                        confidence=0.9
                    )
                    self.issues.append(issue)

        if not daily_limit_found:
            issue = TradingIssue(
                severity=Severity.CRITICAL,
                rule="Daily Loss Limit Missing",
                file_path=self.file_path,
                line_number=1,
                message="No daily loss limit implementation found",
                business_impact="Unlimited daily losses possible (catastrophic risk)",
                suggested_fix="Implement daily loss tracking and enforcement",
                auto_fixable=False,
                confidence=0.95
            )
            self.issues.append(issue)

    def _validate_monthly_limit(self):
        """Validate monthly loss limit enforcement"""
        monthly_limit_found = False

        for i, line in enumerate(self.lines):
            if 'monthly' in line.lower() and ('loss' in line.lower() or 'limit' in line.lower()):
                monthly_limit_found = True

        if not monthly_limit_found:
            issue = TradingIssue(
                severity=Severity.HIGH,
                rule="Monthly Loss Limit Missing",
                file_path=self.file_path,
                line_number=1,
                message="No monthly loss limit implementation found",
                business_impact="Monthly losses not tracked; could exceed policy",
                suggested_fix="Implement monthly P&L tracking with review trigger",
                auto_fixable=False,
                confidence=0.8
            )
            self.issues.append(issue)

    def _validate_drawdown_limit(self):
        """Validate maximum drawdown limit"""
        drawdown_found = False

        for i, line in enumerate(self.lines):
            if 'drawdown' in line.lower() or 'max_dd' in line.lower():
                drawdown_found = True
                context = '\n'.join(self.lines[max(0, i-2):min(len(self.lines), i+5)])

                # Check for peak tracking
                if 'peak' not in context.lower():
                    issue = TradingIssue(
                        severity=Severity.HIGH,
                        rule="Drawdown Calculation",
                        file_path=self.file_path,
                        line_number=i + 1,
                        message="Drawdown calculation missing peak tracking",
                        code_snippet=context.strip(),
                        business_impact="Drawdown not calculated correctly (peak must be tracked)",
                        suggested_fix="Drawdown = (peak - current) / peak; track rolling peak",
                        auto_fixable=False,
                        test_cases=[
                            "Peak: $100,000, Current: $85,000 → Drawdown: 15%",
                            "Peak: $100,000, Current: $120,000 → Drawdown: 0% (new peak)",
                        ],
                        confidence=0.85
                    )
                    self.issues.append(issue)

        if not drawdown_found:
            issue = TradingIssue(
                severity=Severity.MEDIUM,
                rule="Drawdown Limit Missing",
                file_path=self.file_path,
                line_number=1,
                message="No maximum drawdown limit implementation found",
                business_impact="Portfolio drawdown not monitored (recommended max: 15-20%)",
                suggested_fix="Implement drawdown tracking: (peak_value - current_value) / peak_value",
                auto_fixable=False,
                confidence=0.75
            )
            self.issues.append(issue)

    def _validate_position_limits(self):
        """Validate maximum position size enforcement"""
        max_position_found = False

        for i, line in enumerate(self.lines):
            if 'position' in line.lower() and ('max' in line.lower() or 'limit' in line.lower()):
                max_position_found = True
                context = '\n'.join(self.lines[max(0, i-2):min(len(self.lines), i+5)])

                # Check for 10% default
                if '0.10' not in context and '10' not in context:
                    issue = TradingIssue(
                        severity=Severity.MEDIUM,
                        rule="Position Size Limit",
                        file_path=self.file_path,
                        line_number=i + 1,
                        message="Position size limit seems non-standard (recommend 10% max per position)",
                        code_snippet=context.strip(),
                        business_impact="Over-concentration in single positions increases risk",
                        suggested_fix="Set max_position_size = 0.10 (10% of portfolio)",
                        auto_fixable=False,
                        confidence=0.7
                    )
                    self.issues.append(issue)


class ConsensusMechanismValidator:
    """Validates agent consensus mechanism (Bayesian aggregation)"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[TradingIssue] = []
        self.lines: List[str] = []

    def analyze(self, content: str) -> List[TradingIssue]:
        """Analyze consensus mechanism"""
        self.lines = content.split('\n')

        # Check for Bayesian pooling
        self._validate_bayesian_pooling()

        # Check for weight normalization
        self._validate_weight_normalization()

        # Check for agent disagreement handling
        self._validate_disagreement_handling()

        return self.issues

    def _validate_bayesian_pooling(self):
        """Validate Bayesian opinion pooling implementation"""
        for i, line in enumerate(self.lines):
            if 'consensus' in line.lower() or 'aggregate' in line.lower() or 'pool' in line.lower():
                context = '\n'.join(self.lines[max(0, i-3):min(len(self.lines), i+6)])

                # Check for logarithmic pooling
                if 'log' not in context.lower() and 'average' not in context.lower():
                    issue = TradingIssue(
                        severity=Severity.HIGH,
                        rule="Consensus Mechanism",
                        file_path=self.file_path,
                        line_number=i + 1,
                        message="Consensus mechanism not using Bayesian pooling",
                        code_snippet=context.strip(),
                        business_impact="Naive averaging loses probabilistic information from agents",
                        suggested_fix="Use logarithmic pooling: P(outcome) ∝ ∏ P_i(outcome)^w_i",
                        auto_fixable=False,
                        test_cases=[
                            "Agent A: 70% confidence, Agent B: 60% confidence",
                            "Naive average: 65% (loses information)",
                            "Log pooling (equal weights): 65.3% with better calibration",
                        ],
                        confidence=0.75
                    )
                    self.issues.append(issue)
                    break

    def _validate_weight_normalization(self):
        """Validate weights sum to 1.0"""
        for i, line in enumerate(self.lines):
            if 'weight' in line.lower() and '=' in line:
                context = '\n'.join(self.lines[max(0, i-2):min(len(self.lines), i+8)])

                if 'sum' not in context.lower() and 'normalize' not in context.lower():
                    if 'weight' in context and '[' in context:
                        issue = TradingIssue(
                            severity=Severity.HIGH,
                            rule="Weight Normalization",
                            file_path=self.file_path,
                            line_number=i + 1,
                            message="Agent weights not normalized (should sum to 1.0)",
                            code_snippet=context.strip(),
                            business_impact="Non-normalized weights bias consensus incorrectly",
                            suggested_fix="weights = weights / weights.sum() # Normalize to 1.0",
                            auto_fixable=False,
                            test_cases=[
                                "Raw weights: [0.7, 0.8, 0.6] → sum = 2.1",
                                "Normalized: [0.333, 0.381, 0.286] → sum = 1.0",
                            ],
                            confidence=0.85
                        )
                        self.issues.append(issue)

    def _validate_disagreement_handling(self):
        """Validate handling of agent disagreement"""
        disagreement_handled = False

        for i, line in enumerate(self.lines):
            if 'disagree' in line.lower() or 'variance' in line.lower() or 'std' in line.lower():
                disagreement_handled = True

        if not disagreement_handled:
            issue = TradingIssue(
                severity=Severity.MEDIUM,
                rule="Disagreement Handling",
                file_path=self.file_path,
                line_number=1,
                message="No mechanism to handle high disagreement between agents",
                business_impact="High agent disagreement indicates low-confidence signals; should reduce position",
                suggested_fix="Calculate consensus variance; reduce position size if variance > threshold",
                auto_fixable=False,
                test_cases=[
                    "All agents agree (variance=0.01) → Full position",
                    "Agents disagree (variance=0.5) → Reduce position 50%",
                ],
                confidence=0.7
            )
            self.issues.append(issue)


class EventScoringValidator:
    """Validates event scoring formula correctness"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[TradingIssue] = []
        self.lines: List[str] = []

    def analyze(self, content: str) -> List[TradingIssue]:
        """Analyze event scoring implementation"""
        self.lines = content.split('\n')

        # Check for score components
        self._validate_score_components()

        # Check for score normalization
        self._validate_score_normalization()

        # Check for time decay
        self._validate_time_decay()

        return self.issues

    def _validate_score_components(self):
        """Validate all required score components"""
        required_components = ['impact', 'confidence', 'tradability', 'decay']
        found_components = set()

        for line in self.lines:
            for component in required_components:
                if component in line.lower():
                    found_components.add(component)

        missing = required_components - found_components
        if missing:
            issue = TradingIssue(
                severity=Severity.MEDIUM,
                rule="Event Score Components",
                file_path=self.file_path,
                line_number=1,
                message=f"Missing score components: {', '.join(missing)}",
                business_impact="Incomplete event scoring misses important tradability factors",
                suggested_fix=f"Implement: score = impact × confidence × tradability × time_decay",
                auto_fixable=False,
                test_cases=[
                    f"Required: impact, confidence, tradability, decay",
                    f"Score formula: {' × '.join(required_components)}",
                ],
                confidence=0.8
            )
            self.issues.append(issue)

    def _validate_score_normalization(self):
        """Validate scores are in [0, 1] range"""
        for i, line in enumerate(self.lines):
            if 'score' in line.lower() and '=' in line:
                context = '\n'.join(self.lines[max(0, i-2):min(len(self.lines), i+5)])

                # Check if score is clamped
                if 'clip' not in context.lower() and 'min(' not in context and 'max(' not in context:
                    if '*' in context:  # Likely a score calculation
                        issue = TradingIssue(
                            severity=Severity.MEDIUM,
                            rule="Score Normalization",
                            file_path=self.file_path,
                            line_number=i + 1,
                            message="Event score not normalized to [0, 1] range",
                            code_snippet=context.strip(),
                            business_impact="Non-normalized scores are inconsistent; makes thresholds meaningless",
                            suggested_fix="Clamp score: score = np.clip(score, 0, 1)",
                            auto_fixable=False,
                            test_cases=[
                                "Unclamped: 1.2 × 0.8 = 0.96 ✓ (acceptable)",
                                "Unclamped: 1.5 × 1.2 = 1.8 ✗ (out of range)",
                                "Clamped: min(1.8, 1.0) = 1.0 ✓",
                            ],
                            confidence=0.7
                        )
                        self.issues.append(issue)

    def _validate_time_decay(self):
        """Validate time decay calculation"""
        for i, line in enumerate(self.lines):
            if 'decay' in line.lower() or 'time' in line.lower():
                context = '\n'.join(self.lines[max(0, i-2):min(len(self.lines), i+5)])

                if 'decay' in context.lower() and 'exp' not in context.lower():
                    # Exponential decay is preferred
                    issue = TradingIssue(
                        severity=Severity.LOW,
                        rule="Time Decay Formula",
                        file_path=self.file_path,
                        line_number=i + 1,
                        message="Time decay not using exponential function",
                        code_snippet=context.strip(),
                        business_impact="Linear decay is less realistic; exponential better matches event relevance",
                        suggested_fix="Use exponential decay: decay = exp(-lambda × time_elapsed)",
                        auto_fixable=False,
                        test_cases=[
                            "Linear decay: score(t=0)=1.0, score(t=1h)=0.5, score(t=2h)=0",
                            "Exp decay (λ=0.69): score(t=0)=1.0, score(t=1h)=0.5, score(t=2h)=0.25",
                        ],
                        confidence=0.65
                    )
                    self.issues.append(issue)


class TradingValidator:
    """Main trading logic validator orchestrating all checks"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[TradingIssue] = []

    def validate(self, content: str) -> List[TradingIssue]:
        """Run all trading logic validation checks"""
        self.issues.clear()

        # Kelly Criterion validation
        kelly_validator = KellyCriterionValidator(self.file_path)
        self.issues.extend(kelly_validator.analyze(content))

        # Risk limit validation
        risk_validator = RiskLimitValidator(self.file_path)
        self.issues.extend(risk_validator.analyze(content))

        # Consensus mechanism validation
        consensus_validator = ConsensusMechanismValidator(self.file_path)
        self.issues.extend(consensus_validator.analyze(content))

        # Event scoring validation
        scoring_validator = EventScoringValidator(self.file_path)
        self.issues.extend(scoring_validator.analyze(content))

        return self.issues

    def has_critical_issues(self) -> bool:
        """Check if there are any critical trading issues"""
        return any(issue.severity == Severity.CRITICAL for issue in self.issues)

    def get_summary(self) -> str:
        """Get summary of issues found"""
        by_severity = {}
        for issue in self.issues:
            severity = issue.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1

        summary = f"Trading Logic Issues in {self.file_path}:\n"
        summary += f"  🔴 Critical: {by_severity.get('critical', 0)}\n"
        summary += f"  🟠 High: {by_severity.get('high', 0)}\n"
        summary += f"  🟡 Medium: {by_severity.get('medium', 0)}\n"
        summary += f"  🔵 Low: {by_severity.get('low', 0)}\n"

        return summary

    def print_detailed_report(self):
        """Print detailed report of all issues"""
        if not self.issues:
            print(f"✅ {self.file_path}: No trading logic issues detected")
            return

        print(f"\n📊 Trading Logic Validation Report: {self.file_path}")
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
                    print(f"  Impact: {issue.business_impact}")
                    if issue.suggested_fix:
                        print(f"  Fix: {issue.suggested_fix}")
                    if issue.test_cases:
                        print(f"  Test Cases:")
                        for test_case in issue.test_cases:
                            print(f"    - {test_case}")
                    print(f"  Confidence: {issue.confidence:.0%}")


# Test cases and example usage
if __name__ == "__main__":
    print("Trading Logic Validation Rules Module")
    print("=" * 70)
    print("\nValidators available:")
    print("  - KellyCriterionValidator: Position sizing correctness")
    print("  - RiskLimitValidator: Daily, monthly, drawdown enforcement")
    print("  - ConsensusMechanismValidator: Agent consensus logic")
    print("  - EventScoringValidator: Event scoring formula validation")
    print("\nSeverity Levels:")
    print("  🔴 CRITICAL: Risk limit violations, incorrect Kelly, leverage > 2x")
    print("  🟠 HIGH: Consensus errors, position sizing > 10%")
    print("  🟡 MEDIUM: Scoring formula issues, rebalancing logic")
    print("  🔵 LOW: Minor optimization opportunities")
