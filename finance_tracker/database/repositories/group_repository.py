from typing import List, Dict, Optional
from .base_repository import BaseRepository


class GroupRepository(BaseRepository):
    """Repository for group and group-expense related operations."""

    def create_group(self, group_data: Dict) -> Optional[Dict]:
        try:
            resp = self.client.table('groups').insert(group_data).execute()
            return resp.data[0] if resp.data else None
        except Exception:
            return None

    def add_member(self, member_data: Dict) -> Optional[Dict]:
        try:
            resp = self.client.table('group_members').insert(member_data).execute()
            return resp.data[0] if resp.data else None
        except Exception:
            return None

    def create_expense(self, expense_data: Dict) -> Optional[Dict]:
        try:
            resp = self.client.table('group_expenses').insert(expense_data).execute()
            return resp.data[0] if resp.data else None
        except Exception:
            return None

    def add_shares(self, shares: List[Dict]) -> bool:
        try:
            self.client.table('group_expense_shares').insert(shares).execute()
            return True
        except Exception:
            return False

    def list_groups_for_user(self, user_id: str) -> List[Dict]:
        try:
            resp = self.client.table('group_members').select('group_id').eq('user_id', user_id).execute()
            ids = [r['group_id'] for r in (resp.data or [])]
            if not ids:
                return []
            groups = self.client.table('groups').select('*').in_('id', ids).execute()
            return groups.data or []
        except Exception:
            return []

    def get_members_for_group(self, group_id: str) -> List[Dict]:
        try:
            resp = self.client.table('group_members').select('*').eq('group_id', group_id).execute()
            return resp.data or []
        except Exception:
            return []

    def get_expenses_for_group(self, group_id: str) -> List[Dict]:
        try:
            resp = self.client.table('group_expenses').select('*').eq('group_id', group_id).order('date', desc=True).execute()
            return resp.data or []
        except Exception:
            return []

    def get_shares_for_expense(self, expense_id: str) -> List[Dict]:
        try:
            resp = self.client.table('group_expense_shares').select('*').eq('expense_id', expense_id).execute()
            return resp.data or []
        except Exception:
            return []
