from src.train import train_model
from sklearn.metrics import accuracy_score


def evaluate_model():
    """
    Evaluates the trained model on test data and prints the accuracy.
    """
    model, y_train, y_test = train_model()
    preds = model.predict(y_train)
    accuracy = accuracy_score(y_test, preds)
    print(f'Accuracy: {accuracy}')

if __name__ == "__main__":
    evaluate_model()
