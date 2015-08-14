#! /usr/bin/python

import sys


# Notations:
# The four digits will be represented as abcd in this description.

# 0. Parse the digits from the string.
# We shall represent the four digits as a tuple (a, b, c, d)


def parse_digits(digitstring):
    return tuple(map(int, list(digitstring)))


# Sub Problems:


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

# 2.1 Refactored to find either the largest number or the smallest number by
# passing in a generator. Includes a check to test if the number is valid or
# not.


def arrange_number(pa, gen):
    arranged = ""
    for i in gen:
        if pa[i] == 4:
            print("Invalid input")
            sys.exit()
        arranged += str(i)*pa[i]
    return arranged

# 2.2 Create the largest number using a wrapper that calls arrange_number.
# We do this by walking down from index 9-0 of the precomputed array,
# concatenating the index by the number of times in the value.


def largest_number(pa):
    return arrange_number(pa, range(9, -1, -1))


# 2.3 Create the smallest number using a wrapper that calls arrange_number.
# We do this by doing the opposite of 2.2. We walk from 0-9. We can actually
# refactor this code by passing the generator dynamically but this looks
# cleaner.


def smallest_number(pa):
    return arrange_number(pa, range(10))


def main():
    digits = sys.argv[1]
    pd = parse_digits(digits)
    pa = precompute_array(pd)
    print("Largest:  %s" % largest_number(pa))
    print("Smallest: %s" % smallest_number(pa))

if __name__ == "__main__":
    main()
