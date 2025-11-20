from typing import List, Dict, Optional
from database.repositories.transaction_repository import TransactionRepository
from database.repositories.category_repository import CategoryRepository
from datetime import datetime


class TransactionService:
    """Business logic for transactions.

    This service integrates optional ML-based auto-categorization. If a
    `category` is not provided when adding a transaction, the service will try
    to load `ai_modules.TransactionClassifier` and predict a category from the
    transaction description. The classifier is optional — the service falls
    back gracefully when models or dependencies are not available.
    """

    def __init__(self):
        self.repo = TransactionRepository()
        self.cat_repo = CategoryRepository()

    def add_transaction(self, user_id: str, amount: float, date: str, category: Optional[str], transaction_type: str, description: str = '') -> Optional[Dict]:
        """Create a transaction record.

        If `category` is falsy, attempt to auto-categorize using the trained
        classifier. Returns the created transaction dict or `None` on failure.
        """
        try:
            # Auto-categorize when category not provided
            if not category:
                try:
                    from ai_modules import TransactionClassifier
                except Exception:
                    # TransactionClassifier import may be via package; try direct
                    try:
                        from ai_modules.transaction_classifier import TransactionClassifier
                    except Exception:
                        TransactionClassifier = None

                predicted = None
                if TransactionClassifier:
                    try:
                        clf = TransactionClassifier(model_dir='ai_modules/models')
                        predicted = clf.predict(description)
                    except Exception:
                        predicted = None
                category = predicted or 'Uncategorized'

            # Ensure category exists (may create)
            cat = self.cat_repo.find_or_create(user_id, category, transaction_type)
            payload = {
                'user_id': user_id,
                'category_id': cat.get('id') if cat else None,
                'amount': amount,
                'transaction_type': transaction_type,
                'description': description,
                'date': date
            }
            return self.repo.create(payload)
        except Exception:
            return None

    def get_recent_transactions(self, user_id: str, limit: int = 100) -> List[Dict]:
        return self.repo.get_by_user(user_id, limit)

    def get_category_breakdown(self, user_id: str) -> List[Dict]:
        # Aggregation should ideally be done server-side; provide client-side fallback
        txns = self.get_recent_transactions(user_id, limit=500)
        agg = {}
        for t in txns:
            if t.get('transaction_type') != 'expense':
                continue
            cat = t.get('category') or (t.get('categories') and t.get('categories').get('name'))
            if not cat:
                cat = 'Uncategorized'
            agg[cat] = agg.get(cat, 0) + float(t.get('amount', 0))
        return [{'category': k, 'amount': v} for k, v in agg.items()]

    def get_monthly_comparison(self, user_id: str) -> Dict:
        txns = self.get_recent_transactions(user_id, limit=1000)
        import pandas as pd
        if not txns:
            return {'month': [], 'income': [], 'expense': []}
        df = pd.DataFrame(txns)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M').astype(str)
        grouped = df.groupby(['month', 'transaction_type']).amount.sum().unstack(fill_value=0)
        months = list(grouped.index)
        income = grouped.get('income', None)
        expense = grouped.get('expense', None)
        return {
            'month': months,
            'income': income.tolist() if income is not None else [0]*len(months),
            'expense': expense.tolist() if expense is not None else [0]*len(months)
        }
