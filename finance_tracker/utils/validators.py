from datetime import datetime


def validate_amount(value) -> bool:
    try:
        v = float(value)
        return v > 0
    except Exception:
        return False


def validate_date(value) -> bool:
    if isinstance(value, datetime):
        return True
    try:
        datetime.fromisoformat(str(value))
        return True
    except Exception:
        return False
