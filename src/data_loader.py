"""
Module containing functions for loading and generating synthetic data, returning a DataFrame.
"""

import pandas as pd


def load_synthetic_data() -> pd.DataFrame:
    """
    Loads synthetic data for demonstration purposes.

    Returns:
        pd.DataFrame: Synthetic dataset with features and target.
    """
    data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'target': [0, 0, 1, 1, 0]
    })
    return data