from sklearn.metrics import accuracy_score


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model by predicting and calculating accuracy.

    Args:
        model: Trained model with predict method.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): Test target.

    Returns:
        float: Accuracy score.
    """
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    return accuracy