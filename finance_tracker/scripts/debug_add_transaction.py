"""Debug helper to attempt adding a transaction via TransactionService.

Usage:
  .\.venv312\Scripts\Activate
  python scripts\debug_add_transaction.py

This will print the result returned by the service (success dict or None/error).
"""
from services.transaction_service import TransactionService
from datetime import date
import traceback

def main():
    svc = TransactionService()
    user_id = 'dev-user'
    try:
        res = svc.add_transaction(user_id=user_id, amount=123.45, date=date.today().isoformat(), category=None, transaction_type='expense', description='Debug test')
        print('Result:', res)
    except Exception as exc:
        print('Exception when calling add_transaction:')
        traceback.print_exc()

if __name__ == '__main__':
    main()
