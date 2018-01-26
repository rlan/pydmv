#!/usr/bin/python

'''
Flop (horizontal flip) objects in VOC xml files and write to new xml files.

[path]/[file].xml will be read and output file will be written at ./[file].xml
'''

import os
import sys
import argparse
import xml.etree.ElementTree as ET


#Auto-import parent module
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import voc


parser = argparse.ArgumentParser(description="Flop (horizontal flip) objects in VOC xml files and write to new xml files.")
parser.add_argument("file", help="A VOC index file")
parser.add_argument("path", help="Root path to xml")
args = parser.parse_args()
in_file = args.file
path = args.path

'''
in_file = '~/data/VOC/VOCdevkit/VOC2018/Annotations/round778184_test.txt'
path = '~/data/VOC/VOCdevkit/VOC2018/Annotations/'
'''


for index in voc.stream(in_file):
  index = index.rstrip()
  full_file = path + index + ".xml"
  out_file = index + ".xml"
  print("Generating {}".format(out_file))
  voc.flipBBInVocXml(full_file, out_file)
