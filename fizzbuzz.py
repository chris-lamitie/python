#!/bin/python3
#
# Complete the 'fizzBuzz' function below.
# Problem we are solving:
# Given a number n, for each integer i in the range 1 to n inclusive,
# print one value per line as follows:
#   if i is a multiple of both 3 and 5, print FizzBuzz
#   if i is a multiple of 3 (but not 5), print Fizz
#   if i is a multiple of 5 (but not 3), print Buzz
#   if i is not a multiple of 3 or 5, print the value of i
# The function accepts INTEGER n as parameter.
#

import math
import os
import random
import re
import sys

def fizzBuzz(n):
    # Write your code here
    i = 1
    while i <= n:
        #print ("n is",n)
        #print ("i is",i)
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0 and not i % 5 == 0:
            print("Fizz")
        elif i % 5 == 0 and not i % 3 == 0:
            print("Buzz")
        else:
            print(i)
        i += 1

print ("fizzBuzz for 15")
fizzBuzz(15)

print ("fizzBuzz for 21")
fizzBuzz(21)

print ("fizzBuzz for 32")
fizzBuzz(32)

print ("fizzBuzz for 40")
fizzBuzz(40)

#if __name__ == '__main__':
#    n = int(input().strip())
#
#    fizzBuzz(n)
