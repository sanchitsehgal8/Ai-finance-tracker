from typing import Optional, Dict, List
from database.repositories.budget_repository import BudgetRepository
from database.repositories.alert_repository import AlertRepository


class BudgetService:
    """Budget checking and alerts."""

    def __init__(self):
        self.repo = BudgetRepository()
        self.alert_repo = AlertRepository()

    def set_budget(self, user_id: str, category_id: str, monthly_limit: float, month: str) -> Optional[Dict]:
        try:
            payload = {'user_id': user_id, 'category_id': category_id, 'monthly_limit': monthly_limit, 'month': month}
            return self.repo.create(payload)
        except Exception:
            return None

    def get_budget_status(self, user_id: str) -> float:
        # Placeholder: compute percentage of budgets used. Returns a percent.
        budgets = self.repo.get_by_user(user_id)
        if not budgets:
            return 0.0
        used_pct = 0.0
        try:
            total_limits = sum([float(b.get('monthly_limit', 0)) for b in budgets])
            # In real app, replace with actual spent calculation
            total_spent = total_limits * 0.5
            used_pct = (total_spent / total_limits) * 100 if total_limits > 0 else 0.0
        except Exception:
            used_pct = 0.0
        return round(used_pct, 2)

    def check_and_alert(self, user_id: str, category: str, overage_amount: float):
        # Create an alert when budget overage occurs
        payload = {'user_id': user_id, 'alert_type': 'budget', 'message': f'Budget overage in {category}', 'priority': 'HIGH'}
        return self.alert_repo.create(payload)
