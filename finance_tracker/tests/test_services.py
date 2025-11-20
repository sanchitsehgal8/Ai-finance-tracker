import pytest
from services.transaction_service import TransactionService


def test_transaction_service_methods():
    svc = TransactionService()
    # Methods should not raise when client is not configured; they return sensible defaults
    txns = svc.get_recent_transactions('no-user')
    assert isinstance(txns, list)
    # Adding a transaction with no category should attempt auto-categorization
    res = svc.add_transaction('no-user', 1.23, '2025-01-01', None, 'expense', 'Test coffee purchase')
    # We can't assert persistence without Supabase configured, but the call should not raise
    assert (res is None) or isinstance(res, dict)
