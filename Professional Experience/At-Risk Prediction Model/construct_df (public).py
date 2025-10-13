"""
Data preprocessing (illustrative).

What it shows:
- Load tabular data (CSV/Excel)
- Basic cleaning (row completeness, ID drop, simple text normalization)
- Split into X (features) / y (target)
- Lightweight one-hot encoding via pandas (no on-disk artifacts)

NOTE: This script is for demonstration only and won’t run without private datasets.
"""

from __future__ import annotations
import os
import pandas as pd
from typing import Optional, List, Tuple

class TabularPreprocessor:
    def __init__(
        self,
        file_path: str,
        id_column: str = "record_id",
        label_column: str = "target",
        drop_columns: Optional[List[str]] = None,
        text_columns_to_normalize: Optional[List[str]] = None,
        max_missing_per_row: int = 3,
    ):
        self.file_path = file_path
        self.id_column = id_column
        self.label_column = label_column
        self.drop_columns = drop_columns or []
        self.text_cols = text_columns_to_normalize or []
        self.max_missing_per_row = max_missing_per_row
        self.df: Optional[pd.DataFrame] = None

    def load(self) -> None:
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext in (".xlsx", ".xls"):
            self.df = pd.read_excel(self.file_path, engine="openpyxl")
        else:
            self.df = pd.read_csv(self.file_path)

    def _normalize(self, s: pd.Series) -> pd.Series:
        return s.astype(str).str.replace(r"\s+", "", regex=True).replace({"nan": pd.NA})

    def clean(self) -> None:
        assert self.df is not None, "Call load() first."
        # Drop rows with too many missing fields
        keep_thresh = len(self.df.columns) - self.max_missing_per_row
        self.df = self.df.dropna(thresh=keep_thresh)

        # Drop identifier and any domain-specific columns
        cols_to_drop = [c for c in [self.id_column, *self.drop_columns] if c in self.df.columns]
        self.df = self.df.drop(columns=cols_to_drop, errors="ignore")

        # Normalize selected text columns (if present)
        for c in self.text_cols:
            if c in self.df.columns:
                self.df[c] = self._normalize(self.df[c])

        # Simple imputation
        self.df = self.df.fillna(0)

    def split_xy(self) -> Tuple[pd.DataFrame, pd.Series]:
        assert self.df is not None, "Call load() and clean() first."
        if self.label_column not in self.df.columns:
            raise ValueError(f"Missing target column '{self.label_column}'.")
        X = self.df.drop(columns=[self.label_column])
        y = self.df[self.label_column]
        # One-hot encode categoricals without saving any mapping files
        X = pd.get_dummies(X, drop_first=False)
        return X, y

# Example (non-running) usage:
# pre = TabularPreprocessor("dataset.xlsx", id_column="record_id", label_column="target")
# pre.load(); pre.clean(); X, y = pre.split_xy()
