from typing import List, Dict, Optional
from datetime import date
from database.repositories.group_repository import GroupRepository


class GroupService:
    """Business logic for group expenses (Splitwise-like features)."""

    def __init__(self, repo: Optional[GroupRepository] = None):
        self.repo = repo or GroupRepository()

    def create_group(self, owner_id: str, name: str, description: Optional[str] = None) -> Optional[Dict]:
        # If repo uses Supabase client and it's not configured, return informative error
        if hasattr(self.repo, 'client') and not getattr(self.repo, 'client'):
            return {"error": "no_client", "message": "Supabase client not configured. Set SUPABASE_URL and SUPABASE_KEY or enable dev bypass."}
        payload = {"owner_id": owner_id, "name": name, "description": description}
        return self.repo.create_group(payload)

    def add_member(self, group_id: str, user_id: str) -> Optional[Dict]:
        if hasattr(self.repo, 'client') and not getattr(self.repo, 'client'):
            return {"error": "no_client", "message": "Supabase client not configured. Set SUPABASE_URL and SUPABASE_KEY or enable dev bypass."}
        payload = {"group_id": group_id, "user_id": user_id}
        return self.repo.add_member(payload)

    def list_group_members(self, group_id: str) -> List[str]:
        """Return list of user_ids for a group."""
        members = self.repo.get_members_for_group(group_id)
        return [m.get('user_id') for m in (members or [])]

    def add_expense(self, group_id: str, payer_id: str, amount: float, date_obj: date, description: Optional[str], shares: List[Dict]) -> Optional[Dict]:
        if hasattr(self.repo, 'client') and not getattr(self.repo, 'client'):
            return {"error": "no_client", "message": "Supabase client not configured. Set SUPABASE_URL and SUPABASE_KEY or enable dev bypass."}

        expense = {
            "group_id": group_id,
            "payer_id": payer_id,
            "amount": float(amount),
            "description": description,
            "date": date_obj.isoformat(),
        }
        created = self.repo.create_expense(expense)
        if not created:
            return None
        expense_id = created.get('id')
        # attach expense_id to each share and insert
        for s in shares:
            s['expense_id'] = expense_id
        ok = self.repo.add_shares(shares)
        return created if ok else None

    def compute_group_balances(self, group_id: str) -> Dict[str, float]:
        """Return a map user_id -> net balance (positive = owed to user)."""
        expenses = self.repo.get_expenses_for_group(group_id)
        balances: Dict[str, float] = {}
        for exp in expenses:
            expense_id = exp.get('id')
            payer = exp.get('payer_id')
            amount = float(exp.get('amount', 0) or 0)
            shares = self.repo.get_shares_for_expense(expense_id)
            # sum of shares might not exactly match amount; use share amounts
            for s in shares:
                uid = s.get('user_id')
                share_amt = float(s.get('share_amount', 0) or 0)
                # each user owes share_amt to the payer (payer has positive)
                balances[uid] = balances.get(uid, 0.0) - share_amt
                balances[payer] = balances.get(payer, 0.0) + share_amt
        return balances
