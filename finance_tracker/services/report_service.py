from typing import List, Dict
from models.report import MonthlyReport, YearlyReport


class ReportService:
    """Report generation logic."""

    def generate_monthly(self, user_id: str, month: int, year: int, transactions: List[Dict]) -> Dict:
        report = MonthlyReport(user_id, month, year)
        return report.generate(transactions)

    def generate_yearly(self, user_id: str, year: int, transactions: List[Dict]) -> Dict:
        report = YearlyReport(user_id, year)
        return report.generate(transactions)
