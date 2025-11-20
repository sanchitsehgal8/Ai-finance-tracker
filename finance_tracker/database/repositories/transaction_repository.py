from typing import List, Dict, Optional
from .base_repository import BaseRepository


class TransactionRepository(BaseRepository):
    """Repository for transaction data access using Supabase tables.

    Methods return raw dicts from Supabase responses. Caller should handle None.
    """

    def create(self, transaction_data: Dict) -> Optional[Dict]:
        try:
            response = self.client.table('transactions').insert(transaction_data).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None

    def get_by_user(self, user_id: str, limit: int = 100) -> List[Dict]:
        try:
            response = self.client.table('transactions').select("*, categories(*)").eq('user_id', user_id).order('date', desc=True).limit(limit).execute()
            return response.data or []
        except Exception:
            return []

    def get_by_date_range(self, user_id: str, start_date: str, end_date: str) -> List[Dict]:
        try:
            response = self.client.table('transactions').select('*').eq('user_id', user_id).gte('date', start_date).lte('date', end_date).execute()
            return response.data or []
        except Exception:
            return []

    def update(self, transaction_id: str, data: Dict) -> Optional[Dict]:
        try:
            response = self.client.table('transactions').update(data).eq('id', transaction_id).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None

    def delete(self, transaction_id: str) -> bool:
        try:
            self.client.table('transactions').delete().eq('id', transaction_id).execute()
            return True
        except Exception:
            return False
