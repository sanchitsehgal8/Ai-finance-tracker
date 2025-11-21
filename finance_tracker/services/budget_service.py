from typing import Optional, Dict, List
from database.repositories.budget_repository import BudgetRepository
from database.repositories.alert_repository import AlertRepository
import uuid


class BudgetService:
    """Budget checking and alerts."""

    def __init__(self):
        self.repo = BudgetRepository()
        self.alert_repo = AlertRepository()

    def set_budget(self, user_id: str, category_id: str, monthly_limit: float, month: str) -> Optional[Dict]:
        # Validate UUIDs for user_id and category_id (category_id may be None)
        try:
            if not user_id:
                return {'error': True, 'message': 'user_id is required'}
            try:
                uuid.UUID(str(user_id))
            except Exception:
                return {'error': True, 'message': 'Invalid user_id: must be a UUID'}

            if category_id:
                try:
                    uuid.UUID(str(category_id))
                except Exception:
                    return {'error': True, 'message': 'Invalid category_id: must be a UUID or left blank'}

            payload = {'user_id': user_id, 'category_id': category_id, 'monthly_limit': monthly_limit, 'month': month}
            res = self.repo.create(payload)
            # If repository returns structured error, pass it through
            if isinstance(res, dict) and res.get('error'):
                return res
            return res
        except Exception as exc:
            return {'error': True, 'message': str(exc)}

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
