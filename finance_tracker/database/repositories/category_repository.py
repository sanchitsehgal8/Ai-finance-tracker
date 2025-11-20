from typing import Optional, Dict, List
from .base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    """Repository for categories table operations."""

    def create(self, category_data: Dict) -> Optional[Dict]:
        try:
            response = self.client.table('categories').insert(category_data).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None

    def get_by_user(self, user_id: str) -> List[Dict]:
        try:
            response = self.client.table('categories').select('*').eq('user_id', user_id).execute()
            return response.data or []
        except Exception:
            return []

    def find_or_create(self, user_id: str, name: str, type: str, icon: str = '💰') -> Optional[Dict]:
        try:
            existing = self.client.table('categories').select('*').eq('user_id', user_id).eq('name', name).execute()
            if existing.data:
                return existing.data[0]
            payload = {'user_id': user_id, 'name': name, 'type': type, 'icon': icon}
            response = self.client.table('categories').insert(payload).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None
