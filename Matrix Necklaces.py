'''
Disorderly Escape
=================

Oh no! You've managed to free the bunny workers and escape Commander Lambdas exploding space station, but Lambda's
team of elite starfighters has flanked your ship. If you dont jump to hyperspace, and fast, youll be shot out of the sky!

Problem is, to avoid detection by galactic law enforcement, Commander Lambda planted the space station in the middle
of a quasar quantum flux field. In order to make the jump to hyperspace, you need to know the configuration of celestial
bodies in the quadrant you plan to jump through. In order to do *that*, you need to figure out how many configurations 
each quadrant could possibly have, so that you can pick the optimal quadrant through which youll make your jump. 

There's something important to note about quasar quantum flux fields' configurations: when drawn on a star grid,
configurations are considered equivalent by grouping rather than by order. That is, for a given set of configurations,
if you exchange the position of any two columns or any two rows some number of times, youll find that all of those
configurations are equivalent in that way -- in grouping, rather than order.

Write a function solution(w, h, s) that takes 3 integers and returns the number of unique, non-equivalent configurations
that can be found on a star grid w blocks wide and h blocks tall where each celestial body has s possible states.
Equivalency is defined as above: any two star grids with each celestial body in the same state where the actual order
of the rows and columns do not matter (and can thus be freely swapped around). Star grid standardization means that the width
and height of the grid will always be between 1 and 12, inclusive. And while there are a variety of celestial bodies in each
grid, the number of states of those bodies is between 2 and 20, inclusive. The solution can be over 20 digits long, so return
it as a decimal string. The intermediate values can also be large, so you will likely need to use at least 64-bit integers.

For example, consider w=2, h=2, s=2. We have a 2x2 grid where each celestial body is either in state 0 (for instance, silent)
or state 1 (for instance, noisy).  We can examine which grids are equivalent by swapping rows and columns.

00
00

In the above configuration, all celestial bodies are "silent" - that is, they have a state of 0 - so any swap of row or column
would keep it in the same state.

00 00 01 10
01 10 00 00

1 celestial body is emitting noise - that is, has a state of 1 - so swapping rows and columns can put it in any of the 4 positions.
All four of the above configurations are equivalent.

00 11
11 00

2 celestial bodies are emitting noise side-by-side.  Swapping columns leaves them unchanged, and swapping rows simply moves them
between the top and bottom.  In both, the *groupings* are the same: one row with two bodies in state 0, one row with two bodies
in state 1, and two columns with one of each state.

01 10
01 10

2 noisy celestial bodies adjacent vertically. This is symmetric to the side-by-side case, but it is different because there's no
way to transpose the grid.

01 10
10 01

2 noisy celestial bodies diagonally.  Both have 2 rows and 2 columns that have one of each state, so they are equivalent to each other.

01 10 11 11
11 11 01 10

3 noisy celestial bodies, similar to the case where only one of four is noisy.

11
11

4 noisy celestial bodies.

There are 7 distinct, non-equivalent grids in total, so solution(2, 2, 2) would return 7.

-- Python cases -- 
Input:
solution.solution(2, 3, 4)
Output:
    430

Input:
solution.solution(2, 2, 2)
Output:
    7
'''

import operator as op
from functools import reduce
from math import factorial as fact
from math import gcd
from fractions import Fraction
from collections import Counter
from time import time


def solution(w, h, s):
    cycleW = cycles(w)
    cycleH = cycles(h)

    #Generate the cycle index of the matrix by combining all possible combinations of the cycles for the width and the height
    cycleIndex = []
    for termW in cycleW:
        for termH in cycleH:
            cycleIndex.append(combine(termW, termH))
    
    #Plug in the number of states into the cycle index polynomial to get the final answer
    final = 0
    for term in cycleIndex:
        final += term[0] * s ** sum(term[1].values())
    return str(final)


#Returns the cycle index polynomial as a list of frequency, partition tuples

#e.g. [ (1/2, {2: 1}), (1/2, {1: 2}) ] for n = 2
#e.g. [ (1/4, {4: 1}), (1/3, {3: 1, 1: 1}), (1/8, {2: 2}), (1/4, {2: 1, 1: 2}), (1/24, {1: 4}) ] for n = 4

#Note that frequencies add up to n!
def cycles(n):
    cycle = []
    partitions = partition(n)
    for part in partitions:
        freq = Fraction(1)
        left = n
        for num, occurs in part.items():
            for k in range(occurs):
                freq *= choose(left, num) * fact(num - 1)
                left -= num
            freq /= fact(occurs)
        cycle.append((freq / fact(n), part))
    return cycle


#Combines two cycle index monomials
def combine(a, b):
    coeff = a[0] * b[0]
    new = {}
    for subA, supA in a[1].items():
        for subB, supB in b[1].items():
            sup = subA * supA * subB * supB // lcm(subA, subB)
            sub = lcm(subA, subB)
            new[sub] = new.get(sub, 0) + sup
    return (coeff, new)


#Returns a list of every partition that adds up to n

#e.g. [ {2: 1}, {1: 2} ] for n = 2
#e.g. [ {4: 1}, {3: 1, 1: 1}, {2: 2}, {2: 1, 1: 2}, {1: 4} ] for n = 4
def partition(n):
    parts = []
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            parts.append( dict(Counter(a[:k + 2])) )
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        parts.append( dict(Counter(a[:k + 1])) )
    return parts


#nCr implementation
def choose(n, r):
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer // denom


#lcm implementation
def lcm(x, y):
    return x * y // gcd(x, y)


t = time()
print(solution(3, 3, 2))
print(time() - t)