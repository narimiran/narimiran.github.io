---
layout: post
title: "Advent of Clojure: Need for Speed"
date: 2023-01-17
---

[Advent of Code](https://adventofcode.com/) (AoC) is a series of fun programming challenges, released every December.
People solve the tasks in a variety of programming languages, and I find them great for the purpose of learning a new language.

Each year I usually solve the tasks in two or more languages: first in a language I'm very familiar with (so I can concentrate on the task at hand) and after that in a language I'm trying to learn, using my initial solution as a template of what I'm trying to achieve.
In the past, that is how I started learning Nim, OCaml and Racket.

This year I decided I would use AoC to learn Clojure.

Learning Clojure was a very pleasant experience and I really liked the language, but one thing I noticed throughout December: Clojure was slow.
Often slower than my Python solutions taking the same approach and using the same algorithm.
I was surprised and disappointed.
What was going?

But let's start from the beginning...


> This article is aimed at Clojure beginners, where I (as another Clojure beginner) will try to show things that I discovered along the way, and which I wish I had known from the start.





## Clojure: setting up the project

I have experience with Lisp syntax (Racket) and functional programming (OCaml), so, broadly speaking, I shouldn't have a problem writing a simple Clojure program.
But starting a Clojure project?

Lately I've been increasingly using VSCode editor (instead of my usual Neovim), so I searched for some Clojure extension and found and installed [Calva](https://calva.io).
Calva has been a great experience, and I can recommend learning some if its [Top 10 Commands](https://calva.io/commands-top10/), which I frequently use while developing.

At the time, I didn't know about the existence of [Leiningen](https://leiningen.org), so I had some problems with connecting my project to the REPL.
This was solved thanks to the help from [Discljord community](https://discord.gg/discljord) on Discord, who explained to me that I need to have at least a basic `deps.edn` file containing the following:

```clj
{:paths ["clojure"]
 :deps {org.clojure/clojure {:mvn/version "1.11.1"}}}
```

Here `"clojure"` is a name of a subfolder where my Clojure solutions reside (I have a subfolder for each language I'm solving in).
Usually, this would be `"src"`.






## Before you start


### Clojure-specific syntax

Clojure is a Lisp, so it is just a bunch of lists inside of parentheses, right?

Not really.
You are not limited to that.

- `[1 3 9]` is a vector.
- `{1 5 2 7}` is a map (a.k.a. table, dictionary). Notice no colons (`:`), commas, or any other punctuation.
  It has the even number of elements, where each odd element is a key.
  Since Clojure treats commas as a whitespace, I prefer to write it `{1 5 , 2 7}` or to put every key-value pair on its own line, to make it more obvious what is a key and what is a value.
  This example is an equivalent of this Python dict: `{1: 5, 2: 7}`.
- `#{5 3}` is a set. Notice the `#`. (Without it, this would be a map with one key-value pair.)
- `(fn [x] (* 5 x))` is an anonymous function.
  You can use it as a predicate to the `map` function (not to be confused with map data structure mentioned above), e.g. `map (fn [x] (* 5 x)) xs`, where `xs` is a collection of numbers.
- `#(* 5 %)` is a short way of writing an anonymous function, and it is equivalent to the example above.
  The `%` is used instead of the argument.
  If your function takes multiple arguments, you can use `%1` for the first argument, `%2` for the second, etc.
  But at that point, using the `fn` construct from above is more readable, or even creating a non-anonymous function.

In REPL, you sometimes want to reuse the last result.
You can use up to three last results and the syntax is `*1` for the last one, `*2` for the one before, etc.




### Differences to Racket

I could go in great lengths comparing and contrasting Racket and Clojure, but I'll try to keep it short by mentioning just two differences I immediately noticed.
One is a simple stylistic choice (in Racket), and the other is something I really wanted to have when I was using Racket.

In Racket, it is preferred to use `define` instead of `let` (see Section 4.2 [here](https://docs.racket-lang.org/style/Choosing_the_Right_Construct.html)).
I tried to do the same in Clojure, by writing some `def` inside a function, and was greeted with "inline def" warning.
It turns out that `def` would produce global binding, which is something we don't want to do in 98% of cases.

The other 2%?
It is a useful debugging tool, when we want to know the value of some internal variable.
For example:

```clj
(def y 10) ; global y

(defn func1 [x]
  (let [y (do-something x)] ; local y
    (def y-from-func1 y)    ; capture local y
    (->> y
         (map func2)
         (reduce +))))
```

By using `(def y-from-func1 y)` we can now inspect the value of the local `y` in the REPL and use it (test it) outside that function.
The name `y-from-func1` was chosen not to clash with the global `y`; if you are not worried about namespace pollution, you can simply do `(def y y)`.

&nbsp;

The other immediately noticeable difference is that we can finally do a simple and elegant destructuring of function's arguments and variables.
It doesn't seem like much, but for me, it is a nice quality-of-life improvement.

Consider this simple example in Python:

```py
def manhattan(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return dx + dy

print(manhattan((2, 5), (3, 7)))
```

In Racket you would do something similar to that example, by using `(match-define (list x1 y1) pt1)` inside the function, and so on.
But this is very verbose, and it gets boring and tiring repeating it over and over again.
Clojure solves this by having destructuring possible directly on function arguments:

```clj
(defn manhattan [[x1 y1] [x2 y2]]
  (let [dx (abs (- x2 x1))
        dy (abs (- y2 y1))]
    (+ dx dy)))

(manhattan [2 5] [3 7])
```

Destructuring in Clojure is more powerful and useful than just that.
I recommend reading [the official article about it](https://clojure.org/guides/destructuring).






## Writing first programs

When it comes to translating a known program to a new language, the problem usually isn't _what_ to do, but _how_ to do it, i.e. what is available in the standard library and how to use it.

For example, if you want the nth element of a sequence (`xs[n]` in Python) you would use the `nth` function with the index you want.
If you want first n elements (`xs[:n]`), you would use `take` and specify the amount.
In the beginning, the problem for me was that these two functions have different order of arguments.
You would do `(nth xs n)`, but `(take n xs)`.
(Can you guess the order of the arguments for the function whose name is the mix of those two, `take-nth`? :))

Something that helped me immensely and what is constantly open in my browser window next to the editor is [Clojure Cheat Sheet](https://jafingerhut.github.io/cheatsheet/clojuredocs/cheatsheet-tiptip-cdocs-summary.html).
It is grouped in various sections, which not only helped me to see how to use some function, but also to discover new ones.

One day I was checking the documentation for `concat`, just to discover right next to it that `mapcat` exists and I could use that instead; and in that group are also `interleave` and `interpose`, so I learnt about those too.
When I was doing some set operations, by checking what the cheat sheet has in the Sets section, I discovered `clojure.data.int-map` which I now use when I have sets or maps with integers.
And so on.

The tutorial which I followed was [Clojure from the ground up](https://aphyr.com/tags/Clojure-from-the-ground-up), and I've read the free online version of [Clojure for the brave and true](https://www.braveclojure.com/clojure-for-the-brave-and-true/).
Other learning materials can be found in this ["opinionated list of excellent Clojure learning materials"](https://gist.github.com/ssrihari/0bf159afb781eef7cc552a1a0b17786f).

This was enough to solve all 25 AoC tasks.
Slowly.



## Need for Speed

One of my main goals, besides learning a new language, of solving AoC tasks this time was to try to provide simple and idiomatic solutions.
Writing fast solutions was _not_ my main goal.
(It was back in 2017 when I managed to [run all 25 tasks in 500 ms in total using Nim](https://github.com/narimiran/AdventOfCode2017).)

But writing _slow_ solutions was also not my goal.

I'll try to list some performance tips and gotchas that helped me gain some performance.
Sometimes it was just a minor improvement of couple percents, but some other times it was almost an order of magnitude faster.

I will start with some simple things, and then move to more specific ones and those which need a bit more involvement.
Note that these will not work every time nor for every task.
The performance gains will depend on the domain size, the amount of work you need to do, etc.

I won't talk about algorithmic improvements you can do, which would help the execution times in any programming language.
My goal is just to show you some ideas what to try to do or avoid in your Clojure programs.

> While I'll show some examples of AoC programs, I'll try to keep it as much spoiler-free as possible.



### Criterium

If I want to improve the execution times, I need to have exact measurements to see if there are any improvements, and how large they are.
Early on I discovered I cannot trust the times reported by the `time` macro.
Enter [Criterium](https://github.com/hugoduncan/criterium).

To use Criterium, first we have to install it.
That means adding it as an extra dependency to the already mentioned `deps.edn` file:

```clj
{:paths ["clojure"]
 :deps {org.clojure/clojure {:mvn/version "1.11.1"}
        criterium/criterium {:mvn/version "0.4.6"}}}
```

On the next REPL restart, it will be downloaded and ready to use.
I would use it just inside the REPL, when I was in the namespace of some tasks.
For example, for `day01.clj`:

```
clj꞉day01꞉> (require '[criterium.core :as c])
nil

clj꞉day01꞉> (c/quick-bench (solve))
Evaluation count : 1296 in 6 samples of 216 calls.
             Execution time mean : 489.977542 µs
    Execution time std-deviation : 21.294806 µs
   Execution time lower quantile : 470.625722 µs ( 2.5%)
   Execution time upper quantile : 514.017624 µs (97.5%)
                   Overhead used : 4.212424 ns
nil
```

The `require` is needed only once per namespace.
For each following time, only `(c/quick-bench (solve))` is needed.

One "trick" that I did was to have `solve` function in each task, which includes both parsing the input (without any arguments, `solve` would load the real input for that day) and solving both parts of the task.
This way it was easy just to switch the namespace and run the same `quick-bench` command, without the need to change anything, which made benchmarking much easier.





### `map` vs `pmap`

We start with an easy one.
Just one letter change.

If there is a lot of work to do with each element of your collection, why do it sequentially when you can do it parallel?

Not a lot of AoC tasks where I found it beneficial: usually there is low amount of elements and simple operations on them, so the benefits don't overcome the coordination overhead, but it is a simple change and easy to test it.




### `future`

On a similar note, why wait for part 1 of a task to finish before you start working on a solution for part 2?

My `solve` function always returns a vector of solutions for each part.
Instead of doing something like this:

```clj
(defn solve [input]
  (let [blueprints (parse-input input)]
    [(part-1 blueprints)
     (part-2 blueprints)]))
```

We can use `future` which will calculate the expression in another thread, and then deref the result with `@`:

```clj
(defn solve [input]
  (let [blueprints (parse-input input)
        p1 (future (part-1 blueprints))
        p2 (future (part-2 blueprints))]
    [@p1 @p2]))
```

Once again, don't expect it to work every time, but it is something to consider.




### Use `rseq` instead of `reverse`

If you are having a vector you need to reverse (e.g. [Day 8](https://adventofcode.com/2022/day/8)), be careful how you do it:

```
clj꞉user꞉> (def v (vec (range 1000)))
#'user/v

clj꞉user꞉> (c/quick-bench (doall (reverse (take 300 v))))
Evaluation count : 20544 in 6 samples of 3424 calls.
             Execution time mean : 32.882534 µs
    Execution time std-deviation : 5.049151 µs
   Execution time lower quantile : 28.780374 µs ( 2.5%)
   Execution time upper quantile : 39.038014 µs (97.5%)
                   Overhead used : 4.212424 ns
nil

clj꞉user꞉> (c/quick-bench (doall (reverse (subvec v 0 300))))
Evaluation count : 35406 in 6 samples of 5901 calls.
             Execution time mean : 17.570030 µs
    Execution time std-deviation : 656.424709 ns
   Execution time lower quantile : 17.147678 µs ( 2.5%)
   Execution time upper quantile : 18.453735 µs (97.5%)
                   Overhead used : 4.212424 ns
nil

clj꞉user꞉> (c/quick-bench (doall (rseq (subvec v 0 300))))
Evaluation count : 220278 in 6 samples of 36713 calls.
             Execution time mean : 3.411845 µs
    Execution time std-deviation : 846.943934 ns
   Execution time lower quantile : 2.703574 µs ( 2.5%)
   Execution time upper quantile : 4.443904 µs (97.5%)
                   Overhead used : 4.212424 ns
nil
```


We use `doall` to get rid of the laziness which would skew the results.
See the Common mistakes section [here](http://clojure-goes-fast.com/blog/benchmarking-tool-criterium/).

Using `subvec` and `rseq` is one order of magnitude faster than the initial solution with `take` and `reverse`.




### `int-set` vs `set`

The package [int-map](https://github.com/clojure/data.int-map) provides optimized maps and sets, when keys/members are integers.

If you already have integers in your set or map keys, the change in code is trivial.
For map, change `into {}` to `into (int-map)`.
For sets, you have two options, `int-set` and `dense-int-set`, depending on how dense are your members.
I always try both options, to see which one works faster.
The latter one is usually more performant for AoC tasks.

In lots of AoC tasks, you don't have integer keys, but x-y coordinates on some 2D grid.
If you are willing to lose some readability and elegance, you can turn an `[x y]` vector to some `(+ x (* const y))` integer, and then use `int-map` and traverse the map by doing integer arithmetic, instead of operations on vectors.
I've seen 85% cut in the execution times by doing that.



### Other set-related slowness

Sets are generally powerful, and I like to use them whenever I can in any programming language, and in Clojure they have one additional benefit: they can be used as a predicate function.
For example, if you want to keep all members of a vector whose value is either 1 or 2, there are two ways to write a predicate --
using a function or using a set:

```clj
(filter #(or (= % 1) (= % 2)) [1 2 3 4 3 2 1])

(filter #{1 2} [1 2 3 4 3 2 1])
```

In [Day 17](https://adventofcode.com/2022/day/17) I had to check if two vectors are disjoint (don't contain any common members).
My idea was to convert one of them to set:

```clj
(defn not-clashes? [rock tower]
  (not-any? (set rock) tower))
```

The problem was this was inside a nested loop, and I was creating lots and lots of sets just to do that check.
The solution was, in hindsight, simple and obvious:
The `tower` vector was constant for the whole duration of the inner loop, and I could convert it to set just once per outer loop's step, and there were no conversions in the inner loop:

```clj
(defn not-clashes? [rock tower]
  (not-any? tower rock))
```

This cut the execution time in half!

&nbsp;

The other mistake I did with sets was in [Day 19](https://adventofcode.com/2022/day/19), where I had a `seen` set in which I've put every state visited.
Each set member was a `[t bots resources]` vector, where `t` was time remaining, `bots` were available robots and `resources` were resources for that time in that scenario.

The problem?
Notice the plural names.
Those last two elements of a vector were, in fact, maps:

```clj
; initial states:
:bots      {:ore 1 , :clay 0 , :obs 0 , :geode 0}
:resources {:ore 0 , :clay 0 , :obs 0 , :geode 0}
```

The `seen` set had members which were nested structures (vectors containing maps).
The remedy was applied in three steps:

1. Instead of those two maps, hash their values, so the set members are now vectors of integers, roughly: `[t (calc-hash-1 bots) (calc-hash-2 resources)]`.
2. This vector can be turned into an integer: `(calc-hash t bots resources)`.
3. Now `seen` can be a `dense-int-set`.

The result of all three steps was a significant cut in the execution time:
From almost 5 seconds, down to around 600 milliseconds.




### Use `transduce`

One of the recurring themes of AoC tasks is to `map` or `filter` some collection, and then find a sum or product of the result:

```clj
(->> xs
     (map some-func)
     (reduce +))

(->> xs
     (filter some-pred?)
     (reduce *))
```

We are not interested in the sequences produced by `map` and `filter`, so it is the best to avoid them in the first place.
It might not matter if you're doing this once, but if you are inside a nested loop, this redundancy builds up.
The solution is to replace those constructs with `transduce`:

```clj
(transduce (map some-func) + xs)

(transduce (filter some-pred?) * xs)
```





### (Un)boxed math

If you execute the following in your REPL, now every time you evaluate some function it will warn you if you're doing some boxed arithmetic:

```
clj꞉user꞉> (set! *unchecked-math* :warn-on-boxed)
```

```clj
(defn some-func [x y]
  (+ x (inc y)))

; Boxed math warning, (...)/output.calva-repl:xx:8 -
; (...) unchecked_inc(java.lang.Object).
;
; Boxed math warning, (...)/output.calva-repl:xx:3 - 
; (...) unchecked_add(java.lang.Object,java.lang.Object).
```

To address those warnings, you should type-hint your operands and/or function arguments.
You should, additionally, type hint the function return type too.

```clj
(defn some-func ^long [^long x ^long y]
  (+ x (inc y)))
```

From my limited experience, the gains are usually small, and there's no need to do this everywhere where the warning points you (it shows line and column, so it is easy to find offending operands).
You might notice some benefits inside hot loops.




### Use `transient`

If you have a collection you're modifying a lot, e.g. inside a `reduce`, consider making it `transient` and using the bang-version of the functions (`conj!`, `assoc!`, etc.):

```clj
(defn move [elves proposals]
  (->> proposals
       (reduce-kv (fn [elves prop old]
                    (-> elves
                        (disj! old)
                        (conj! prop)))
                  (transient elves))
       persistent!))
```

See [the official article about transient data structures](https://clojure.org/reference/transients).







### Quick ones

- Maybe not idiomatic Clojure, but sometimes it is the best (fastest) to use mutable Java arrays and modify them.

- `not-any?` can be slow. Write your own, faster, version:

  ```clj
  (defn none? [pred xs]
    ;; Faster version of `not-any?`.
    (reduce
     (fn [acc x]
       (if (pred x)
         (reduced false)
         acc))
     true
     xs))
  ```

- Checking if a container is `empty?` before using it can be, relatively speaking, slow.
  See if you can use `if-let`.

- Don't create a map just to `merge` it with the existing one. Use `assoc`.

  ```clj
  (let [grid (merge grid {start 0 end 25})]
    ...)

  (let [grid (-> grid
                 (assoc start 0)
                 (assoc end 25))]
    ...)
  ```

- `update-in` works on variable number of arguments, hence it can be slow.
  If you are always the same amount of layers deep, write your own version:

  ```clj
  (defn update-monkeys [m k1 k2 f]
    ;; Much faster than the `update-in` built-in.
    (let [m2 (m k1)]
      (assoc m k1 (assoc m2 k2 (f (k2 m2))))))
  ```

- `loop` might be slightly faster than `reduce`. (But I still prefer to use `reduce`.)

- Experiment with [Reducers](https://clojure.org/reference/reducers) and using `r/fold` instead of `reduce`.







## Conclusion

There are, of course, other things you can do on top of the ones mentioned in this article, but the ultimate speed was never my main goal.
I wanted clean, readable solutions with reasonable speed, i.e. without the penalties due to my lack of knowledge of the language.

Initially, I had some tasks which took more than 10 seconds to run.
My main problem was that it was very hard for me to reason about the performance.
I would see some Clojure solutions taking a lot more time than my Python solutions, and I was clueless where does this slowness come from.

With the help of [r/Clojure community](https://old.reddit.com/r/Clojure/) on Reddit, who were very helpful in answering my questions and providing the feedback to my initial solutions, I discovered most of the things presented here.
There is a lot of other stuff I still don't understand, but these tips here were enough to find bottlenecks in my code and to make considerable improvements.

In the end, [my Clojure solutions](https://github.com/narimiran/AdventOfCode2022/tree/main/clojure) run in less than 4 seconds total, and even the slowest task takes less than 1 second.

Sorry Clojure for thinking you were the problem.
As it turns out:
It's not you, it's me.

