from typing import List, Optional
from datetime import datetime


class User:
    """Base User class."""

    def __init__(self, user_id: str, name: str, email: str):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._created_at = datetime.now()

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email


class IndividualUser(User):
    """Individual user account."""

    def __init__(self, user_id: str, name: str, email: str):
        super().__init__(user_id, name, email)
        self._account_type = "individual"


class FamilyAccount(User):
    """Family shared account with members."""

    def __init__(self, user_id: str, name: str, email: str):
        super().__init__(user_id, name, email)
        self._account_type = "family"
        self._members: List[str] = []

    def add_member(self, member_id: str):
        if member_id not in self._members:
            self._members.append(member_id)

    def remove_member(self, member_id: str):
        if member_id in self._members:
            self._members.remove(member_id)
