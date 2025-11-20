from typing import Optional


class Category:
    """Transaction category model representing income or expense categories.

    Encapsulates name, type ('income' or 'expense') and an optional icon.
    """

    def __init__(self, name: str, category_type: str, icon: str = "💰"):
        if category_type not in ('income', 'expense'):
            raise ValueError("category_type must be 'income' or 'expense'")
        if not name:
            raise ValueError("name must be provided")
        self._name = name
        self._type = category_type
        self._icon = icon
        self._id: Optional[str] = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def icon(self) -> str:
        return self._icon

    def to_dict(self) -> dict:
        return {"name": self._name, "type": self._type, "icon": self._icon}
from typing import Optional


class Category:
    """Transaction category model."""

    def __init__(self, name: str, category_type: str, icon: str = "💰"):
        self._name = name
        self._type = category_type  # 'income' or 'expense'
        self._icon = icon
        self._id: Optional[str] = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type
