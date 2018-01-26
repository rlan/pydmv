#!/usr/bin/python

import os
import sys
import argparse

#Auto-import parent module
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import util
#from pydmv import util

parser = argparse.ArgumentParser(description="Show all factors of an integer")
parser.add_argument("value", help="An integer")
args = parser.parse_args()
value = int(args.value)

print("Factors of {} are {}".format(value, util.factors(value)))
