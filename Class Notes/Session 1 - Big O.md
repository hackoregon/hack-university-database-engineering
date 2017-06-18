# Install and Big O

## start by [installing vagrant](../install.md)

## Big O

Big O is easy.  It takes something that can be hard (but doesn't have to be) and makes it less hard.

algorithm: steps to accomplish a thing.

### how do you know if an algorithm is fast?
It depends.  We need tools to help us choose the right algorithm for our needs.

All algorithms are fast on small data sets.

### How to measure speed?
Count the number of steps.  Doesn't matter what you pick as a step, but you have to be able give a constant highest bound for how long a step can take.  For instance, looking at an element, a comparison is a fine step.  Functional calls can be, too.  1 second of processing would also work.  When you use Big O in the real world, you never define your step.

### Example  

#### Simple Recursive Factorial
```
fib(n) = fib(n-1) + fib(n-2)
also
fib(2) = 1, fib(1) = 1
```
Function calls make good steps in this example.

#### Simple Iterative Factorial
```
fib(target)
	current, i, temp = 1
	last = 0

while i < target
		temp = current + last
		last = current
		current = temp
		i = i + 1
	return current
```
Iterations of the loop make good steps for this example.

How many steps are done by each algorithm for fib(2)?  fib(10)?  fib(1000)?

|target|fib(target)|iterative|recursive|
|:---:|:---:|:---:|:---:|
|1|1|1|1|
|2|1|1|1|
|3|2|2|3|
|4|3|3|5|
|5|5|4|9|
|10|55|9|109|
|100|354,224,848,179,262,000,000|99|33,282,055,501,241,100,000,000|


Common Growth Rates:

1. 1
1. n
1. 2^n
1. log(n)


Putting money under your mattress is a good examples of linear growth.
Saving money at the bank is a good example of exponential growth.

#### Help understanding exponential growth:
Play this [video game](http://www.kongregate.com/games/Playsaurus/clicker-heroes) for one hour.  Every 5 minutes, write down your DPS and predict what your DPS will be in 5 minutes.


## Algorithms for Databases.
Four algorithms are really important in DBs:

1. Linear search
1. Binary search
1. Sort
1. Hashing (this will come later)

Linear search is O(n).

Binary search is O(log n).

Sort is O(n log n).
