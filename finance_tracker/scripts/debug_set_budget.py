"""Debug helper: attempt to create a budget via the service and print results.

Run from project root with your venv activated:
    python scripts\debug_set_budget.py
"""
import os
import sys
import uuid
from datetime import date
from pathlib import Path

# Ensure project root is on sys.path so `services` package can be imported when running this script
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.budget_service import BudgetService


def main():
    # Example values — replace with real values from your app if needed
    user_id = os.getenv('DEV_USER_ID') or os.getenv('SUPABASE_TEST_USER') or None
    if not user_id:
        print('Warning: DEV_USER_ID or SUPABASE_TEST_USER env var not set — using placeholder UUID')
        user_id = str(uuid.uuid4())

    category_id = os.getenv('DEV_CATEGORY_ID') or None
    monthly_limit = 1000.0
    month = date.today().isoformat()

    svc = BudgetService()
    print('Calling BudgetService.set_budget with:')
    print('  user_id:', user_id)
    print('  category_id:', category_id)
    print('  monthly_limit:', monthly_limit)
    print('  month:', month)

    res = svc.set_budget(user_id, category_id, monthly_limit, month)
    print('Result:', res)


if __name__ == '__main__':
    main()
