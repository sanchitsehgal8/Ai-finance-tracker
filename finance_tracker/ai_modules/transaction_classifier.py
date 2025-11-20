from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from typing import List, Tuple, Optional
import os


class TransactionClassifier:
    """ML model for transaction categorization using RandomForest and TF-IDF."""

    def __init__(self, model_dir: str = 'finance_tracker/ai_modules/models'):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.model_path = os.path.join(model_dir, 'classifier.pkl')
        self.vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        os.makedirs(model_dir, exist_ok=True)
        self._load_models()

    def train(self, descriptions: List[str], categories: List[str]):
        X = self.vectorizer.fit_transform(descriptions)
        self.model.fit(X, categories)
        self._save_models()

    def predict(self, description: str) -> Optional[str]:
        try:
            X = self.vectorizer.transform([description])
            prediction = self.model.predict(X)
            return prediction[0]
        except Exception:
            return None

    def predict_proba(self, description: str) -> List[Tuple[str, float]]:
        X = self.vectorizer.transform([description])
        probabilities = self.model.predict_proba(X)[0]
        classes = self.model.classes_
        return list(zip(classes, probabilities))

    def _save_models(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(self.vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)

    def _load_models(self):
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
            except Exception:
                pass
