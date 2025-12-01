
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data():
    """
    Loads and preprocesses the data.

    Returns:
        tuple: A tuple containing the training and testing data (X_train, X_test, y_train, y_test).
    """
    # Load data
    data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'target': [0, 0, 1, 1, 0]
    })

    # Preprocess
    X = data[['feature1', 'feature2']]
y = data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # Added random_state for reproducibility
    return X_train, X_test, y_train, y_test
