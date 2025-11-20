"""AI modules package for ML models and helpers.

SpendingPredictor is imported lazily because it depends on external
packages that may not be available in every environment.
"""

from .transaction_classifier import TransactionClassifier
from .savings_recommender import SavingsRecommender

# Optional import: Prophet is not required to use the classifier.
try:
	from .spending_predictor import SpendingPredictor
except Exception:
	SpendingPredictor = None

__all__ = ['TransactionClassifier', 'SavingsRecommender', 'SpendingPredictor']
