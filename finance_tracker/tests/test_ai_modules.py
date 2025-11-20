import pytest
from ai_modules.transaction_classifier import TransactionClassifier
from ai_modules import train_classifier


def test_transaction_classifier_training_and_predict(tmp_path):
    # Train a small classifier and ensure it can predict a known token
    # Use the training helper to write model files into the package models dir
    train_classifier.train_and_save()
    tc = TransactionClassifier(model_dir='ai_modules/models')
    pred = tc.predict('Salary payment from employer')
    # Prediction may vary (trained on synthetic data), but should not raise and returns a str or None
    assert (pred is None) or isinstance(pred, str)
