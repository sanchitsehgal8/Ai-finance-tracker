from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from utils.formatters import format_currency


class Transaction(ABC):
    """Abstract base class for all transactions.

    Attributes are encapsulated with properties to enforce validation.
    """

    def __init__(self, amount: float, date: datetime, category: str, description: str, user_id: str):
        self._amount = amount
        self._date = date
        self._category = category
        self._description = description
        self._user_id = user_id
        self._id: Optional[str] = None

    @abstractmethod
    def get_summary(self) -> str:
        """Return formatted transaction summary."""
        raise NotImplementedError()

    @abstractmethod
    def validate(self) -> bool:
        """Validate transaction data."""
        raise NotImplementedError()

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float):
        if value <= 0:
            raise ValueError("Amount must be positive")
        self._amount = value

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, value: datetime):
        if not isinstance(value, datetime):
            raise ValueError("date must be a datetime")
        self._date = value


class Income(Transaction):
    """Concrete Income class."""

    def get_summary(self) -> str:
        return f"Income: {format_currency(self._amount)} from {self._category} on {self._date.strftime('%Y-%m-%d')}"

    def validate(self) -> bool:
        return self._amount > 0 and self._category is not None


class Expense(Transaction):
    """Concrete Expense class."""

    def get_summary(self) -> str:
        return f"Expense: {format_currency(self._amount)} for {self._category} on {self._date.strftime('%Y-%m-%d')}"

    def validate(self) -> bool:
        return self._amount > 0 and self._category is not None
