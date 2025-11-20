import pytest

def test_repository_sanity():
    # Repositories rely on Supabase client; basic import test
    from database.repositories.transaction_repository import TransactionRepository
    repo = TransactionRepository()
    assert repo is not None
