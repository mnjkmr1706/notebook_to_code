#!/usr/bin/env python3
"""
Main script to execute the full ML pipeline: load data, preprocess, train, and evaluate.
"""

import sys
import os
# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.train import train
from src.evaluate import evaluate


if __name__ == "__main__":
    model, X_test, y_test = train()
    evaluate(model, X_test, y_test)