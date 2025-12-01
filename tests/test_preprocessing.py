"""
Unit tests for preprocessing and data splitting functions.
"""

import pandas as pd
from src.preprocessing import preprocess_data, load_config


def test_preprocess_data():
    data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'target': [0, 0, 1, 1, 0]
    })
    config = load_config()
    X_train, X_test, y_train, y_test = preprocess_data(data)
    # Since split is random, check shapes
    total = len(data)
    test_size = config['test_size']
    expected_test_len = int(total * test_size)
    assert len(X_test) == expected_test_len
    assert len(X_train) == total - expected_test_len
    assert 'feature1' in X_train.columns
    assert 'feature2' in X_train.columns


if __name__ == '__main__':
    test_preprocess_data()
    print("All tests passed!")