# copy-pasted, with minor modifications, from:
# https://realpython.com/numpy-tensorflow-performance/

import time
import itertools as it
import numpy as np


np.random.seed(444)

N = 10000
sigma = 0.1
noise = sigma * np.random.randn(N)
x = np.linspace(0, 2, N)
d = 3 + 2 * x + noise
d.shape = (N, 1)

mu = 0.001
N_epochs = 10000


def py_descent(x, d, mu, N_epochs):
    N = len(x)
    f = 2 / N

    y = [0] * N
    w = [0, 0]
    grad = [0, 0]

    for _ in it.repeat(None, N_epochs):
        err = tuple(i - j for i, j in zip(d, y))
        grad[0] = f * sum(err)
        grad[1] = f * sum(i * j for i, j in zip(err, x))
        w = [i + mu * j for i, j in zip(w, grad)]
        y = (w[0] + w[1] * i for i in x)
    return w


def np_descent(x, d, mu, N_epochs):
    d = d.squeeze()
    N = len(x)
    f = 2 / N

    y = np.zeros(N)
    err = np.zeros(N)
    w = np.zeros(2)
    grad = np.empty(2)

    for _ in it.repeat(None, N_epochs):
        np.subtract(d, y, out=err)
        grad[:] = f * np.sum(err), f * (err @ x)
        w = w + mu * grad
        y = w[0] + w[1] * x
    return w


x_list = x.tolist()
d_list = d.squeeze().tolist()  # Need 1d lists

t0 = time.time()
py_w = py_descent(x_list, d_list, mu, N_epochs)
t1 = time.time()

t2 = time.time()
np_w = np_descent(x, d, mu, N_epochs)
t3 = time.time()

print(py_w)
print(np_w)

print('Python time: {:.2f} seconds'.format(round(t1 - t0, 2)))
print('NumPy time: {:.2f} seconds'.format(round(t3 - t2, 2)))
