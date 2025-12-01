"""
Unit tests for training functionality.
"""

from src.model import LogisticClassifier
from src.train import train_model
import numpy as np


def test_train_model():
    model = LogisticClassifier()
    X_train = np.array([[1, 2], [3, 4], [5, 6]])
    y_train = np.array([0, 1, 0])
    train_model(model, X_train, y_train)
    # Since fit happens, model should be fitted
    assert hasattr(model.model, 'coef_')


if __name__ == '__main__':
    test_train_model()
    print("All tests passed!")