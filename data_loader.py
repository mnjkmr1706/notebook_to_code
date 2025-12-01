import pandas as pd

def load_data():
    """
    Load the dataset.
    For this example, we create a sample DataFrame.
    In a real scenario, this could load from a CSV file.
    """
    data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'target': [0, 0, 1, 1, 0]
    })
    return data

def preprocess(data):
    """
    Preprocess the data by selecting features and target.
    """
    X = data[['feature1', 'feature2']]
    y = data['target']
    return X, y