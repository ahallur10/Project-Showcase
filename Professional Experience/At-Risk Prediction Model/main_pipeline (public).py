"""
End-to-end ML workflow (illustrative).

What it shows:
- Build features/labels from a tabular file
- K-fold evaluation of either a tree-based model or a small neural net
- Aggregate predictions for reporting

NOTE: This script is for demonstration only and won’t run without private datasets.
All names are generic and de-identified for public sharing.
"""

from __future__ import annotations
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

# Local modules (illustrative versions from this repo)
#   data_preprocessing.py : TabularPreprocessor
#   model_training.py     : TreeLabelGenerator
#   nn_trainer.py         : NNTrainer
#   model_evaluation.py   : evaluate_runs
#   model_selector.py     : choose_model (optional)
from data_preprocessing import TabularPreprocessor
from model_training import TreeLabelGenerator
from nn_trainer import NNTrainer
from model_evaluation import evaluate_runs
# from model_selector import choose_model  # optional GUI

def select_model(default: str = "decision_tree") -> str:
    """
    Simple selector to avoid launching a GUI in public repos.
    Set MODEL_CHOICE env var to 'decision_tree' or 'neural_network'.
    """
    choice = os.getenv("MODEL_CHOICE", default).strip().lower()
    if choice not in {"decision_tree", "neural_network"}:
        choice = default
    return choice

def main():
    # Display settings (safe for large tables when demonstrating)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 160)

    # --- 1) Build features/labels (illustrative) ---
    # Replace "dataset.xlsx" with your own de-identified filename locally; not included in this repo.
    pre = TabularPreprocessor(
        file_path="dataset.xlsx",        # placeholder; not shipped publicly
        id_column="record_id",
        label_column="target",
        drop_columns=[],                 # put domain-specific columns here if needed
        text_columns_to_normalize=["bmi_category"],  # generic example
    )
    pre.load()
    pre.clean()
    X, y = pre.split_xy()

    # --- 2) Choose model (no GUI by default for public repos) ---
    # model_name = choose_model(options=["Decision Tree", "Neural Network"]).lower().replace(" ", "_")
    model_name = select_model(default="decision_tree")  # or set MODEL_CHOICE env var

    # --- 3) K-fold evaluation (illustrative) ---
    k = 5
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)

    runs = []  # will hold (y_pred, y_true, record_ids) per fold
    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X, y), start=1):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        # Optionally: apply resampling here if class imbalance exists (left out for clarity)
        # from imblearn.over_sampling import SMOTE
        # X_train, y_train = SMOTE(random_state=42).fit_resample(X_train, y_train)

        if model_name == "neural_network":
            trainer = NNTrainer(
                X_train, y_train,
                X_test,  y_test,
                epochs=30, patience=5, min_delta=1e-3, lr=1e-3, batch_size=64
            )
            y_pred, y_true = trainer.run()
            # trainer.save("mlp_state.pt")  # optional artifact (not committed)
        else:
            gen = TreeLabelGenerator(
                X_train, y_train,
                X_test,  y_test,
                model="decision_tree",   # or "random_forest"
                max_depth=None,
                random_state=42,
            )
            y_pred, y_true = gen.run()
            # gen.save("model.joblib")  # optional artifact (not committed)

        # Record IDs are just the test index here; evaluate_runs will hash by default.
        runs.append((y_pred, y_true, np.arange(len(y_true))))

    # --- 4) Aggregate & report (hashed identifiers by default) ---
    _ = evaluate_runs(runs=runs, save_path=None, verbose=True)

if __name__ == "__main__":
    main()
