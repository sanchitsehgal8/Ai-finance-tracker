from typing import Dict, Optional


class Budget:
    """Budget management class."""

    def __init__(self, user_id: str, monthly_limit: float):
        self._user_id = user_id
        self._monthly_limit = monthly_limit
        self._category_limits: Dict[str, float] = {}
        self._id: Optional[str] = None

    def set_category_limit(self, category: str, limit: float):
        """Set spending limit for a category."""
        if limit <= 0:
            raise ValueError("Limit must be positive")
        self._category_limits[category] = limit

    def check_limit(self, category: str, amount: float) -> bool:
        """Check if amount exceeds category limit."""
        if category in self._category_limits:
            return amount <= self._category_limits[category]
        return True

    def get_remaining_budget(self, category: str, spent: float) -> float:
        """Calculate remaining budget for category."""
        if category in self._category_limits:
            return max(0.0, self._category_limits[category] - spent)
        return 0.0
