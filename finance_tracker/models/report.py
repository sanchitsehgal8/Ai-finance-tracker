from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import pandas as pd


class Report(ABC):
    """Abstract base class for reports."""

    def __init__(self, user_id: str):
        self._user_id = user_id
        self._data: Optional[pd.DataFrame] = None

    @abstractmethod
    def generate(self, transactions: List[Dict]) -> Dict:
        """Generate report data from transactions list."""
        raise NotImplementedError()

    @abstractmethod
    def format_output(self) -> str:
        raise NotImplementedError()


class MonthlyReport(Report):
    """Monthly financial report."""

    def __init__(self, user_id: str, month: int, year: int):
        super().__init__(user_id)
        self._month = month
        self._year = year

    def generate(self, transactions: List[Dict]) -> Dict:
        df = pd.DataFrame(transactions)
        if df.empty:
            return {'income': 0.0, 'expense': 0.0, 'breakdown': {}}
        df['date'] = pd.to_datetime(df['date'])
        mask = (df['date'].dt.month == self._month) & (df['date'].dt.year == self._year)
        subset = df.loc[mask]
        income = subset.loc[subset['transaction_type'] == 'income', 'amount'].sum()
        expense = subset.loc[subset['transaction_type'] == 'expense', 'amount'].sum()
        breakdown = subset.groupby('category').amount.sum().to_dict() if not subset.empty else {}
        return {'income': float(income), 'expense': float(expense), 'breakdown': breakdown}

    def format_output(self) -> str:
        return f"Monthly Report for {self._month}/{self._year}"


class YearlyReport(Report):
    """Yearly financial report."""

    def __init__(self, user_id: str, year: int):
        super().__init__(user_id)
        self._year = year

    def generate(self, transactions: List[Dict]) -> Dict:
        df = pd.DataFrame(transactions)
        if df.empty:
            return {'income': 0.0, 'expense': 0.0, 'monthly': {}}
        df['date'] = pd.to_datetime(df['date'])
        mask = df['date'].dt.year == self._year
        subset = df.loc[mask]
        income = subset.loc[subset['transaction_type'] == 'income', 'amount'].sum()
        expense = subset.loc[subset['transaction_type'] == 'expense', 'amount'].sum()
        monthly = subset.groupby(subset['date'].dt.month).amount.sum().to_dict() if not subset.empty else {}
        return {'income': float(income), 'expense': float(expense), 'monthly': monthly}

    def format_output(self) -> str:
        return f"Yearly Report for {self._year}"
