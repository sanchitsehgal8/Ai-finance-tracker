from typing import Optional, Dict, List
from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    """Repository handling user profile interactions."""

    def create_profile(self, profile: Dict) -> Optional[Dict]:
        try:
            response = self.client.table('user_profiles').insert(profile).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None

    def get_profile(self, user_id: str) -> Optional[Dict]:
        try:
            response = self.client.table('user_profiles').select('*').eq('id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None

    def update_profile(self, user_id: str, data: Dict) -> Optional[Dict]:
        try:
            response = self.client.table('user_profiles').update(data).eq('id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception:
            return None

    def list_profiles(self, limit: int = 100) -> List[Dict]:
        try:
            response = self.client.table('user_profiles').select('*').limit(limit).execute()
            return response.data or []
        except Exception:
            return []
