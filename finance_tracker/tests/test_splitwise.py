from services.group_service import GroupService
from typing import List, Dict
from datetime import date


class InMemoryRepo:
    def __init__(self):
        self.groups = {}
        self.members = []
        self.expenses = {}
        self.shares = []
        self._id = 1

    def _new_id(self):
        self._id += 1
        return f"id_{self._id}"

    def create_group(self, group_data: Dict):
        gid = self._new_id()
        group = {**group_data, 'id': gid}
        self.groups[gid] = group
        return group

    def add_member(self, member_data: Dict):
        mid = self._new_id()
        m = {**member_data, 'id': mid}
        self.members.append(m)
        return m

    def create_expense(self, expense_data: Dict):
        eid = self._new_id()
        exp = {**expense_data, 'id': eid}
        self.expenses[eid] = exp
        return exp

    def add_shares(self, shares: List[Dict]):
        for s in shares:
            srec = {**s, 'id': self._new_id()}
            self.shares.append(srec)
        return True

    def list_groups_for_user(self, user_id: str):
        gids = [m['group_id'] for m in self.members if m['user_id'] == user_id]
        return [self.groups[g] for g in gids]

    def get_expenses_for_group(self, group_id: str):
        return [e for e in self.expenses.values() if e['group_id'] == group_id]

    def get_shares_for_expense(self, expense_id: str):
        return [s for s in self.shares if s['expense_id'] == expense_id]


def test_group_balances_equal_split():
    repo = InMemoryRepo()
    svc = GroupService(repo=repo)
    owner = 'u1'
    g = svc.create_group(owner_id=owner, name='Trip')
    gid = g['id']
    svc.add_member(gid, 'u1')
    svc.add_member(gid, 'u2')
    svc.add_member(gid, 'u3')
    # u1 pays 300 split equally => each share 100
    shares = [{'user_id': 'u1', 'share_amount': 100.0}, {'user_id': 'u2', 'share_amount': 100.0}, {'user_id': 'u3', 'share_amount': 100.0}]
    svc.add_expense(group_id=gid, payer_id='u1', amount=300.0, date_obj=date.today(), description='Dinner', shares=shares)
    balances = svc.compute_group_balances(gid)
    # u1 should be +200 (others owe 100 each), u2 -100, u3 -100
    assert round(balances.get('u1', 0), 2) == 200.0
    assert round(balances.get('u2', 0), 2) == -100.0
    assert round(balances.get('u3', 0), 2) == -100.0
