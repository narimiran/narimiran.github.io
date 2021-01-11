---
layout: post
title: Parsing inputs in Nim
date: 2021-01-11
---

One of the challenges during [2020 Advent of Code](https://adventofcode.com/2020/) was how to easily and conveniently parse your inputs and convert them into some usable data type for later use.
In this post I'll show several different methods you can use in Nim for parsing:

1. Parse as you go
2. Just use `split`
3. "I know, I'll use regex!"
4. `scanf` macro
5. `npeg` library



## Parse as you go

This example is from [Day 5](https://adventofcode.com/2020/day/5), where the input looks like this:
```
BFFFFBBRRL
FBBBBBBRRL
BBBFFBBRRR
BFFFFFFLRL
FBFFBFBRRR
(...)
```

When the task is such that you'll go through your input only once and it will be simple line-by-line traversal, there is no need to convert your multi-line input to a sequence of strings (or `seq[seq[char]]`) and then iterate over that sequence(s).
There is `lines` iterator which accepts a filename and yields lines of that file.

Instead of:
```nim
import strutils

let filename = "path/to/input.txt"
let content = readFile(filename).splitLines()

for line in content:
  doSomething(line)
```

You can do that directly (and without the need to `import strutils`):
```nim
let filename = "path/to/input.txt"

for line in filename.lines:
  doSomething(line)
```



## Just use `split`

The input for [Day 4](https://adventofcode.com/2020/day/4) was the first irregular input where you need to treat everything until an empty line as one group (which could be all in one row or in two or more multiple rows):

```
cid:242 iyr:2011 pid:953198122 eyr:2029 ecl:blu hcl:#888785

eyr:2033
hgt:177cm pid:173cm
ecl:utc byr:2029 hcl:#efcc98 iyr:2023

(...)
```

I know people who had already struggled with splitting the input into separate groups, not realizing you can use a simple `split("\n\n")`.
(They have split input at each line, and then wrote some logic to concatenate back stuff that should be in the same group.)
Once you have a sequence of groups, now you need to separate each field of the group.

The fields are delimited by a whitespace or a newline.
Once again I've seen people having trouble with this, doing `replace('\n', ' ')` so they have everything separated by whitespace before doing a `split(' ')`.
No need for that!
Using `splitWhitespace` you can immediately split on any whitespace, including a newline or a tab.

```nim
import strutils

let filename = "path/to/input.txt"
for group in readFile(filename).split("\n\n"):
  for field in group.splitWhitespace:
    doSomething(field)
```

Even though the input looked irregular and hard to parse at the first sight, it can be easily parsed just by using `split` and `splitWhitespace`.
(For splitting a field, you can also once again use `split(':')` or notice that each key is exactly three characters long and then take a slice: `let key = field[0..2]`.)
There is no need to bring "big guns" if the input is in fact quite simple.

Note: Don't be fooled into using this method if you're parsing a CSV file!
Use the dedicated `parsecsv` for that.



## "I know, I'll use regex!"

You might recognize the title of this section as a part of a famous quote:

> Some people, when confronted with a problem, think "I know, I'll use regular expressions."  
> Now they have two problems.

When I'm writing Python, I don't mind doing `import re` and using regular expressions in the situations that ask for some regex.
I would say I'm quite familiar with regex and I have no problem writing non-trivial ones.

But when I write Nim, even though Nim has multiple regex libraries (some as a part of standard library, others as Nimble packages), I (almost) never use regular expressions.
The reason for that is that when I discovered `scanf`, there was no turning back.
(The other reason is: when I have too many options too choose from, I spend more time analyzing which one is superior to others than using it :))



## `scanf` macro

A part of [Day 16](https://adventofcode.com/2020/day/16)'s input looked like this:
```
departure date: 28-109 or 135-950
departure time: 38-622 or 631-958
arrival location: 35-61 or 69-957
arrival station: 36-216 or 241-951
class: 31-439 or 445-957
duration: 35-925 or 939-965
price: 41-473 or 494-952
(...)
```

You needed to:
- extract the field name: everything before the colon (`:`); sometimes one word, sometimes two words
- parse two integer ranges between `or`

Splitting on `": "`, and then on `" or "`, and then on `"-"` was out of the question: it felt too convoluted and would be hard to read, and I knew I had a better tool for the job.
Enter [strscans.scanf](https://nim-lang.github.io/Nim/strscans.html)!

`scanf` macro takes an input string, a pattern we wish to match, and the variables we will assign to our pattern matches (the variables must be declared beforehand).
The macro returns a Boolean, depending if the matching was successful or not.

This means we can parse our input with the following code:
```nim
import strscans

var min1, max1, min2, max2: int
var field: string

for line in input.lines:
  if line.scanf("$+: $i-$i or $i-$i", field, min1, max1, min2, max2):
    result[field] = {min1..max1, min2..max2}
```

As you can see, there's no need for `parseInt`: the numbers matched with `$i` are already converted to integers.
(`result` is a `Table`, declared outside of this example.)

Yes, you could have done the same with regex and some groups and matches, but I find `scanf` both easier to write and easier to read and immediately understand what is going on.

You can also use `scanf` when the input contains more than one pattern, like it was the case for [Day 14](https://adventofcode.com/2020/day/14):

```
mask = 11110100010101111011001X0100XX00100X
mem[17610] = 1035852
mem[55284] = 229776690
mem[16166] = 12685380
mask = 0X1X0X010101011X10X101000X0001110100
mem[968] = 15992
mem[32758] = 7076
(...)
```

Here a line can contain either a `mask` (a binary-looking string, containing 1's, 0's and X's) or an instruction where to put some values in `mem`.

```nim
import tables, strscans

var mem: Table[int, int]
var k, v: int
var mask: string

for line in path.lines:
  if line.scanf("mask = $+", mask):
    doStuff(mask)
  elif line.scanf("mem[$i] = $i", k, v):
    mem[k] = v
```

Easy and elegant.



## `npeg` library

I've seen some people use [npeg](https://github.com/zevv/npeg), a pattern matching library especially suited for PEGs ([parsing expression grammar](https://en.wikipedia.org/wiki/Parsing_expression_grammar)), from the first day of Advent of Code.
I felt no need to learn a completely new (to me) tool just to do stuff that I could achieve with the stuff mentioned in the previous sections, which I was familiar with.

That was the case until [Day 19](https://adventofcode.com/2020/day/19) came.
Its input looked like this:
```
72: "b"
45: 46 52 | 9 72
85: 9 52 | 9 72
67: 52 48
25: 19 72 | 103 52
8: 42
32: 90 52 | 78 72
50: 113 113
(...)

bbabbaabaabaaaababbbbabaabbaabab
aaabbbabaabbbbbbbbabaaba
(...)
```

It is a series of rules which the messages need to satisfy, an empty line, a list of messages.
There are three different types of rules:
- `72: "b"` -- rule 72 is just a single character `b`
- `67: 52 48` -- rule 67 is: rule 52 followed by rule 48
- `45: 46 52 | 9 72` -- rule 45 is *either* rule 46 followed by rule 52 *or* rule 9 followed by rule 72

Within those rules, there is rule 0, which is the starting rule, and our task is to check if the messages satisfy that rule.
This task looked like a perfect opportunity to learn `npeg`!



### Defining a grammar

If you want a quick introduction to `npeg`, I can recommend [npeg's readme](https://github.com/zevv/npeg/blob/master/README.md) which contains several examples and lots of explanations of every part of npeg's syntax.

We start top-down, describing what our input looks like:
it is a series of rules (`+rule`), followed by an empty line (`'\n'`), and then a list of messages (`+message`).
Each rule starts by a multi-digit number (`+Digit`), followed by `": "`, and then one of three different types of a rule described above (I'm calling them `letter`, `list`, and `choice`, respectively), followed by a newline.
A message is just a series of characters (`+Alpha`), followed by a newline.
Putting all this together, we have:

```nim
input <- +rule * '\n' * +message
rule <- +Digit * ": " * (letter | choice | list) * '\n'
message <- +Alpha * '\n'
```

Now it is time to define each of those sub-rules:
- `letter` is just a single character inside of a pair of `"`
- `list` is a series of one or more numbers
- `choice` are two `list` separated by `" | "`

```nim
letter <- '"' * Alpha * '"'
list <- +Digit * *(' ' * +Digit)
choice <- list * " | " * list
```

That is our complete grammar!
And now comes the interesting part: capturing the stuff we need.



### Capturing the matches

`npeg` allows us to catch any part of a PEG with a `>` prefix, e.g. `>list` or `>+Digit`, and if we end a grammar rule with a colon (`:`), we can then write a regular Nim code block where we can manipulate the captures.


First we'll define the types we need.
The `Rule` type is a [variant object](https://nim-lang.github.io/Nim/manual.html#types-object-variants), with different variants depending on the rule kind as described above.
Other types should be self-explanatory.

```nim
type
  RuleKind = enum
    rkLetter, rkList, rkChoice
  Rule = object
    case kind: RuleKind
    of rkLetter:
      letter: char
    of rkList:
      rules: seq[int]
    of rkChoice:
      left: seq[int]
      right: seq[int]
  Rules = Table[int, Rule]
  Messages = seq[string]

var rules: Rules
var currentRule: Rule
var messages: Messages
```

Let's start simple.
We'll slightly modify our grammar rule for `message` from above:

```nim
message <- >+Alpha * '\n':
  messages.add $1
```

All it took was adding a `>` to capture a series of letters and then adding that capture to the `messages` sequence.

Capturing the rules is slightly more convoluted.
Every time we encounter a rule kind, we capture it in `currentRule` variable.

```nim
letter <- '"' * >Alpha * '"':
  currentRule = Rule(kind: rkLetter, letter: ($1)[0])

list <- +Digit * *(' ' * +Digit):
  currentRule = Rule(kind: rkList, rules: ($0).split.map(parseInt))

choice <- >list * " | " * >list:
  currentRule = Rule(kind: rkChoice,
                     left: ($1).split.map(parseInt),
                     right: ($2).split.map(parseInt))
```

After the whole rule is captured, we add the current rule to the table of all rules:

```nim
rule <- >+Digit * ": " * (letter | choice | list) * '\n':
  rules[parseInt($1)] = currentRule
```


### All together now

Putting the whole parser together, we have this:

```nim
let parser = peg input:
  input <- +rule * '\n' * +message
  rule <- >+Digit * ": " * (letter | choice | list) * '\n':
    rules[parseInt($1)] = currentRule
  letter <- '"' * >Alpha * '"':
    currentRule = Rule(kind: rkLetter, letter: ($1)[0])
  choice <- >list * " | " * >list:
    currentRule = Rule(kind: rkChoice,
                       left: ($1).split.map(parseInt),
                       right: ($2).split.map(parseInt))
  list <- +Digit * *(' ' * +Digit):
    currentRule = Rule(kind: rkList, rules: ($0).split.map(parseInt))
  message <- >+Alpha * '\n':
    messages.add $1

discard parser.matchFile(path)
```

A bit more convoluted than the examples in the previous sections, but the main reason for that is the input was more complicated to start with.
Even so, I think the code clearly (once you understand `npeg` syntax) shows the grammar of our input and what we're doing with captures.

One nice extra: `npeg` allows us to easily create [railroad diagrams](https://en.wikipedia.org/wiki/Syntax_diagram) if we compile our program with `-d:npegGraph`.
For our grammar defined above it looks like this:

```
input o─┬─[rule]─┬»─'\n'─»┬─[message]─┬─o
        ╰───«────╯        ╰─────«─────╯

        ╭╶╶╶╶╶╶╶╶╶╶╶╮
rule o───┬─[Digit]─┬──»─": "─»─┬─[letter]─┬─»─'\n'──o
        ┆╰────«────╯┆          ├─[choice]─┤
        ╰╶╶╶╶╶╶╶╶╶╶╶╯          ╰─[list]───╯

                ╭╶╶╶╶╶╶╶╶╶╮
letter o──'"'─»───[Alpha]───»─'"'──o
                ╰╶╶╶╶╶╶╶╶╶╯

          ╭╶╶╶╶╶╶╶╶╮           ╭╶╶╶╶╶╶╶╶╮
choice o────[list]───»─" | "─»───[list]────o
          ╰╶╶╶╶╶╶╶╶╯           ╰╶╶╶╶╶╶╶╶╯

                   ╭─────────»─────────╮
list o─┬─[Digit]─┬»┴┬─' '─»┬─[Digit]─┬┬┴─o
       ╰────«────╯  │      ╰────«────╯│
                    ╰────────«────────╯

           ╭╶╶╶╶╶╶╶╶╶╶╶╮
message o───┬─[Alpha]─┬──»─'\n'──o
           ┆╰────«────╯┆
           ╰╶╶╶╶╶╶╶╶╶╶╶╯
```

This is not just a pretty graph, it can also be used for better understanding a complex grammar or debugging: you can notice optionals (`»` line above), repeats (`«` line below), captures (inside of a dotted-line rectangular), etc. 



## Conclusion

Nim offers us several different ways to parse a file, ranging from very simple to writing our own grammar parser.
What to choose depends on the input, as well as on personal preferences (any of the methods shown here could be used in all of the examples shown).

Hopefully, you learnt something new that will help you write parsers more easily in the future.

&nbsp;

> All the examples are based on [my Advent of Code solutions](https://github.com/narimiran/AdventOfCode2020).
