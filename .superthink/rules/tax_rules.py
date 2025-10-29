"""
Tax accuracy validation rules for Superthink-Code-Analyzer.
Ensures trading tax calculations are correct and compliant.
"""

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TaxIssue:
    """Represents a detected tax accuracy issue."""
    severity: str  # critical, high, medium, low
    rule: str
    file_path: str
    line_number: int
    message: str
    test_case: Optional[str] = None
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False


class TaxValidator:
    """Validates tax calculation correctness."""

    # Tax rate constants
    TAX_RATES = {
        'short_term': 0.37,  # Ordinary income rates, max federal
        'long_term': 0.20,   # LTCG rates
        'section_1256': 0.268,  # 60/40 blend
        'niit': 0.038,  # Net Investment Income Tax
    }

    # Validation thresholds
    THRESHOLDS = {
        'holding_period_ltcg': 365,  # Days to qualify as long-term
        'wash_sale_window': 61,  # Total days in wash sale window (30 before + 30 after)
        'tax_calculation_error': 0.01,  # 1% tolerance for rounding
    }

    def validate_tax_lot_tracking(self, file_path: str, content: str) -> List[TaxIssue]:
        """Validate tax lot tracking implementation."""
        issues = []
        lines = content.split('\n')

        # Check for FIFO implementation
        for i, line in enumerate(lines, 1):
            if 'FIFO' in line and '=' in line:
                # Check if implementation looks reasonable
                if not any(check in content[max(0, i*50-200):(i*50)+200] for check in
                          ['first', 'pop(0)', '[0]', 'queue']):
                    issue = TaxIssue(
                        severity='high',
                        rule='tax_lot_fifo_implementation',
                        file_path=file_path,
                        line_number=i,
                        message='FIFO implementation may be incorrect. Check that first-in items are sold first.',
                        test_case='FIFO([lot1, lot2, lot3], 2) should return [lot1, lot2]',
                        suggested_fix='Use collections.deque and popleft() for FIFO',
                        auto_fixable=False,
                    )
                    issues.append(issue)

        # Check for cost basis calculation
        if 'cost_basis' in content.lower():
            for i, line in enumerate(lines, 1):
                if 'cost_basis' in line.lower() and '=' in line:
                    # Check if fees are included
                    if 'fee' not in content[max(0, i*50-300):(i*50)+300].lower():
                        issue = TaxIssue(
                            severity='critical',
                            rule='tax_lot_missing_fees',
                            file_path=file_path,
                            line_number=i,
                            message='Cost basis calculation may not include transaction fees',
                            test_case='cost_basis = purchase_price + fees. Example: buy 1 BTC at $45k + $20 fee = $45,020 cost basis',
                            suggested_fix='Include transaction fees in cost_basis = purchase_price + fees',
                            auto_fixable=False,
                        )
                        issues.append(issue)

        return issues

    def validate_wash_sale_detection(self, file_path: str, content: str) -> List[TaxIssue]:
        """Validate wash sale rule implementation."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for wash sale window calculation
            if 'wash_sale' in line.lower() or '30' in line and 'day' in line.lower():
                # Look for the window calculation nearby
                context = '\n'.join(lines[max(0, i-3):min(len(lines), i+3)])

                # Should check 30 days BEFORE and AFTER
                has_before = 'before' in context.lower() or '-30' in context
                has_after = 'after' in context.lower() or '+30' in context or 'and' in context

                if not (has_before and has_after):
                    issue = TaxIssue(
                        severity='critical',
                        rule='wash_sale_window_incomplete',
                        file_path=file_path,
                        line_number=i,
                        message='Wash sale window must check 30 days BEFORE AND 30 days AFTER the sale date',
                        test_case='If sell on day 100, check purchases on days 70-130 (both directions)',
                        suggested_fix='window_start = sale_date - 30 days\nwindow_end = sale_date + 30 days\ncheck_purchases(window_start, window_end)',
                        auto_fixable=False,
                    )
                    issues.append(issue)

        return issues

    def validate_ltcg_classification(self, file_path: str, content: str) -> List[TaxIssue]:
        """Validate long-term capital gains classification."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for holding period calculation
            if 'holding' in line.lower() and ('365' in line or 'year' in line.lower()):
                # Check if using > 365 or >= 365
                if '>= 365' in line or '> 365' not in line:
                    issue = TaxIssue(
                        severity='high',
                        rule='ltcg_holding_period_boundary',
                        file_path=file_path,
                        line_number=i,
                        message='LTCG requires >365 days (more than 1 year), not >= 365',
                        test_case='365 days held = short-term. 366 days held = long-term',
                        suggested_fix='Use: if holding_days > 365: return "LTCG"',
                        auto_fixable=True,
                    )
                    issues.append(issue)

            # Check for tax rate application
            if 'tax_rate' in line.lower() and 'ltcg' in line.lower():
                if '0.20' not in line and '20%' not in line and '20' not in line:
                    issue = TaxIssue(
                        severity='high',
                        rule='ltcg_tax_rate_incorrect',
                        file_path=file_path,
                        line_number=i,
                        message='LTCG tax rate for high earners should be 20% (0.20)',
                        test_case='LTCG tax = capital_gain * 0.20',
                        suggested_fix='ltcg_rate = 0.20',
                        auto_fixable=False,
                    )
                    issues.append(issue)

        return issues

    def validate_section_1256_treatment(self, file_path: str, content: str) -> List[TaxIssue]:
        """Validate Section 1256 contract treatment (60/40 rule)."""
        issues = []

        # Only validate files that deal with futures/options
        if 'futures' not in file_path.lower() and 'option' not in file_path.lower():
            return issues

        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            if '1256' in line or 'section' in line.lower():
                # Check if implementing 60/40 split
                context = '\n'.join(lines[max(0, i-3):min(len(lines), i+5)])

                if '0.60' not in context and '60%' not in context:
                    issue = TaxIssue(
                        severity='high',
                        rule='section_1256_missing_treatment',
                        file_path=file_path,
                        line_number=i,
                        message='Section 1256 contracts must use 60% long-term, 40% short-term treatment',
                        test_case='If contract gain = $100:\n  LTCG = $100 * 0.60 * 0.20 = $12 tax\n  STCG = $100 * 0.40 * 0.37 = $14.80 tax\n  Total = $26.80 tax',
                        suggested_fix='long_term_portion = gain * 0.60\nshort_term_portion = gain * 0.40\ntax = long_term_portion * 0.20 + short_term_portion * 0.37',
                        auto_fixable=False,
                    )
                    issues.append(issue)

        return issues

    def validate_realized_vs_unrealized(self, file_path: str, content: str) -> List[TaxIssue]:
        """Validate distinction between realized and unrealized gains."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for realized gain calculation
            if 'realized_gain' in line.lower():
                # Should only be calculated on sales
                context = '\n'.join(lines[max(0, i-2):min(len(lines), i+2)])

                if 'sale' not in context.lower() and 'exit' not in context.lower() and 'close' not in context.lower():
                    issue = TaxIssue(
                        severity='high',
                        rule='realized_gain_on_open_position',
                        file_path=file_path,
                        line_number=i,
                        message='Realized gains should only be calculated when position is closed/sold',
                        test_case='Open position: BTC bought at $40k, now worth $45k. Unrealized gain = $5k. Realized gain = $0 (not sold yet)',
                        suggested_fix='Only calculate realized_gain when position is closed: realized_gain = sale_price - cost_basis',
                        auto_fixable=False,
                    )
                    issues.append(issue)

        return issues

    def validate_year_end_planning(self, file_path: str, content: str) -> List[TaxIssue]:
        """Validate year-end tax planning implementation."""
        issues = []

        # Only check if file mentions tax planning
        if 'year_end' not in content.lower() and 'tax_plan' not in content.lower():
            return issues

        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            if 'harvest' in line.lower() and 'year' in line.lower():
                # Check for deadline awareness
                if '12/31' not in line and 'december 31' not in line.lower():
                    issue = TaxIssue(
                        severity='medium',
                        rule='tax_loss_harvesting_deadline',
                        file_path=file_path,
                        line_number=i,
                        message='Tax-loss harvesting must be completed by December 31st',
                        test_case='Trades must settle by 12/31 to count for that year',
                        suggested_fix='Add deadline check: if datetime.now().date() > datetime(year, 12, 31).date(): raise ValueError("Too late for tax-loss harvesting this year")',
                        auto_fixable=False,
                    )
                    issues.append(issue)

        return issues

    def validate_multi_year_loss_carryforward(self, file_path: str, content: str) -> List[TaxIssue]:
        """Validate loss carryforward across years."""
        issues = []

        if 'carryforward' not in content.lower() and 'carry_forward' not in content.lower():
            return issues

        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            if ('carry' in line.lower() or 'carry_forward' in line.lower()) and 'loss' in line.lower():
                # Check if tracking year-to-year
                context = '\n'.join(lines[max(0, i-3):min(len(lines), i+5)])

                if 'year' not in context.lower():
                    issue = TaxIssue(
                        severity='medium',
                        rule='loss_carryforward_year_tracking',
                        file_path=file_path,
                        line_number=i,
                        message='Loss carryforward must track which year losses originated',
                        test_case='Year 1 loss: $5,000 unused. Year 2: Use $3,000 against gains. $2,000 carries to Year 3.',
                        suggested_fix='Track by year: carryforward[year] = unused_losses',
                        auto_fixable=False,
                    )
                    issues.append(issue)

        return issues

    def run_all_validations(self, file_path: str, content: str) -> List[TaxIssue]:
        """Run all tax accuracy validations on a file."""
        all_issues = []

        all_issues.extend(self.validate_tax_lot_tracking(file_path, content))
        all_issues.extend(self.validate_wash_sale_detection(file_path, content))
        all_issues.extend(self.validate_ltcg_classification(file_path, content))
        all_issues.extend(self.validate_section_1256_treatment(file_path, content))
        all_issues.extend(self.validate_realized_vs_unrealized(file_path, content))
        all_issues.extend(self.validate_year_end_planning(file_path, content))
        all_issues.extend(self.validate_multi_year_loss_carryforward(file_path, content))

        return all_issues


def validate_tax(file_path: str, content: str) -> List[TaxIssue]:
    """Main entry point for tax validation."""
    validator = TaxValidator()
    return validator.run_all_validations(file_path, content)
