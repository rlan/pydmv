'''
https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
'''

import os
import sys
import argparse


def factors(n):    
    l1, l2 = [], []
    for i in range(1, int(n ** 0.5) + 1):
        q,r = n//i, n%i     # Alter: divmod() fn can be used.
        if r == 0:
            l1.append(i) 
            l2.append(q)    # q's obtained are decreasing.
    if l1[-1] == l2[-1]:    # To avoid duplication of the possible factor sqrt(n)
        l1.pop()
    l2.reverse()
    return l1 + l2


if __name__ == "__main__":
  
    parser = argparse.ArgumentParser()
    parser.add_argument("value", help="Integer to factor")
    args = parser.parse_args()
    value = int(args.value)

    print("Factors of {} are {}".format(value, factors(value)))
