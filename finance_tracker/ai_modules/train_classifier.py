"""Small training script to build a sample transaction classifier.

This script trains a RandomForest + TF-IDF classifier on a tiny synthetic
dataset and writes model artifacts into `ai_modules/models/`.
"""
from ai_modules.transaction_classifier import TransactionClassifier


def make_sample_data():
    descriptions = [
        'Starbucks latte', 'Salary from ACME corp', 'Walmart groceries', 'Uber ride',
        'Paycheck deposit', 'Electricity bill payment', 'Dinner at Italian restaurant',
        'Gym membership', 'Movie tickets', 'Sold old bike on marketplace'
    ]
    categories = [
        'coffee', 'salary', 'groceries', 'transport',
        'salary', 'utilities', 'dining',
        'health', 'entertainment', 'income'
    ]
    return descriptions, categories


def train_and_save():
    descriptions, categories = make_sample_data()
    clf = TransactionClassifier(model_dir='ai_modules/models')
    clf.train(descriptions, categories)
    print('Training complete, models saved to ai_modules/models')


if __name__ == '__main__':
    train_and_save()
