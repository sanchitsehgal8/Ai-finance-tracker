from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, datetime


@dataclass
class Group:
    id: Optional[str]
    owner_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GroupMember:
    id: Optional[str]
    group_id: str
    user_id: str
    joined_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GroupExpense:
    id: Optional[str]
    group_id: str
    payer_id: str
    amount: float
    description: Optional[str]
    date: date
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ExpenseShare:
    id: Optional[str]
    expense_id: str
    user_id: str
    share_amount: float
    settled: bool = False
