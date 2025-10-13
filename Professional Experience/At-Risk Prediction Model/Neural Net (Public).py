"""
Binary classifier with PyTorch (illustrative).

What it shows:
- Minimal MLP with BatchNorm/Dropout for tabular data
- DataLoader wrappers for (X, y) tensors from pandas
- Training loop with early stopping on validation loss
- Prediction helper returning numpy arrays
- Optional model save/load hooks

PRIVACY: No domain terms or identifiers. For demonstration only; not runnable without private datasets.
"""

from __future__ import annotations
from typing import Optional, Tuple
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# Prefer GPU when available; fall back to CPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# --- Model definition ---
class MLP(nn.Module):
    def __init__(self, in_features: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 64),
            nn.BatchNorm1d(64),
            nn.LeakyReLU(),
            nn.Dropout(0.30),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.LeakyReLU(),
            nn.Dropout(0.30),
            nn.Linear(32, 1),  # logits for BCEWithLogitsLoss
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


# --- Dataset wrapper (expects pandas DataFrame/Series) ---
class TabularDataset(Dataset):
    def __init__(self, X_df, y_sr):
        # BCEWithLogitsLoss expects float targets (0./1.)
        self.X = torch.tensor(X_df.values, dtype=torch.float32)
        self.y = torch.tensor(y_sr.values, dtype=torch.float32).view(-1, 1)

    def __len__(self) -> int:
        return self.X.size(0)

    def __getitem__(self, idx: int):
        return self.X[idx], self.y[idx]


# --- Trainer with early stopping ---
class NNTrainer:
    def __init__(
        self,
        X_train, y_train,
        X_val, y_val,
        *,
        batch_size: int = 64,
        epochs: int = 50,
        lr: float = 1e-3,
        patience: int = 5,
        min_delta: float = 1e-3,
        device: Optional[torch.device] = None,
    ):
        self.device = device or DEVICE
        self.batch_size, self.epochs = batch_size, epochs
        self.lr, self.patience, self.min_delta = lr, patience, min_delta

        self.train_loader = DataLoader(TabularDataset(X_train, y_train), batch_size=batch_size, shuffle=True)
        self.val_loader   = DataLoader(TabularDataset(X_val,   y_val),   batch_size=batch_size, shuffle=False)

        in_features = X_train.shape[1]
        self.model = MLP(in_features=in_features).to(self.device)
        self.opt = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.BCEWithLogitsLoss()

        self.train_curve, self.val_curve = [], []

    def _epoch(self, loader: DataLoader, train: bool) -> float:
        self.model.train(mode=train)
        total = 0.0
        for X, y in loader:
            X, y = X.to(self.device), y.to(self.device)
            logits = self.model(X)
            loss = self.criterion(logits, y)
            if train:
                self.opt.zero_grad()
                loss.backward()
                self.opt.step()
            total += float(loss.item())
        return total / max(1, len(loader))

    def fit(self) -> None:
        best_val = float("inf")
        best_state = None
        no_improve = 0

        for _ in range(self.epochs):
            tr = self._epoch(self.train_loader, train=True)
            vl = self._epoch(self.val_loader,   train=False)
            self.train_curve.append(tr)
            self.val_curve.append(vl)

            if best_val - vl > self.min_delta:
                best_val, best_state, no_improve = vl, self.model.state_dict(), 0
            else:
                no_improve += 1
                if no_improve >= self.patience:
                    break

        if best_state is not None:
            self.model.load_state_dict(best_state)

    @torch.no_grad()
    def predict_vs_true(self) -> Tuple[np.ndarray, np.ndarray]:
        self.model.eval()
        preds, trues = [], []
        for X, y in self.val_loader:
            X = X.to(self.device)
            logits = self.model(X)
            probs = torch.sigmoid(logits)
            pred = (probs > 0.5).float()
            preds.append(pred.cpu().view(-1))
            trues.append(y.cpu().view(-1))
        return torch.cat(preds).numpy(), torch.cat(trues).numpy()

    def run(self) -> Tuple[np.ndarray, np.ndarray]:
        """Train then return (y_pred, y_true) on the validation set."""
        self.fit()
        return self.predict_vs_true()

    def save(self, path: str) -> None:
        torch.save(self.model.state_dict(), path)

# Example (illustrative only; requires private data)
# trainer = NNTrainer(X_train, y_train, X_val, y_val, epochs=30, patience=4)
# y_pred, y_true = trainer.run()
# trainer.save("mlp_state.pt")
