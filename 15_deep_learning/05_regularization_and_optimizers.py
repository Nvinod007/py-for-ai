# Making training work: overfitting controls, optimizers, learning rates, early stopping.

import torch
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from torch import nn

# A small noisy dataset makes overfitting easy to see
X, y = make_moons(n_samples=240, noise=0.35, random_state=1)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.5, random_state=1)
Xt, yt = torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
Xv, yv = torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.float32).unsqueeze(1)


def build(hidden=128, dropout=0.0):
    return nn.Sequential(
        nn.Linear(2, hidden), nn.ReLU(), nn.Dropout(dropout),
        nn.Linear(hidden, hidden), nn.ReLU(), nn.Dropout(dropout),
        nn.Linear(hidden, 1),
    )


def fit(model, epochs=300, lr=0.01, weight_decay=0.0, optimizer_name="adam", patience=None, verbose=False):
    optimizers = {
        "sgd": torch.optim.SGD(model.parameters(), lr=lr, weight_decay=weight_decay),
        "momentum": torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=weight_decay),
        "adam": torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay),
        "adamw": torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=max(weight_decay, 0.01)),
    }
    optimizer, loss_fn = optimizers[optimizer_name], nn.BCEWithLogitsLoss()
    best, bad_epochs, best_state = float("inf"), 0, None
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        loss_fn(model(Xt), yt).backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            val_loss = loss_fn(model(Xv), yv).item()
        if val_loss < best:
            best, bad_epochs = val_loss, 0
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            bad_epochs += 1
            if patience and bad_epochs >= patience:
                if verbose:
                    print(f"early stop at epoch {epoch}")
                model.load_state_dict(best_state)
                break
    model.eval()
    with torch.no_grad():
        train_acc = ((model(Xt) > 0).float() == yt).float().mean().item()
        val_acc = ((model(Xv) > 0).float() == yv).float().mean().item()
    return round(train_acc, 3), round(val_acc, 3)


# %% 1. Overfitting: a big network on little data
torch.manual_seed(0)
print("no protection        (train, val):", fit(build()))

# %% 2. Dropout: randomly switch off neurons while training
torch.manual_seed(0)
print("dropout 0.3          (train, val):", fit(build(dropout=0.3)))

# %% 3. Weight decay: penalize large weights
torch.manual_seed(0)
print("weight decay 0.01    (train, val):", fit(build(), weight_decay=0.01, optimizer_name="adamw"))

# %% 4. Early stopping: stop when validation stops improving
torch.manual_seed(0)
print("early stopping       (train, val):", fit(build(), epochs=1000, patience=20, verbose=True))

# %% 5. Smaller model
torch.manual_seed(0)
print("smaller network (8)  (train, val):", fit(build(hidden=8)))

# %% Optimizers compared (same model, same data)
for name in ["sgd", "momentum", "adam", "adamw"]:
    torch.manual_seed(0)
    print(f"{name:9}", fit(build(hidden=32), epochs=200, lr=0.01, optimizer_name=name))

# %% Learning rate schedules lower the learning rate over time
model = build(hidden=32)
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)
rates = []
for epoch in range(30):
    rates.append(optimizer.param_groups[0]["lr"])
    optimizer.step()
    scheduler.step()
print([round(r, 4) for r in rates[::10]])

# %% Other tools you will meet
# Batch normalization / layer normalization: keep activations well scaled (nn.BatchNorm1d, nn.LayerNorm)
# Gradient clipping: torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
# Data augmentation: more varied training data for images and text
# Mixed precision, gradient accumulation: fit bigger models in memory
