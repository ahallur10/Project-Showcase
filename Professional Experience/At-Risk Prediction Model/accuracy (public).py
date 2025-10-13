"""
Model evaluation utilities (illustrative).

What it shows:
- Compute accuracy, confusion matrix, and classification report per run/fold
- Aggregate (record_id, y_pred, y_true) rows
- Optional hashing of identifiers for privacy
- Optional CSV/Excel export

NOTE: This script is for demonstration only and won’t run without private datasets.
"""

from __future__ import annotations
import hashlib
from typing import Iterable, Sequence, Tuple, Optional, Union
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

ArrayLike = Union[Sequence[int], Sequence[float], np.ndarray, pd.Series]

def _hash_id(x) -> str:
    return hashlib.sha256(str(x).encode()).hexdigest()[:10]

def evaluate_runs(
    runs: Iterable[Tuple[ArrayLike, ArrayLike, ArrayLike]],
    *,
    labels_order: Sequence[int] = (0, 1),
    hash_ids: bool = True,
    save_path: Optional[str] = None,
    verbose: bool = True,
) -> pd.DataFrame:
    all_rows = []
    for idx, (y_pred, y_true, rec_ids) in enumerate(runs, 1):
        y_pred = pd.Series(y_pred).reset_index(drop=True)
        y_true = pd.Series(y_true).reset_index(drop=True)
        rec_ids = pd.Series(rec_ids).reset_index(drop=True)
        if len(y_pred) != len(y_true) or len(y_true) != len(rec_ids):
            raise ValueError(f"Run {idx}: mismatched lengths.")

        acc = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred, labels=labels_order)
        report = classification_report(y_true, y_pred, labels=labels_order, zero_division=0)

        if verbose:
            print(f"\n=== Run {idx} ===")
            print(f"Accuracy: {acc:.4f}")
            print("Confusion Matrix (rows=true, cols=pred):")
            print(pd.DataFrame(cm, index=[f"T={l}" for l in labels_order], columns=[f"P={l}" for l in labels_order]))
            print("Classification Report:\n", report)

        if hash_ids:
            rec_ids = rec_ids.map(_hash_id)

        all_rows.append(pd.DataFrame({"record_id": rec_ids, "y_pred": y_pred.astype(int), "y_true": y_true.astype(int)}))

    results = pd.concat(all_rows, ignore_index=True)

    if save_path:
        if save_path.lower().endswith(".xlsx"):
            with pd.ExcelWriter(save_path, engine="openpyxl") as w:
                results.to_excel(w, index=False, sheet_name="model_output")
        else:
            results.to_csv(save_path, index=False)

    return results

# Example (non-running) usage:
# runs = [ (y_pred_fold1, y_true_fold1, ids_fold1), (y_pred_fold2, y_true_fold2, ids_fold2) ]
# results = evaluate_runs(runs, save_path="model_output.csv")
