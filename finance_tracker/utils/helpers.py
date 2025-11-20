from typing import Any


def safe_get(d: dict, key: str, default: Any = None):
    try:
        return d.get(key, default)
    except Exception:
        return default
