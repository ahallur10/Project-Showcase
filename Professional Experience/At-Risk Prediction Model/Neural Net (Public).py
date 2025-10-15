import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

# Use proper torch.device for device management
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Class for the NN architecture
class NeuralNetwork(nn.Module):
    def __init__(self, input_size: int = 12):
        super(NeuralNetwork, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.BatchNorm1d(64),
            nn.LeakyReLU(),
            nn.Dropout(0.3),

            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.LeakyReLU(),
            nn.Dropout(0.3),

            nn.Linear(32, 1)  # Raw logits for BCEWithLogitsLoss
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

# Class to house our tensor datasets that pandas must convert to
class CustomDataset(Dataset):
    def __init__(self, df_features, df_labels):

        self.X = torch.tensor(df_features.values, dtype=torch.float32)
        # For binary classification, BCEWithLogitsLoss expects float targets.
        self.y = torch.tensor(df_labels.values, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx: int):
        return self.X[idx], self.y[idx]

# Class to house all methods and attributes to train the model. Contains many hyperparameters
class NeuralNetworkTrainer:
    def __init__(
        self,
        train_x,
        train_y,
        test_x,
        test_y,
        batch_size: int = 64,
        epochs: int = 50,
        lr: float = 0.001,
        early_stopping_patience: int = 5,
        early_stopping_min_delta: float = 0.001,
    ):

        self.train_x = train_x
        self.train_y = train_y
        self.test_x = test_x
        self.test_y = test_y
        self.batch_size = batch_size
        self.epochs = epochs
        self.lr = lr
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_min_delta = early_stopping_min_delta
        self.device = device
        self.model = None
        self.train_loader = None
        self.test_loader = None

        # Initialize loss curves
        self.train_loss_curve = []
        self.test_loss_curve = []

    def run(self):

        self.prepare_data()
        self.build_model()
        self.train()
        preds, actuals = self.generate_labels()
        return preds, actuals

    def prepare_data(self):

        self.train_loader = DataLoader(
            CustomDataset(self.train_x, self.train_y),
            batch_size=self.batch_size,
            shuffle=True,
        )
        self.test_loader = DataLoader(
            CustomDataset(self.test_x, self.test_y),
            batch_size=self.batch_size,
            shuffle=False,
        )

    def build_model(self):

        input_size = self.train_x.shape[1]  # Dynamically determine input features
        self.model = NeuralNetwork(input_size=input_size).to(self.device)
        print("Model architecture:\n", self.model)

    # Trains the model with early stopping
    def train(self):
        self.loss_fn = nn.BCEWithLogitsLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        best_loss = float("inf")
        epochs_without_improvement = 0
        best_model_state = None

        for epoch in range(1, self.epochs + 1):
            print(f"\nEpoch {epoch}/{self.epochs}")

            train_loss = self._train_epoch()  # Get average training loss for the epoch
            val_loss = self._validate()  # Get average validation loss for the epoch

            # Store the losses for later plotting
            self.train_loss_curve.append(train_loss)
            self.test_loss_curve.append(val_loss)

            # Check for improvement in validation loss
            if best_loss - val_loss > self.early_stopping_min_delta:
                best_loss = val_loss
                epochs_without_improvement = 0
                best_model_state = self.model.state_dict()
                print(f"Validation loss improved to {val_loss:.6f}.")
            else:
                epochs_without_improvement += 1
                print(f"No significant improvement for {epochs_without_improvement} epoch(s).")

            if epochs_without_improvement >= self.early_stopping_patience:
                print("Early stopping triggered.")
                break

        if best_model_state is not None:
            self.model.load_state_dict(best_model_state)
            print("Loaded best model state from training.")

    def _train_epoch(self):
        self.model.train()
        total_loss = 0
        for batch_idx, (X, y) in enumerate(self.train_loader):
            X, y = X.to(self.device), y.to(self.device).unsqueeze(1)  # Ensure shape [batch, 1]
            self.optimizer.zero_grad()  # Clear gradients at start of batch
            logits = self.model(X)
            loss = self.loss_fn(logits, y)
            loss.backward()
            self.optimizer.step()
            total_loss += loss.item()

            if batch_idx % 100 == 0:
                print(f"Batch {batch_idx:>3}: Loss = {loss.item():.6f}")

        avg_train_loss = total_loss / len(self.train_loader)
        print(f"Average Training Loss: {avg_train_loss:.6f}")
        return avg_train_loss

    # Test the model
    def _validate(self):
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total_samples = 0

        with torch.no_grad():
            for X, y in self.test_loader:
                X, y = X.to(self.device), y.to(self.device).unsqueeze(1)
                logits = self.model(X)
                loss = self.loss_fn(logits, y)
                total_loss += loss.item()

                probs = torch.sigmoid(logits)
                preds = (probs > 0.5).float()
                correct += (preds == y).sum().item()
                total_samples += y.size(0)

        avg_loss = total_loss / len(self.test_loader)
        accuracy = correct / total_samples
        print(f"Validation Results: Accuracy = {accuracy * 100:.1f}%, Avg Loss = {avg_loss:.6f}")
        return avg_loss

    # Run the testing set through the model to get the generated label
    def generate_labels(self):
        self.model.eval()
        all_preds = []
        all_actual = []

        with torch.no_grad():
            for X, y in self.test_loader:
                X, y = X.to(self.device), y.to(self.device)
                logits = self.model(X)
                probs = torch.sigmoid(logits)
                preds = (probs > 0.5).float().view(-1)
                all_preds.append(preds.cpu())
                all_actual.append(y.cpu().view(-1))

        generated_labels = torch.cat(all_preds).numpy()
        actual_labels = torch.cat(all_actual).numpy()
        return generated_labels, actual_labels

    def save_model(self, file_path: str):
        torch.save(self.model.state_dict(), file_path)
        print(f"Model saved to {file_path}")

