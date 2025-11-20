import datetime


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def iso_date(dt: datetime.date) -> str:
    return dt.isoformat()
