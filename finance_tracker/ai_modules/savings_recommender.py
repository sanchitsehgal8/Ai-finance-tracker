from typing import List, Dict


class SavingsRecommender:
    """Simple rule-based recommender for savings suggestions.

    In production this should use user's historical patterns and modelled forecasts.
    """

    def recommend(self, transactions: List[Dict], monthly_limit: float) -> List[Dict]:
        # Very simple heuristic: recommend categories with high spend as savings targets
        agg = {}
        for t in transactions:
            if t.get('transaction_type') == 'expense':
                cat = t.get('category') or (t.get('categories') and t.get('categories').get('name')) or 'Uncategorized'
                agg[cat] = agg.get(cat, 0) + float(t.get('amount', 0))
        # Sort categories by spend desc and recommend top 3
        items = sorted(agg.items(), key=lambda x: x[1], reverse=True)[:3]
        recs = []
        for cat, amt in items:
            recs.append({'category': cat, 'suggested_saving': round(min(amt * 0.1, monthly_limit * 0.05), 2)})
        return recs
