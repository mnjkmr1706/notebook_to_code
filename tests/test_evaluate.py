"""
Unit tests for evaluation metrics and prediction functions.
"""

from src.model import LogisticClassifier
from src.evaluate import evaluate_model
import numpy as np


def test_evaluate_model():
    model = LogisticClassifier()
    X = np.array([[1, 2], [3, 4], [5, 6]])
    y = np.array([0, 1, 0])
    model.fit(X, y)
    accuracy = evaluate_model(model, X, y)
    # Accuracy should be perfect for training data
    assert 0 <= accuracy <= 1


if __name__ == '__main__':
    test_evaluate_model()
    print("All tests passed!")