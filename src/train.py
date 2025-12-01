from src.data import load_data
from src.model import create_model


def train_model():
    """
    Trains the Logistic Regression model.
    """
    X_train, y_train, X_test, y_test = load_data()
    model = create_model()
    model.fit(X_train, X_test)
    return model, y_train, y_test

if __name__ == "__main__":
    model, y_train, y_test = train_model()
    print("Model training complete.")
