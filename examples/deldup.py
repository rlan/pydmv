#!/usr/bin/python

import os
import sys
import argparse

#Auto-import parent module
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import voc
#from pydmv import voc

parser = argparse.ArgumentParser(description="Print VOC index file without duplicates")
parser.add_argument("file", help="Input index file")
args = parser.parse_args()
in_file = args.file

my_bag = set()
for index in voc.stream(in_file):
  if index not in my_bag:
    print(index)
    my_bag.add(index)
