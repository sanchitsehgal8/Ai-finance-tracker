import datetime
from typing import Any


def _format_indian_number(n: int) -> str:
    """Format integer part using Indian numbering system (lakhs, crores).

    e.g. 12345678 -> '1,23,45,678'
    """
    s = str(n)
    if len(s) <= 3:
        return s
    last3 = s[-3:]
    rest = s[:-3]
    parts = []
    while len(rest) > 2:
        parts.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.insert(0, rest)
    return ",".join(parts) + "," + last3


def format_currency(value: Any, symbol: str = '₹') -> str:
    """Format a numeric value as currency using Indian grouping.

    Accepts numeric strings or numbers. Returns a string like '₹1,23,456.78'.
    """
    try:
        v = float(value)
    except Exception:
        return f"{symbol}0.00"
    sign = '-' if v < 0 else ''
    v = abs(v)
    int_part = int(v)
    dec_part = int(round((v - int_part) * 100))
    formatted_int = _format_indian_number(int_part)
    return f"{sign}{symbol}{formatted_int}.{dec_part:02d}"


def iso_date(dt: datetime.date) -> str:
    return dt.isoformat()
