Big O is easy.  It takes something that can be hard (but doesn't have to be) and makes it less hard.

algorithm defintion - steps to accomplish a thing.

how do you know if an algorithm is fast? 
It depends.  We need tools to help us choose the right algo for our needs.

All algorithms are fast on small data sets.

How to measure speed:
Count the number of steps.  Doesn't matter what you pick as a step, but you have to be able give a constant highest bound for how long a step can take.  For instance, looking at an element, a comparison is a fine step.  Functional call, too.  1 second of processing would also work.  In the wild, you never define the step.

Factorial  

fib(n) = fib(n-1) + fib(n-2)
also
fib(2) = 1, fib(1) = 1


fib(target)
	f, fm1, i, temp = 1
	fm2 = 0
	while i < target
		temp = fm1 + fm2
		fm2 = fm1
		fm1 = f
		f = temp
		i =
 i + 1
	return f

common growth rates
1
n
2^
log2
examples of linear growth - saving money while working
examples of exponential growth - money reproducing, and counting in binary

Help understanding exponential growth:
Play this [video game](http://www.kongregate.com/games/Playsaurus/clicker-heroes) for one hour.  Every 5 minutes, write down your DPS and predict what your DPS will be in 5 minutes.


Four algorithms are really important in DBs
Linear search
Binary search
Sort
Hashing
hashing will come later

linear search is O(n)
binary search is O(log n)
sort is O(n log n)

