from typing import Optional, Dict, List
from .base_repository import BaseRepository


class AlertRepository(BaseRepository):
    """Repository for alerts table operations."""

    def create(self, alert_data: Dict) -> Optional[Dict]:
        try:
            response = self.client.table('alerts').insert(alert_data).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None

    def list_for_user(self, user_id: str, unread_only: bool = False) -> List[Dict]:
        try:
            q = self.client.table('alerts').select('*').eq('user_id', user_id)
            if unread_only:
                q = q.eq('is_read', False)
            response = q.execute()
            return response.data or []
        except Exception:
            return []

    def mark_read(self, alert_id: str) -> bool:
        try:
            self.client.table('alerts').update({'is_read': True}).eq('id', alert_id).execute()
            return True
        except Exception:
            return False
