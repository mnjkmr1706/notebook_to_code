import pandas as pd
from sklearn.metrics import accuracy_score

from src.data import load_data, preprocess_data
from src.model import LogisticRegressionModel


def main():
    """Main function to load, preprocess, train, and evaluate the model."""
    # Load data
    try:
        data = load_data()
    except FileNotFoundError:
        print("Error: sample_data.csv not found in the data directory.  Creating sample data...")
        data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'target': [0, 0, 1, 1, 0]
        })
        data.to_csv("data/sample_data.csv", index=False)

    # Preprocess data
    X_train, X_test, y_train, y_test = preprocess_data(data)

    # Train model
    model = LogisticRegressionModel()
    model.train(X_train, y_train)

    # Evaluate model
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    print(f"Accuracy: {accuracy}")


if __name__ == "__main__":
    main()
