"""
Unit tests for data loading functions.
"""

import pandas as pd
from src.data_loader import load_synthetic_data


def test_load_synthetic_data():
    data = load_synthetic_data()
    assert isinstance(data, pd.DataFrame)
    assert 'feature1' in data.columns
    assert 'feature2' in data.columns
    assert 'target' in data.columns
    assert len(data) == 5
    assert data['target'].tolist() == [0, 0, 1, 1, 0]


if __name__ == '__main__':
    test_load_synthetic_data()
    print("All tests passed!")