"""
Tree-based model training (illustrative).

What it shows:
- Fit a simple tree-based classifier (Decision Tree or Random Forest)
- Return predictions alongside the true labels for downstream evaluation
- Optional: serialize the trained model

NOTE: This script is for demonstration only and won’t run without private datasets.
"""

from __future__ import annotations
from typing import Literal, Optional, Tuple
import joblib
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

ClassifierName = Literal["decision_tree", "random_forest"]

class TreeLabelGenerator:
    def __init__(
        self,
        X_train: pd.DataFrame | np.ndarray,
        y_train: pd.Series | np.ndarray,
        X_test:  pd.DataFrame | np.ndarray,
        y_test:  pd.Series | np.ndarray,
        *,
        model: ClassifierName = "decision_tree",
        random_state: Optional[int] = 42,
        max_depth: Optional[int] = None,
        n_estimators: int = 200,
    ):
        self.X_train, self.y_train = X_train, y_train
        self.X_test,  self.y_test  = X_test,  y_test
        self.model_name = model
        self.random_state = random_state
        self.max_depth = max_depth
        self.n_estimators = n_estimators
        self.clf = None

    def _build_model(self):
        if self.model_name == "random_forest":
            return RandomForestClassifier(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                random_state=self.random_state,
                n_jobs=-1,
            )
        return DecisionTreeClassifier(
            max_depth=self.max_depth,
            random_state=self.random_state,
        )

    def train(self) -> None:
        self.clf = self._build_model()
        self.clf.fit(self.X_train, self.y_train)

    def predict_vs_true(self) -> Tuple[np.ndarray, np.ndarray]:
        if self.clf is None:
            raise RuntimeError("Model not trained. Call train() first.")
        y_pred = self.clf.predict(self.X_test)
        return y_pred, np.asarray(self.y_test)

    def run(self) -> Tuple[np.ndarray, np.ndarray]:
        """Convenience: train then return (y_pred, y_true)."""
        self.train()
        return self.predict_vs_true()

    def save(self, path: str) -> None:
        """Optional: persist the model artifact for reproducibility."""
        if self.clf is None:
            raise RuntimeError("Model not trained. Call train() first.")
        joblib.dump(self.clf, path)
        print(f"Model saved to {path}")

# Example (non-running) usage:
# gen = TreeLabelGenerator(X_train, y_train, X_test, y_test, model="random_forest", max_depth=8)
# y_pred, y_true = gen.run()
# gen.save("model.joblib")
