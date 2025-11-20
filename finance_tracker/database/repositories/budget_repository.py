from typing import Optional, Dict, List
from .base_repository import BaseRepository


class BudgetRepository(BaseRepository):
    """Repository for budgets table operations."""

    def create(self, budget_data: Dict) -> Optional[Dict]:
        try:
            response = self.client.table('budgets').insert(budget_data).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None

    def get_by_user(self, user_id: str) -> List[Dict]:
        try:
            response = self.client.table('budgets').select('*').eq('user_id', user_id).execute()
            return response.data or []
        except Exception:
            return []

    def update(self, budget_id: str, data: Dict) -> Optional[Dict]:
        try:
            response = self.client.table('budgets').update(data).eq('id', budget_id).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None

    def delete(self, budget_id: str) -> bool:
        try:
            self.client.table('budgets').delete().eq('id', budget_id).execute()
            return True
        except Exception:
            return False
