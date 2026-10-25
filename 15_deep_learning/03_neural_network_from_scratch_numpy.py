# A neural network is layers of: multiply by weights, add bias, apply an activation.
# Here is a full one in plain NumPy, including backpropagation, so nothing is hidden.
# Each line has a short comment saying WHAT it is.

# numpy: array maths.
import numpy as np
# make_moons: fake data of two curved half-moons.
from sklearn.datasets import make_moons
# train_test_split: splits data into train and test.
from sklearn.model_selection import train_test_split

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Data: two interleaving half circles (a straight line cannot separate them)
# make_moons(n_samples, noise, random_state): points in two moons; noise = jitter.
X, y = make_moons(n_samples=600, noise=0.2, random_state=0)
# train_test_split(..., test_size=0.25): 25% kept for testing; random_state repeats the split.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
# reshape(-1, 1): turn a flat list into a single column (-1 = figure out the length).
y_train_col, y_test_col = y_train.reshape(-1, 1), y_test.reshape(-1, 1)

# %% Building blocks
# ReLU activation: replaces negatives with 0 (an activation adds the 'bend' so networks learn curves).
def relu(z):
    return np.maximum(0, z)


# Sigmoid activation: squashes any number into 0..1 (like a probability); np.exp = e to the power.
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# Quick check of both activations; round(3) = 3 decimals.
print(relu(np.array([-2, 0, 3])), sigmoid(np.array([-5.0, 0.0, 5.0])).round(3))
# Without activations, stacked layers collapse into ONE linear layer. Activations add the "bend".

# %% A network: 2 inputs -> 16 hidden -> 1 output
# np.random.default_rng(1): random maker with a fixed seed.
rng = np.random.default_rng(1)
# Weights W (connection strengths) start random (rng.normal(mean, spread, shape)); biases b (offsets) start at zeros.
W1, b1 = rng.normal(0, 0.5, (2, 16)), np.zeros((1, 16))
# Second layer: 16 hidden -> 1 output.
W2, b2 = rng.normal(0, 0.5, (16, 1)), np.zeros((1, 1))


# Forward pass: input -> layer 1 -> ReLU -> layer 2 -> sigmoid. '@' = matrix multiplication.
def forward(X):
    z1 = X @ W1 + b1
    a1 = relu(z1)
    z2 = a1 @ W2 + b2
    return z1, a1, sigmoid(z2)


# Share of predictions (>0.5 means class 1) that match the true labels.
def accuracy(X, y):
    return ((forward(X)[2] > 0.5).astype(int) == y).mean()


print("accuracy before training:", round(accuracy(X_test, y_test_col), 3))

# %% Train with backpropagation (chain rule, layer by layer)
# learning_rate: size of each weight nudge.
learning_rate = 0.5
# epoch = one full pass through the training data.
for epoch in range(1, 1501):
    # Run the forward pass on all training data.
    z1, a1, prediction = forward(X_train)
    # loss = how wrong we are (cross-entropy: punishes confident wrong answers); np.mean = average, np.log = natural log, 1e-9 avoids log(0).
    loss = -np.mean(y_train_col * np.log(prediction + 1e-9) + (1 - y_train_col) * np.log(1 - prediction + 1e-9))

    # n = number of training rows.
    n = len(X_train)
    # Backpropagation: work backwards using the chain rule to get the gradient (d_) of the loss for every weight.
    d_z2 = (prediction - y_train_col) / n                  # gradient of the loss at the output
    # a1.T = transpose (swap rows/columns).
    d_W2 = a1.T @ d_z2
    # sum(axis=0, keepdims=True): total down the rows, keeping 2D shape.
    d_b2 = d_z2.sum(axis=0, keepdims=True)
    d_a1 = d_z2 @ W2.T
    # (z1 > 0) is the ReLU slope: 1 where positive, 0 otherwise.
    d_z1 = d_a1 * (z1 > 0)                                 # derivative of ReLU
    d_W1 = X_train.T @ d_z1
    d_b1 = d_z1.sum(axis=0, keepdims=True)

    # Update: move each weight a little against its gradient.
    W2 -= learning_rate * d_W2
    b2 -= learning_rate * d_b2
    W1 -= learning_rate * d_W1
    b1 -= learning_rate * d_b1

    # Print on epoch 1 and every 300th.
    if epoch % 300 == 0 or epoch == 1:
        print(f"epoch {epoch:4d} loss={loss:.4f} train_acc={accuracy(X_train, y_train_col):.3f} "
              f"test_acc={accuracy(X_test, y_test_col):.3f}")

# %% Predict
# Two new points to predict.
sample = np.array([[0.0, 0.5], [1.0, -0.5]])
# [2] = output probabilities; ravel() flattens.
print(forward(sample)[2].round(3).ravel())


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% What you just built
# forward pass   -> predictions
# loss           -> how wrong
# backward pass  -> gradient for every weight
# update         -> weights -= learning_rate * gradient
# PyTorch automates exactly this (next file).
