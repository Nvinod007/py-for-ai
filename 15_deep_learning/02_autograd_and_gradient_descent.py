# Learning = nudging numbers to reduce an error.
# The gradient says which direction reduces the error. Autograd computes it for you.

import torch

# %% Gradient of y = x^2 at x = 3 should be 2x = 6
x = torch.tensor(3.0, requires_grad=True)
y = x**2
y.backward()
print(x.grad)

# %% A small chain: z = (2x + 1)^2, dz/dx = 4(2x + 1) = 28 at x = 3
x = torch.tensor(3.0, requires_grad=True)
z = (2 * x + 1) ** 2
z.backward()
print(x.grad)

# %% Gradient descent by hand: fit y = 2x + 1
torch.manual_seed(0)
xs = torch.linspace(-1, 1, 50)
ys = 2 * xs + 1 + 0.05 * torch.randn(50)

w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
learning_rate = 0.1

for step in range(101):
    prediction = w * xs + b
    loss = ((prediction - ys) ** 2).mean()          # mean squared error
    loss.backward()                                 # fills w.grad and b.grad
    with torch.no_grad():                           # update without tracking
        w -= learning_rate * w.grad
        b -= learning_rate * b.grad
    w.grad.zero_()                                  # gradients ADD UP, so reset them
    b.grad.zero_()
    if step % 25 == 0:
        print(f"step {step:3d} loss={loss.item():.4f} w={w.item():.3f} b={b.item():.3f}")

# %% Learning rate matters
def train(lr, steps=30):
    w = torch.tensor(0.0, requires_grad=True)
    for _ in range(steps):
        loss = ((w * xs - 2 * xs) ** 2).mean()
        loss.backward()
        with torch.no_grad():
            w -= lr * w.grad
        w.grad.zero_()
    return w.item()


for lr in (0.001, 0.1, 1.5, 3.0):
    print(f"lr={lr:5} -> w={train(lr):.3f}  (target is 2)")        # too small crawls, too big explodes

# %% Turn off gradients when predicting (faster, less memory)
with torch.no_grad():
    print((w * torch.tensor([0.5]) + b).item())

# %% Words
# loss      a number saying how wrong the model is (lower is better)
# gradient  how the loss changes if a weight changes
# epoch     one pass through all the training data
# batch     a small group of examples used for one update
