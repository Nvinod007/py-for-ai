# A neural network is layers of: multiply by weights, add bias, apply an activation.
# Here is a full one in plain NumPy, including backpropagation, so nothing is hidden.

import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

# %% Data: two interleaving half circles (a straight line cannot separate them)
X, y = make_moons(n_samples=600, noise=0.2, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
y_train_col, y_test_col = y_train.reshape(-1, 1), y_test.reshape(-1, 1)

# %% Building blocks
def relu(z):
    return np.maximum(0, z)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


print(relu(np.array([-2, 0, 3])), sigmoid(np.array([-5.0, 0.0, 5.0])).round(3))
# Without activations, stacked layers collapse into ONE linear layer. Activations add the "bend".

# %% A network: 2 inputs -> 16 hidden -> 1 output
rng = np.random.default_rng(1)
W1, b1 = rng.normal(0, 0.5, (2, 16)), np.zeros((1, 16))
W2, b2 = rng.normal(0, 0.5, (16, 1)), np.zeros((1, 1))


def forward(X):
    z1 = X @ W1 + b1
    a1 = relu(z1)
    z2 = a1 @ W2 + b2
    return z1, a1, sigmoid(z2)


def accuracy(X, y):
    return ((forward(X)[2] > 0.5).astype(int) == y).mean()


print("accuracy before training:", round(accuracy(X_test, y_test_col), 3))

# %% Train with backpropagation (chain rule, layer by layer)
learning_rate = 0.5
for epoch in range(1, 1501):
    z1, a1, prediction = forward(X_train)
    loss = -np.mean(y_train_col * np.log(prediction + 1e-9) + (1 - y_train_col) * np.log(1 - prediction + 1e-9))

    n = len(X_train)
    d_z2 = (prediction - y_train_col) / n                  # gradient of the loss at the output
    d_W2 = a1.T @ d_z2
    d_b2 = d_z2.sum(axis=0, keepdims=True)
    d_a1 = d_z2 @ W2.T
    d_z1 = d_a1 * (z1 > 0)                                 # derivative of ReLU
    d_W1 = X_train.T @ d_z1
    d_b1 = d_z1.sum(axis=0, keepdims=True)

    W2 -= learning_rate * d_W2
    b2 -= learning_rate * d_b2
    W1 -= learning_rate * d_W1
    b1 -= learning_rate * d_b1

    if epoch % 300 == 0 or epoch == 1:
        print(f"epoch {epoch:4d} loss={loss:.4f} train_acc={accuracy(X_train, y_train_col):.3f} "
              f"test_acc={accuracy(X_test, y_test_col):.3f}")

# %% Predict
sample = np.array([[0.0, 0.5], [1.0, -0.5]])
print(forward(sample)[2].round(3).ravel())

# %% What you just built
# forward pass   -> predictions
# loss           -> how wrong
# backward pass  -> gradient for every weight
# update         -> weights -= learning_rate * gradient
# PyTorch automates exactly this (next file).
