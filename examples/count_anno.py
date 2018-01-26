#!/usr/bin/python

'''
Count number of annotations in each XML given a VOC index file.

'''

import os
import sys
import argparse

import xml.etree.ElementTree as ET


#Auto-import parent module
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import voc as VU


parser = argparse.ArgumentParser(description="Count number of annotations in each XML given a VOC index file.")
parser.add_argument("file", help="A VOC index file")
parser.add_argument("path", help="Root path to xml")
args = parser.parse_args()
in_file = args.file
path = args.path

'''
in_file = '~/data/VOC/VOCdevkit/VOC2018/Annotations/round778184_test.txt'
path = '~/data/VOC/VOCdevkit/VOC2018/Annotations/'
'''


for index in VU.stream(in_file):
  index = index.rstrip()
  new_line = path + index + ".xml"

  if os.path.isfile(new_line):

    tree = ET.parse(new_line)
    root = tree.getroot()

    size = root.find('size')
    if size == None:
      print("Size not found")
      sys.exit()
    #print(size)
    width = size.find('width')
    if width == None:
      print("Width not found")
      sys.exit()
    img_width = int(width.text) * 2
    width.text = str(img_width)
    #print(width)
    #print(width.text)
    height = size.find('height')
    if height == None:
      print("Height not found")
      sys.exit()
    img_height = int(height.text) * 2
    height.text = str(img_height)
    #print(height)
    #print(height.text)
    
    count = 0
    for box in root.iter('bndbox'):
      #print(x)
      count = count + 1

    if count == 0:
      print("{} {} !!!!!".format(index, count))
    else:
      print("{} {}".format(index, count))

  
  else:
    print("XML file not found: {}".format(new_line))
