"""
Module for preprocessing data, including feature extraction, data splitting into train/test sets.
"""

import os
import yaml
from sklearn.model_selection import train_test_split
import pandas as pd


def load_config():
    """
    Loads configuration from config.yaml.

    Returns:
        dict: Configuration dictionary.
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def preprocess_data(data: pd.DataFrame):
    """
    Preprocesses the data by extracting features and splitting into train/test sets.

    Args:
        data (pd.DataFrame): Input dataframe with features and target.

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    config = load_config()
    X = data[['feature1', 'feature2']]
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config['test_size'], random_state=config.get('random_state', 42)
    )
    return X_train, X_test, y_train, y_test