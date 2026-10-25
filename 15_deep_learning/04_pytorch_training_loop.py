# The standard PyTorch recipe. Almost every deep learning script follows it.
# Each line has a short comment saying WHAT it is.

# torch (PyTorch): tensors and deep learning.
import torch
# make_moons: fake two-moons data.
from sklearn.datasets import make_moons
# train_test_split: splits data into train and validation (a held-out set to check progress).
from sklearn.model_selection import train_test_split
# nn: building blocks for neural networks (layers, losses).
from torch import nn
# TensorDataset: pairs inputs with answers; DataLoader: hands out data in small batches.
from torch.utils.data import DataLoader, TensorDataset

# manual_seed(0): fixes random numbers so results repeat.
torch.manual_seed(0)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% 1. Data into tensors, then into batches
# make_moons(n_samples, noise, random_state): points in two curved groups.
X, y = make_moons(n_samples=1000, noise=0.2, random_state=0)
# train_test_split(..., test_size=0.2): 20% kept as validation.
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=0)
# torch.tensor(data, dtype=float32): numpy -> tensor with 32-bit decimals; unsqueeze(1): make a column; TensorDataset(inputs, answers) pairs them.
train_ds = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.float32).unsqueeze(1))
# Same for validation data.
val_ds = TensorDataset(torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.float32).unsqueeze(1))
# DataLoader(ds, batch_size=32, shuffle=True): gives 32 examples at a time (a batch), shuffled each epoch (an epoch = one full pass over the data).
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
# Validation: bigger batches, no shuffle.
val_loader = DataLoader(val_ds, batch_size=256)
# len(loader): number of batches.
print(len(train_loader), "batches per epoch")


# %% 2. The model: a class with layers and a forward method
# nn.Module: base class for all PyTorch models.
class Net(nn.Module):
    # __init__: runs when the model is created; super().__init__() sets up nn.Module.
    def __init__(self, hidden=32):
        super().__init__()
        # nn.Sequential(...): runs layers in order.
        self.layers = nn.Sequential(
            # nn.Linear(in, out): a layer that multiplies by weights and adds a bias; ReLU zeroes negatives (adds the 'bend').
            nn.Linear(2, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1),                          # raw score (logit)
        )

    # forward(x): how data flows through the model; called by model(x).
    def forward(self, x):
        return self.layers(x)


# Create the model with random weights.
model = Net()
# Shows the layers.
print(model)
# parameters(): all learnable numbers; numel() counts the items in each.
print("parameters:", sum(p.numel() for p in model.parameters()))

# %% 3. Loss and optimizer
# BCEWithLogitsLoss: loss = how wrong; for yes/no answers, applies sigmoid inside.
loss_fn = nn.BCEWithLogitsLoss()                           # binary classification, applies sigmoid inside
# Adam: the optimizer updates weights using gradients; lr = learning rate (step size).
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)


# %% 4. Training and validation functions
# One pass over a loader; train=True also learns.
def run_epoch(loader, train):
    # train(True/False): switches layers like dropout between training and evaluation behaviour.
    model.train(train)                                     # train() / eval() switch dropout and batchnorm
    # Counters for loss and correct answers.
    total_loss, correct, count = 0.0, 0, 0
    # Each batch: xb = inputs, yb = answers.
    for xb, yb in loader:
        # set_grad_enabled(flag): track gradients only when training.
        with torch.set_grad_enabled(train):
            # logits = raw scores before turning into probabilities.
            logits = model(xb)
            # Compare the model's scores with the true answers.
            loss = loss_fn(logits, yb)
        if train:
            # zero_grad(): clears old gradients.
            optimizer.zero_grad()                          # 1. clear old gradients
            # backward(): computes new gradients.
            loss.backward()                                # 2. compute new gradients
            # step(): updates weights using the gradients.
            optimizer.step()                               # 3. update weights
        # item(): tensor -> plain number.
        total_loss += loss.item() * len(xb)
        # A score above 0 means class 1; compare with answers, sum() counts matches.
        correct += ((logits > 0).float() == yb).sum().item()
        # Count examples seen.
        count += len(xb)
    # Average loss and accuracy.
    return total_loss / count, correct / count


# %% 5. The loop
# Track the best validation accuracy so far.
best_val = 0
# Repeat for 30 epochs.
for epoch in range(1, 31):
    # Learn on the training data.
    train_loss, train_acc = run_epoch(train_loader, train=True)
    # Only measure on validation data.
    val_loss, val_acc = run_epoch(val_loader, train=False)
    if val_acc > best_val:
        # state_dict(): the model's weights as a dict; clone() copies them so we can restore the best.
        best_val, best_state = val_acc, {k: v.clone() for k, v in model.state_dict().items()}
    # Print on epoch 1 and every 5th.
    if epoch % 5 == 0 or epoch == 1:
        print(f"epoch {epoch:2d} train_loss={train_loss:.3f} val_loss={val_loss:.3f} train_acc={train_acc:.3f} val_acc={val_acc:.3f}")

# %% 6. Save and reload the best weights
# load_state_dict(dict): put saved weights into the model.
model.load_state_dict(best_state)
# torch.save(obj, file): save weights to a file.
torch.save(model.state_dict(), "/tmp/moons_model.pt")
# A fresh model to load the file into.
reloaded = Net()
# torch.load(file): read the saved weights.
reloaded.load_state_dict(torch.load("/tmp/moons_model.pt"))
# eval(): switch to prediction mode.
reloaded.eval()

# %% 7. Predict
# no_grad(): no gradient tracking (faster for prediction).
with torch.no_grad():
    # torch.sigmoid: turns scores into 0..1 probabilities.
    probabilities = torch.sigmoid(reloaded(torch.tensor([[0.0, 0.5], [1.0, -0.5]])))
# squeeze(): drop size-1 dimensions; tolist(): tensor -> Python list.
print(probabilities.squeeze().tolist())


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Checklist for every project
# zero_grad -> forward -> loss -> backward -> step
# model.train() while training, model.eval() + torch.no_grad() when predicting
# watch validation loss, not just training loss
# classification: CrossEntropyLoss (multi-class), BCEWithLogitsLoss (binary)
# regression: MSELoss or L1Loss
