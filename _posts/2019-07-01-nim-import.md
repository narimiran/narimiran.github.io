---
layout: post
title: Imports in Nim
date: 2019-07-01
---

One of the two major complaints about Nim, mostly from people who *don't* use Nim, is the way imports are handled.[^1]

[^1]: The other is case and style insensitivity, which *also* has its advantages, and the downsides are not nearly as bad as people *think*, but this is better left for some other blog post.

The majority of these complaints come from people who work in Python, and see Nim as a potential Python replacement or a language they can use to speed up parts of their existing code.
Two years ago I was one of those people: I came from the Python world, I had just started using Nim, and I immediately started complaining on #nim IRC channel about "wrong imports".

This post is inspired by the realization that in those two years of using Nim I not even *once* had a problem with the imports, and to help other newcomers to Nim by answering what is probably the most common question about Nim imports:

> Why are you the way that you are? --- Michael Scott


## Python imports

Every Python programmer should be familiar with PEP-8, which is a style guide for Python code.
In its [imports section](https://www.python.org/dev/peps/pep-0008/#imports), there is, among others, the following recommendation:

> Wildcard imports (`from <module> import *`) should be avoided, as they make it unclear which names are present in the namespace, confusing both readers and many automated tools.

This excerpt can be easily explained and justified by the following example:
```python
from math import *
from cmath import *
from numpy import *

print(sqrt(-4))
```
Not only does it confuse "both readers and many automated tools", it also does different things based on the order of the imports, because the latter ones overwrite the functions of the same name of the previous ones.
The code as it is written above produces `RuntimeWarning: invalid value encountered in sqrt`.
Had the `cmath` import been the last one, it would have printed `2j`.

A similar overwriting behaviour can be observed when one uses a name of an existing function for their variable name.
The usual offenders are variable `list`, for some unimportant list which doesn't even deserve its dedicated meaningful name, and a variable `sum`, for the result of some manual addition.
After you create those two variables, you can no longer use built-in `list` to convert an iterable to a list, nor `sum` to give you a sum of some numeric iterable.
Python allows you to do this without any warning.

Soon enough, Python developers learn to use `import modulename` and then `modulename.function_name`, so it doesn't overwrite `othermodule.function_name`.
This works great, it solves the real problem and it makes things easier --- why doesn't Nim just copy that?



## The Nim way

Nim offers several different ways to import modules and functions, but the usual complaint is that `import modulename` doesn't work the same as in Python, i.e. it doesn't *force* you to fully qualify access to the imported symbols: you can just do `functionName`, without specifying which module it comes from.
It sure does feel like the Python's star-import (`from modulename import *`), which, as we have seen, is a big no-no.

First off, those two are not equivalent.
Unlike Python's star-import, Nim still allows you to fully qualify the accessed symbols (`modulename.functionName`) if you prefer the Python way of doing things.[^2]

[^2]: Some other ex-Pythonista giveaways are 4-space indentation (Nim prefers two spaces) and `snake_case` (Nim prefers `camelCase`).

Alternatively, if you only import a function or two, you can use the same syntax (with the same behaviour) as in Python: `from modulename import func1, func2`.
A similar syntax, `from modulename import nil`, can be used if you prefer to *enforce* fully qualified access to give you the familiar Python behaviour.
This is usually discouraged and it will backfire sooner or later (more on that in the next section), but if you insist this is the only import behaviour that you're willing to work with, Nim gives you that opportunity.

If you are a stubborn Pythonista who sticks to PEP-8 even in other languages, the options mentioned above will give you the Python imports that you want.
On the other hand, if you would like to see *why* the Nim way of importing isn't really a problem in Nim (but it is in Python) and maybe embrace the star-like imports in the future, keep on reading.



## How it works

Consider a following Nim code:
```nim
import math, complex

var
  f = -4.0
  z = complex(-4.0)

echo sqrt(f)
echo sqrt(z)
```

Unlike the Python example above, there is no ambiguity about which `sqrt` to call in these two cases (nor is there any overwriting happening) because Nim is statically typed and the compiler can disambiguate between the functions of the same name but with different signatures:
```nim
# math.nim
proc sqrt*(x: float32): float32
proc sqrt*(x: float64): float64

# complex.nim
proc sqrt*[T](z: Complex[T]): Complex[T]
```

Nimsuggest, Nim's tool to give IDE-like capabilities, is not "confused" by the original code: go-to-definition works correctly in any code editor which supports Nim via plugins.[^3]

[^3]: VS Code, Vim and Neovim, Emacs, SublimeText, to name a few.

You might want to do `math.sqrt(f)` and `complex.sqrt(z)` for your own sake, but if you want to blindly follow the Python way, then you should also do `z = complex.complex(-4.0)`.
This not only gets tiresome, it makes the code downright ugly and *harder* to read:

```nim
from complex import nil
from tables import nil

var
  z1 = complex.complex(5.0, 2.0)
  z2 = complex.complex(10.0, -3.0)

var t = tables.initTable[int, complex.Complex64]()
tables.`[]=`(t, 1, z1)
tables.`[]=`(t, 2, z2)
echo complex.`+`(tables.`[]`(t, 1), tables.`[]`(t, 2))
```

In the above example, we forced everything to be fully qualified, we can easily see where the stuff comes from, but I'm not sure this is more readable than the idiomatic Nim:
```nim
import complex, tables

var
  z1 = complex(5.0, 2.0)
  z2 = complex(10.0, -3.0)

var t = initTable[int, Complex64]()
t[1] = z1
t[2] = z2
echo t[1] + t[2]
```

Do we really need a constant reminder that the addition of two complex numbers is defined in the `complex` module, or that setters (`[]=`) and getters (`[]`) for tables are defined in the `tables` module?

You can think of Nim modules as a set of functions operating on a specific type introduced in that module.
This is, in fact, quite similar to Python classes and their methods, for which PEP-8 states:

> When importing a class from a class-containing module, it's usually okay to spell this:
```python
from myclass import MyClass
from foo.bar.yourclass import YourClass
```
> If this spelling causes local name clashes, then spell them explicitly

This is exactly what Nim offers you with its `import module` --- you can directly use "classes" and their "methods", just like you would in Python.



### Name collisions

If there are two functions with the same name *and* the same signature from two different imported modules
```nim
import complex
import mycomplex

var z = complex(8.0, -6.0)

echo abs(z)
```
we will get an error at compile time about the ambiguity:
```
Error: ambiguous call;
both mycomplex.abs(x: Complex[abs.T])
[declared in /home/.../mycomplex.nim(7, 6)] and
complex.abs(z: Complex[abs.T])
[declared in /home/.../lib/pure/complex.nim(44, 6)]
match for: (Complex[system.float64])
```

To solve this we can fully qualify just those clashing functions, without a need to change how a module is imported or the way the other functions from that module were invoked.
(Unlike Python, where this would cause much larger refactoring.)
Alternatively, if we're interested only in one of those clashing functions, we can use `import modulename except someFunction`:
```nim
import complex except abs
import mycomplex

var z = complex(8.0, -6.0)
var abs = 6

echo abs(z)
echo abs
echo abs(-7)
```

Notice that we introduced `abs` variable, trying to provoke a name collision like in the Python example (`list` and `sum` variables) but this is not a problem in Nim.



## Conclusion

Coming from Python, it is easy to dismiss things that remind us of Python anti-patterns --- there is a reason why people advice against them.
*In Python*.

Nim's syntax is deceiving.
On the surface it looks like it is just "Python with static typing", and it is hard to see why it differs from Python in some details.
The truth is that Nim is much more than that, and some design choices are there for a reason and they make sense *in Nim*.

Hopefully this article sheds some light on that and it will motivate you to dive deeper into Nim and discover some of its hidden goodies, not visible when looking at it from the distance.

&nbsp;

> Discussion on [Reddit](https://old.reddit.com/r/programming/comments/c7t1ct/imports_in_nim/) and [lobste.rs](https://lobste.rs/s/zi4ttl/imports_nim).
