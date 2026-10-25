# Making training work: overfitting controls, optimizers, learning rates, early stopping.
# Each line has a short comment saying WHAT it is.

# torch (PyTorch): tensors and deep learning.
import torch
# make_moons: fake two-moons data.
from sklearn.datasets import make_moons
# train_test_split: splits data into train and validation.
from sklearn.model_selection import train_test_split
# nn: neural-network building blocks.
from torch import nn

# A small noisy dataset makes overfitting easy to see
# make_moons(n_samples, noise, random_state): points in two curved groups; more noise = harder.
X, y = make_moons(n_samples=240, noise=0.35, random_state=1)
# train_test_split(..., test_size=0.5): half kept as validation (data used only to check).
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.5, random_state=1)
# torch.tensor(data, dtype=float32): numpy -> tensor; unsqueeze(1) makes a column.
Xt, yt = torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
# Same for validation data.
Xv, yv = torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.float32).unsqueeze(1)


# Makes a small network. nn.Sequential runs layers in order.
def build(hidden=128, dropout=0.0):
    return nn.Sequential(
        # nn.Linear(in, out): weights + bias layer; ReLU: zeroes negatives; Dropout(p): randomly switches off a share p of neurons while training so the model can't memorize.
        nn.Linear(2, hidden), nn.ReLU(), nn.Dropout(dropout),
        nn.Linear(hidden, hidden), nn.ReLU(), nn.Dropout(dropout),
        nn.Linear(hidden, 1),
    )


# Trains the model and returns (train accuracy, validation accuracy). patience = epochs to wait for improvement before stopping; weight_decay = penalty on big weights.
def fit(model, epochs=300, lr=0.01, weight_decay=0.0, optimizer_name="adam", patience=None, verbose=False):
    # An optimizer updates weights from gradients. SGD: plain steps; momentum=0.9: keeps rolling in the same direction; Adam: adapts step per weight; AdamW: Adam with cleaner weight decay.
    optimizers = {
        "sgd": torch.optim.SGD(model.parameters(), lr=lr, weight_decay=weight_decay),
        "momentum": torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=weight_decay),
        "adam": torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay),
        "adamw": torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=max(weight_decay, 0.01)),
    }
    # loss = how wrong; BCEWithLogitsLoss: loss for yes/no answers.
    optimizer, loss_fn = optimizers[optimizer_name], nn.BCEWithLogitsLoss()
    # Track the best validation loss and how many epochs without improvement.
    best, bad_epochs, best_state = float("inf"), 0, None
    # epoch = one pass over the data (here the whole set at once).
    for epoch in range(epochs):
        # train(): training mode (dropout on).
        model.train()
        # zero_grad(): clear old gradients.
        optimizer.zero_grad()
        # model(X): predictions; backward(): compute gradients.
        loss_fn(model(Xt), yt).backward()
        # step(): update the weights.
        optimizer.step()
        # eval(): prediction mode (dropout off).
        model.eval()
        # no_grad(): no gradient tracking.
        with torch.no_grad():
            # item(): one-number tensor -> Python number.
            val_loss = loss_fn(model(Xv), yv).item()
        # Save a copy of the weights whenever validation improves; state_dict() = weights as a dict, clone() = copy.
        if val_loss < best:
            best, bad_epochs = val_loss, 0
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            bad_epochs += 1
            if patience and bad_epochs >= patience:
                if verbose:
                    print(f"early stop at epoch {epoch}")
                # load_state_dict: restore the best weights.
                model.load_state_dict(best_state)
                break
    model.eval()
    with torch.no_grad():
        # (score > 0) = predicted class 1; compare with answers; mean() = share correct.
        train_acc = ((model(Xt) > 0).float() == yt).float().mean().item()
        val_acc = ((model(Xv) > 0).float() == yv).float().mean().item()
    # round(x, 3): 3 decimals.
    return round(train_acc, 3), round(val_acc, 3)


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% 1. Overfitting: a big network on little data
# manual_seed: fix randomness so runs match.
torch.manual_seed(0)
# Baseline: big network, no protection.
print("no protection        (train, val):", fit(build()))

# %% 2. Dropout: randomly switch off neurons while training
torch.manual_seed(0)
# dropout=0.3: switch off 30% of neurons while training.
print("dropout 0.3          (train, val):", fit(build(dropout=0.3)))

# %% 3. Weight decay: penalize large weights
torch.manual_seed(0)
# weight_decay: shrink big weights; 'adamw' optimizer.
print("weight decay 0.01    (train, val):", fit(build(), weight_decay=0.01, optimizer_name="adamw"))

# %% 4. Early stopping: stop when validation stops improving
torch.manual_seed(0)
# epochs=1000 with patience=20: stop once 20 epochs pass without improvement.
print("early stopping       (train, val):", fit(build(), epochs=1000, patience=20, verbose=True))

# %% 5. Smaller model
torch.manual_seed(0)
# hidden=8: fewer neurons, less room to memorize.
print("smaller network (8)  (train, val):", fit(build(hidden=8)))

# %% Optimizers compared (same model, same data)
# Same model/data, different optimizers.
for name in ["sgd", "momentum", "adam", "adamw"]:
    torch.manual_seed(0)
    # {name:9} pads the name for neat columns.
    print(f"{name:9}", fit(build(hidden=32), epochs=200, lr=0.01, optimizer_name=name))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Learning rate schedules lower the learning rate over time
# A fresh model for the schedule demo.
model = build(hidden=32)
# Adam optimizer; lr=0.1 = starting learning rate (step size).
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)
# StepLR: multiplies the learning rate by gamma=0.5 every step_size=10 epochs.
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)
# List to record learning rates.
rates = []
for epoch in range(30):
    # param_groups[0]['lr']: the optimizer's current learning rate.
    rates.append(optimizer.param_groups[0]["lr"])
    # step(): update the weights (no loss here; just a demo).
    optimizer.step()
    # scheduler.step(): moves the schedule forward one epoch.
    scheduler.step()
# rates[::10] = every 10th value.
print([round(r, 4) for r in rates[::10]])

# %% Other tools you will meet
# Batch normalization / layer normalization: keep activations well scaled (nn.BatchNorm1d, nn.LayerNorm)
# Gradient clipping: torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
# Data augmentation: more varied training data for images and text
# Mixed precision, gradient accumulation: fit bigger models in memory
