#!/usr/bin/python

'''
Upscale objects in VOC xml files as if image was upscaled by 2x

[path]/[file].xml will be read and output file will be written at ./[file].xml
'''

import os
import sys
import argparse

import xml.etree.ElementTree as ET


#Auto-import parent module
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import voc as VU


parser = argparse.ArgumentParser(description='Upscale objects in VOC xml files as if image was upscaled by 2x')
parser.add_argument("file", help="A VOC index file")
parser.add_argument("path", help="Root path to xml")
args = parser.parse_args()
in_file = args.file
path = args.path

'''
in_file = '~/data/VOC/VOCdevkit/VOC2018/Annotations/round778184_test.txt'
path = '~/data/VOC/VOCdevkit/VOC2018/Annotations/'
'''

def twoX(val):
  if val == 0:
    return 1
  else:
    return 2*val


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
    
    for box in root.iter('bndbox'):
      #print(x)

      x_min = int(box.find('xmin').text)
      y_min = int(box.find('ymin').text)
      x_max = int(box.find('xmax').text)
      y_max = int(box.find('ymax').text)

      x1 = twoX(x_min)
      y1 = twoX(y_min)
      x2 = twoX(x_max)
      y2 = twoX(y_max)

      box.find('xmin').text = str(x1)
      box.find('ymin').text = str(y1)
      box.find('xmax').text = str(x2)
      box.find('ymax').text = str(y2)


    # Write to file
    #tree = ET.ElementTree(root)
    #ET.dump(tree)
    
    out_file = index + ".xml"
    #print(position)
    print("Generating {}".format(out_file))
    with open(out_file, 'w', encoding='utf-8') as f:
      tree.write(f, encoding='unicode')
  
  else:
    print("XML file not found: {}".format(new_line))
