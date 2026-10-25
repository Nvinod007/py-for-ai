# The standard PyTorch recipe. Almost every deep learning script follows it.

import torch
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(0)

# %% 1. Data into tensors, then into batches
X, y = make_moons(n_samples=1000, noise=0.2, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=0)
train_ds = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.float32).unsqueeze(1))
val_ds = TensorDataset(torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.float32).unsqueeze(1))
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
val_loader = DataLoader(val_ds, batch_size=256)
print(len(train_loader), "batches per epoch")


# %% 2. The model: a class with layers and a forward method
class Net(nn.Module):
    def __init__(self, hidden=32):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(2, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1),                          # raw score (logit)
        )

    def forward(self, x):
        return self.layers(x)


model = Net()
print(model)
print("parameters:", sum(p.numel() for p in model.parameters()))

# %% 3. Loss and optimizer
loss_fn = nn.BCEWithLogitsLoss()                           # binary classification, applies sigmoid inside
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)


# %% 4. Training and validation functions
def run_epoch(loader, train):
    model.train(train)                                     # train() / eval() switch dropout and batchnorm
    total_loss, correct, count = 0.0, 0, 0
    for xb, yb in loader:
        with torch.set_grad_enabled(train):
            logits = model(xb)
            loss = loss_fn(logits, yb)
        if train:
            optimizer.zero_grad()                          # 1. clear old gradients
            loss.backward()                                # 2. compute new gradients
            optimizer.step()                               # 3. update weights
        total_loss += loss.item() * len(xb)
        correct += ((logits > 0).float() == yb).sum().item()
        count += len(xb)
    return total_loss / count, correct / count


# %% 5. The loop
best_val = 0
for epoch in range(1, 31):
    train_loss, train_acc = run_epoch(train_loader, train=True)
    val_loss, val_acc = run_epoch(val_loader, train=False)
    if val_acc > best_val:
        best_val, best_state = val_acc, {k: v.clone() for k, v in model.state_dict().items()}
    if epoch % 5 == 0 or epoch == 1:
        print(f"epoch {epoch:2d} train_loss={train_loss:.3f} val_loss={val_loss:.3f} train_acc={train_acc:.3f} val_acc={val_acc:.3f}")

# %% 6. Save and reload the best weights
model.load_state_dict(best_state)
torch.save(model.state_dict(), "/tmp/moons_model.pt")
reloaded = Net()
reloaded.load_state_dict(torch.load("/tmp/moons_model.pt"))
reloaded.eval()

# %% 7. Predict
with torch.no_grad():
    probabilities = torch.sigmoid(reloaded(torch.tensor([[0.0, 0.5], [1.0, -0.5]])))
print(probabilities.squeeze().tolist())

# %% Checklist for every project
# zero_grad -> forward -> loss -> backward -> step
# model.train() while training, model.eval() + torch.no_grad() when predicting
# watch validation loss, not just training loss
# classification: CrossEntropyLoss (multi-class), BCEWithLogitsLoss (binary)
# regression: MSELoss or L1Loss
