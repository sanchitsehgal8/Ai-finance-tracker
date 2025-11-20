from abc import ABC, abstractmethod
from datetime import datetime


class Alert(ABC):
    """Abstract alert class."""

    def __init__(self, user_id: str, message: str):
        self._user_id = user_id
        self._message = message
        self._created_at = datetime.now()
        self._is_read = False

    @abstractmethod
    def get_priority(self) -> str:
        raise NotImplementedError()


class BudgetAlert(Alert):
    """Alert for budget overages."""

    def __init__(self, user_id: str, message: str, category: str, overage_amount: float):
        super().__init__(user_id, message)
        self._category = category
        self._overage_amount = overage_amount

    def get_priority(self) -> str:
        if self._overage_amount > 100:
            return "HIGH"
        return "MEDIUM"


class BillReminder(Alert):
    """Reminder for upcoming bills."""

    def __init__(self, user_id: str, message: str, bill_name: str, due_date: datetime):
        super().__init__(user_id, message)
        self._bill_name = bill_name
        self._due_date = due_date

    def get_priority(self) -> str:
        days_until_due = (self._due_date - datetime.now()).days
        if days_until_due <= 3:
            return "HIGH"
        return "LOW"
