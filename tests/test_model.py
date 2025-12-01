import unittest
from src.model import LogisticRegressionModel
import pandas as pd

class TestLogisticRegressionModel(unittest.TestCase):

    def test_model_training(self):
        # Create a dummy dataset for testing
        data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'target': [0, 0, 1, 1, 0]
        })
        X = data[['feature1', 'feature2']]
        y = data['target']

        # Initialize and train the model
        model = LogisticRegressionModel()
        model.fit(X, y)

        # Assert that the model is trained (basic check)
        self.assertTrue(hasattr(model.model, 'coef_'))

    def test_model_prediction(self):
         # Create a dummy dataset for testing
        data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'target': [0, 0, 1, 1, 0]
        })
        X = data[['feature1', 'feature2']]
        y = data['target']

        # Initialize and train the model
        model = LogisticRegressionModel()
        model.fit(X, y)

        #Make predictions
        predictions = model.predict(X)

        # Assert that predictions are not empty
        self.assertIsNotNone(predictions)


if __name__ == '__main__':
    unittest.main()
