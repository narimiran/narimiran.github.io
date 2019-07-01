---
layout: post
title: Python vs NumPy vs Nim
date: 2018-05-10
---


Yesterday I've stumbled on the article [Pure Python vs NumPy vs TensorFlow Performance Comparison](https://realpython.com/numpy-tensorflow-performance/) where the author gives a performance comparison of different implementations of gradient descent algorithm for a simple linear regression example.

Lately I've been experimenting with the [Nim programming language](https://nim-lang.org/), which promises to offer a Python-like easy to read syntax, while having C-like speeds.
This seemed like a nice and simple example to compare speed between Nim and Python.



## Python results

As _everybody_ would expect, [the article has shown](https://realpython.com/numpy-tensorflow-performance/#conclusion) that the pure Python version is much slower than the other two versions, but _nobody_ would write numerical code like that.

NumPy allows us to write both more readable and much faster code, as it takes advantage of vectorised operations on NumPy arrays, and usually calls optimized C or Fortran code.

The code from the original article is used without modifications, I have just re-run it on my machine (i7-970 @ 3.20 GHz) to get the base values for a later comparison:

```
Python time: 34.62 seconds
NumPy time: 0.71 seconds
```



## Enter Nim

Based on [my previous experience](https://github.com/narimiran/AdventOfCode2017) of using both Nim and Python, I knew I could expect Nim to be noticeably faster than (pure) Python.
The question is -- can Nim compete against NumPy's speed?

We'll take "pure Nim" approach -- no array/tensor library, meaning we need to iterate the arrays element by element, something that is known to be very costly in Python.

Let's go through our program bit by bit:

```nim
import random, times, math

randomize(444)

const
  N = 10_000
  sigma = 0.1
  f = 2 / N
  mu = 0.001
  nEpochs = 10_000
```

Compared to Python, in Nim all imports are written on the same line, and importing a module in Nim is analogous to `from foo import *` in Python.

We take the same seed as in the original, and we define all the needed constants. (All indented lines are part of the `const` block.)
Nim is a statically typed language, but the types can be inferred from the values.

Next we need to define vectors `x` and `d` (`x = np.linspace(0, 2, N)` and `d = 3 + 2 * x + noise` in Python), and we need to do it element by element:

```nim
var x, d: array[N, float]
for i in 0 ..< N:
  x[i] = f * i.float
  d[i] = 3.0 + 2.0 * x[i] + sigma * randomNormal()
```

Operator `..<` iterates _until_ the upper limit. (Operator `..` would iterate to the limit, including it.)

The thing to notice here is that we cannot combine integers and floats -- `i` needs to be converted to float. (Nim has [UFCS](https://en.wikipedia.org/wiki/Uniform_Function_Call_Syntax) support so `i.float` is the same as `float(i)`.)

Function `randomNormal`, which gives us a Gaussian distribution (`np.random.randn` in the Python version), is taken from [Arraymancer](https://mratsim.github.io/Arraymancer/), which is Nim's tensor library (still in early stage, but it is rapidly developed).

The remaining thing to do is to define the `gradientDescent` function:

```nim
proc gradientDescent(x, d: array[N, float], mu: float, nEpochs: int):
                     tuple[w0, w1: float] =
  var
    y: array[N, float]
    err: float
    w0, w1: float

  for n in 1 .. nEpochs:
    var grad0, grad1: float

    for i in 0 ..< N:
      err = f * (d[i] - y[i])
      grad0 += err
      grad1 += err * x[i]

    w0 += mu * grad0
    w1 += mu * grad1

    for i in 0 ..< N:
      y[i] = w0 + w1 * x[i]

  return (w0, w1)
```

When declaring variables, they are initialized with their default values (0.0 for floats), meaning that `var y: array[N, float]` is similar to `y = np.zeros(N, dtype=float)` in Python.

Lastly, we print the values of `w0` and `w1`, to see if the values are close to the ones we expect (`w0 = 3`, `w1 = 2`) and measure the time needed for the calculation:

```nim
let start = cpuTime()
echo gradientDescent(x, d, mu, nEpochs)
echo "Nim time: ", cpuTime() - start, " seconds"
```


## Nim results

We compile the program in [release mode](https://nim-lang.org/docs/nimc.html#additional-compilation-switches), which turns off runtime checks and turns on the optimizer, and run it:

```
$ nim c -d:release gradDesc.nim
$ ./gradDesc

(w0: 2.968954757075724, w1: 2.02593328759163)
Nim time: 0.226344 seconds
```


Version | Time (s) | Speedup vs Python | Speedup vs NumPy
|:---|---:|---:|---:|
Python | 34.62 | - | 0.02x
NumPy | 0.71 | 48.76x | -
Nim | 0.226 | 153.19x | 3.14x


While NumPy has offered significant speedups compared to the pure Python version, Nim manages to further improve upon that, and not just marginally -- it is two orders of a magnitude faster than Python, and, what is more impressive, it is three times faster than NumPy.

Nim has managed to deliver on its promise -- for this example it offers 3x performance compared to NumPy, while keeping the code readable.

&nbsp;

> Discussion on [Reddit](https://www.reddit.com/r/programming/comments/8ilinf/python_vs_numpy_vs_nim/) and [Hacker News](https://news.ycombinator.com/item?id=17045230).
>
> Source files (both .py and .nim) are available [here](https://github.com/narimiran/narimiran.github.io/tree/master/code/python-numpy-nim).
