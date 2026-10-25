# Learning = nudging numbers to reduce an error.
# The gradient says which direction reduces the error. Autograd computes it for you.
# Each line has a short comment saying WHAT it is.

# torch (PyTorch): tensors and automatic gradients.
import torch

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Gradient of y = x^2 at x = 3 should be 2x = 6
# requires_grad=True: PyTorch records maths on x so it can work out gradients (how the result changes if x changes).
x = torch.tensor(3.0, requires_grad=True)
# x**2 = x squared.
y = x**2
# backward(): computes gradients of y for every tracked value (autograd).
y.backward()
# x.grad: the gradient stored on x.
print(x.grad)

# %% A small chain: z = (2x + 1)^2, dz/dx = 4(2x + 1) = 28 at x = 3
# New tracked x (fresh gradient).
x = torch.tensor(3.0, requires_grad=True)
z = (2 * x + 1) ** 2
z.backward()
print(x.grad)

# %% Gradient descent by hand: fit y = 2x + 1
# manual_seed(0): fixes random numbers so results repeat.
torch.manual_seed(0)
# linspace(-1, 1, 50): 50 evenly spaced numbers; randn(50): random noise.
xs = torch.linspace(-1, 1, 50)
# Target values: the line 2x + 1 plus a little noise.
ys = 2 * xs + 1 + 0.05 * torch.randn(50)

# w = weight (slope) to learn, starts at 0.
w = torch.tensor(0.0, requires_grad=True)
# b = bias (offset) to learn, starts at 0.
b = torch.tensor(0.0, requires_grad=True)
# learning_rate: size of each nudge (too big overshoots, too small is slow).
learning_rate = 0.1

# One step = one try and one nudge of the numbers.
for step in range(101):
    # The model's guess: w * x + b.
    prediction = w * xs + b
    # loss = how wrong we are (here mean squared error: average of squared mistakes); .mean() = average.
    loss = ((prediction - ys) ** 2).mean()          # mean squared error
    # backward(): computes gradients of loss for w and b.
    loss.backward()                                 # fills w.grad and b.grad
    # no_grad(): do the next lines without recording gradients.
    with torch.no_grad():                           # update without tracking
        # Nudge w opposite to its gradient (downhill).
        w -= learning_rate * w.grad
        b -= learning_rate * b.grad
    # zero_(): resets gradient to 0 in place.
    w.grad.zero_()                                  # gradients ADD UP, so reset them
    b.grad.zero_()
    # % = remainder; true every 25th step.
    if step % 25 == 0:
        # item(): one-number tensor -> normal Python number; :.4f = 4 decimals.
        print(f"step {step:3d} loss={loss.item():.4f} w={w.item():.3f} b={b.item():.3f}")

# %% Learning rate matters
# Trains one weight with a given learning rate and returns it.
def train(lr, steps=30):
    w = torch.tensor(0.0, requires_grad=True)
    for _ in range(steps):
        loss = ((w * xs - 2 * xs) ** 2).mean()
        loss.backward()
        with torch.no_grad():
            w -= lr * w.grad
        w.grad.zero_()
    return w.item()


# Try several learning rates.
for lr in (0.001, 0.1, 1.5, 3.0):
    print(f"lr={lr:5} -> w={train(lr):.3f}  (target is 2)")        # too small crawls, too big explodes

# %% Turn off gradients when predicting (faster, less memory)
# no_grad(): turns off gradient tracking for speed.
with torch.no_grad():
    print((w * torch.tensor([0.5]) + b).item())


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Words
# loss      a number saying how wrong the model is (lower is better)
# gradient  how the loss changes if a weight changes
# epoch     one pass through all the training data
# batch     a small group of examples used for one update
