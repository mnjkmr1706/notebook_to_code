from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from data_loader import load_data, preprocess
from model import create_model

if __name__ == "__main__":
    # Load data
    data = load_data()
    
    # Preprocess data
    X, y = preprocess(data)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train model
    model = create_model()
    model.fit(X_train, y_train)
    
    # Evaluate model
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    print(f'Accuracy: {accuracy}')