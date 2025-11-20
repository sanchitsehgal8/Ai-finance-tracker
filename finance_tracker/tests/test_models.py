import pytest
from models.transaction import Income, Expense
from datetime import datetime


def test_income_expense_models():
    inc = Income(100.0, datetime.now(), 'Salary', 'Monthly salary', 'user1')
    assert inc.validate()
    assert 'Income' in inc.get_summary()
    exp = Expense(50.0, datetime.now(), 'Groceries', 'Buy food', 'user1')
    assert exp.validate()
    assert 'Expense' in exp.get_summary()
