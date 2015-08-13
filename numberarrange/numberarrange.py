#! /usr/bin/python

import sys


# Notations:
# The four digits will be represented as abcd in this description.

# 0. Parse the digits from the string.
# We shall represent the four digits as a tuple (a, b, c, d)


def parse_digits(digitstring):
    return tuple(map(int, list(digitstring)))


# Sub Problems:

# 1. Check that at least one digit is different from the other three.
# My method is to find the result of a-b+c-d. If this result if 0, then the
# input is invalid else it is valid. This computation is useful because most
# languages take any number except 0 as true and 0 as false so we can shave off
# one or two lines of code in code golf :)


def at_least_one_different(a, b, c, d):
    return a - b + c - d


# 2.1 My approach to finding the largest and smallest numbers formable by the
# four digits is to precompute an array of size 10 that contains the number of
# digits of that index as the value.
# This runs in constant time. It takes four loops to create the precomputed
# array.
# The digits "1333" will create [0, 1, 0, 3, 0, 0, 0, 0, 0, 0].


def precompute_array(tup):
    # Create an array of size 10 initialized with zeros. This will represent the
    # number of digits between 0-9.
    pa = [0]*10
    for i in tup:
        pa[i] += 1
    return pa


# 2.2 Create the largest number.
# We do this by walking down from index 9-0 of the precomputed array,
# concatenating the index by the number of times in the value.


def largest_number(pa):
    largest = ""
    for i in range(9, -1, -1):
        largest += str(i)*pa[i]
    return largest


# 2.3 Create the smallest number.
# We do this by doing the opposite of 2.2. We walk from 0-9. We can actually
# refactor this code by passing the generator dynamically but this looks
# cleaner.


def smallest_number(pa):
    smallest = ""
    for i in range(10):
        smallest += str(i)*pa[i]
    return smallest


def main():
    digits = sys.argv[1]
    pd = parse_digits(digits)
    if at_least_one_different(*pd):
        pa = precompute_array(pd)
        print("Largest:  %s" % largest_number(pa))
        print("Smallest: %s" % smallest_number(pa))
    else:
        print("Invalid input")

if __name__ == "__main__":
    main()
