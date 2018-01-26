
import sys
import os

import argparse
import xml.etree.ElementTree as ET

def flipBoundingBox(x_min, y_min, x_max, y_max, img_width, img_height):
  '''
  Flips coordinates on the vertical axis.

  Assumes x_min, y_min, x_max, y_max starts from 0.
  Assumes all parameters are numbers.
  '''
  x_min_flip = (img_width-1) - x_min
  y_min_flip = y_min
  x_max_flip = (img_width-1) - x_max
  y_max_flip = y_max
  # After flip point_min is at upper right corner
  # and point_max lower left corner.
  # Extract new upper left and lower right corner.
  new_x_min = x_max_flip
  new_y_min = y_min_flip
  new_x_max = x_min_flip
  new_y_max = y_max_flip
  return new_x_min, new_y_min, new_x_max, new_y_max

def flipBoundingBox2(x_min, y_min, x_max, y_max, img_width, img_height):
  '''
  Flips coordinates on the vertical axis.

  Assumes x_min, y_min, x_max, y_max starts from 1.
  Assumes all parameters are numbers.

  PASCAL VOC dataset uses this coordinate system.
  '''
  x_min_flip = img_width - x_min + 1
  y_min_flip = y_min
  x_max_flip = img_width - x_max + 1
  y_max_flip = y_max
  # After flip point_min is at upper right corner
  # and point_max lower left corner.
  # Extract new upper left and lower right corner.
  new_x_min = x_max_flip
  new_y_min = y_min_flip
  new_x_max = x_min_flip
  new_y_max = y_max_flip
  return new_x_min, new_y_min, new_x_max, new_y_max

def flipBoundingBoxTest():
  x1,y1, x2,y2 = flipBoundingBox(10, 20, 40, 100, 256, 128)
  print(x1, y1, x2, y2)
  print("expect 215 20 245 100")


def flipBBInVocXml(file_name, out_file):
  #print("flipBBInVocXml", file_name, out_file)
  if os.path.isfile(file_name):

    tree = ET.parse(file_name)
    root = tree.getroot()

    # get image size
    size = root.find('size')
    if size == None:
      print(file_name)
      print("Size not found")
      return
    #print(size)
    width = size.find('width')
    if width == None:
      print(file_name)
      print("Width not found")
    img_width = int(width.text)
    #print(width)
    #print(width.text)
    height = size.find('height')
    if height == None:
      print(file_name)
      print("Height not found")
    img_height = int(height.text)
    #print(height)
    #print(height.text)
    #print(node.tag, node.attrib, node.text)

    # Processing bounding boxes
    '''
		<bndbox>
			<xmin>237</xmin>
			<ymin>209</ymin>
			<xmax>299</xmax>
			<ymax>268</ymax>
		</bndbox>
    '''
    for box in root.iter('bndbox'):
      #print(box)
      #for child in box:
      #  print(child.tag, child.text)
      #print('==guess')
      #print(box[0].text, box[1].text, box[2].text, box[3].text)
      x_min = int(box[0].text)
      y_min = int(box[1].text)
      x_max = int(box[2].text)
      y_max = int(box[3].text)
      #print('==guest END')
      #x1,y1, x2,y2 = flipBoundingBox(box[0].text, box[1].text, box[2].text, box[3].text, img_width, img_height)
      x1,y1, x2,y2 = flipBoundingBox2(x_min, y_min, x_max, y_max, img_width, img_height)
      #print(x1, y1, x2, y2)

      box[0].text = str(x1)
      box[1].text = str(y1)
      box[2].text = str(x2)
      box[3].text = str(y2)

    tree.write(out_file)

  else:
    print(file_name, "not found")


def stream(voc_index_file):
  with open(voc_index_file) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      yield line.rstrip()

      line = fp.readline()
      cnt += 1


def readComp4DetTest(file_name):
  with open(file_name) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      # processing
      array = line.rstrip().split(' ')
      if len(array) == 6:
        yield {'name' : array[0], 
              'bbox' : {
                'xmin' : float(array[1]),
                'ymin' : float(array[2]),
                'xmax' : float(array[3]),
                'ymax' : float(array[4])
              }}
      else:
        print("Unknown data:", line.rstrip())

      line = fp.readline()
      cnt += 1

def boundCoord(x, limit):
  # Convert floating point pixel coordinate to integer and bound by limit.
  # labelimg is 1..544 (start from 1)
  x1 = int(round(x))
  if x1 < 1: x1 = 1
  if x1 > limit: x1 = limit
  return x1

def boundImageCoord(x, y, image_width, image_height):
  x1 = boundCoord(x, image_width)
  y1 = boundCoord(y, image_height)
  return x1, y1


def readAllComp4DetTest(file_name, label, db, threshold = 0.24, image_width = 544, image_height = 544):
  '''
  db {'file name' : [
      {
        'name': str
       'bndbox': {'xmin': float, 'ymin': float, 'xmax': float, 'ymax': float}
      }
    ],
    [...],
    [...]
  }
  '''

  with open(file_name) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      # processing
      array = line.rstrip().split(' ')
      if len(array) == 6:
        thresh = float(array[1])
        if thresh > threshold:
          image_name = array[0]
          xmin = float(array[2])
          ymin = float(array[3])
          xmin, ymin = boundImageCoord(xmin, ymin, image_width, image_height)
          xmax = float(array[4])
          ymax = float(array[5])
          xmax, ymax = boundImageCoord(xmax, ymax, image_width, image_height)
          if image_name not in db:
            db[image_name] = []
        
          db[image_name].append({'name': label, 'bndbox': {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}})
      else:
        print("Unknown data:", line.rstrip())

      line = fp.readline()
      cnt += 1
  
  print(file_name, "has", cnt, "detections.")
  return db


def readComp4DetTest_TEST(file_name):
  gen = readComp4DetTest(file_name)
  for x in gen:
    print(x)

def setIndexPrefix(index, prefix):
  data = index.split('_')
  size = len(data)
  if size == 1:
    new_str = prefix + index[1:]
    return new_str
  elif size == 2:
    mov = data[0]
    number = data[1]
    new_number = prefix + number[1:]
    new_str = mov + "_" + new_number
    return new_str
  else:
    print("Unsupported VOC index: {}".format(index))
    return ""
  

def changePrefixInVocIndex(file_name, prefix):
  '''
  Generator
  Read each line in the file and do the following:
  Input: 7785_0002001
  Output: 7785_[prefix]002001
  '''

  gen = stream(file_name)
  for line in gen:
    data = line.split('_')
    mov = data[0]
    number = data[1]
    new_number = prefix + number[1:]
    new_str = mov + "_" + new_number
    yield line, new_str

  '''
  with open(file_name) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      data = line.rstrip().split('_')
      mov = data[0]
      number = data[1]
      new_number = prefix + number[1:]
      new_str = mov + "_" + new_number
      yield line.rstrip(), new_str

      line = fp.readline()
      cnt += 1
  '''

def addPrefixInVocIndex(file_name, offset):
  '''
  Generator
  Read each line in the file and do the following:
  Input: 7785_X002001
  Output: 7785_[X+offset]002001
  '''

  gen = stream(file_name)
  for line in gen:
    data = line.split('_')
    mov = data[0]
    number = data[1]
    base = int(number[:1])
    prefix = str(base+offset)
    new_number = prefix + number[1:]
    new_str = mov + "_" + new_number
    yield line, new_str

  '''
  with open(file_name) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      data = line.rstrip().split('_')
      mov = data[0]
      number = data[1]
      base = int(number[:1])
      prefix = str(base+offset)
      new_number = prefix + number[1:]
      new_str = mov + "_" + new_number
      yield line.rstrip(), new_str

      line = fp.readline()
      cnt += 1
  '''

def gen_list_expo(file_name):
  gen = stream(args.file)
  for in_file in gen:
    print("{}".format(in_file))
  gen = changePrefixInVocIndex(args.file, "1")
  for in_file, out_file in gen:
    print("{}".format(out_file))
  gen = changePrefixInVocIndex(args.file, "2")
  for in_file, out_file in gen:
    print("{}".format(out_file))

def gen_anno_expo(file_name):
  print("#!/bin/sh")
  gen = changePrefixInVocIndex(args.file, "1")
  for in_file, out_file in gen:
    print("\cp {}.xml {}.xml".format(in_file, out_file))
  gen = changePrefixInVocIndex(args.file, "2")
  for in_file, out_file in gen:
    print("\cp {}.xml {}.xml".format(in_file, out_file))

def do_expo(file_name):
  print("#!/bin/sh")
  gen = changePrefixInVocIndex(args.file, "1")
  for in_file, out_file in gen:
    print("exposure -a -50 {}.jpg {}.jpg".format(in_file, out_file))
  gen = changePrefixInVocIndex(args.file, "2")
  for in_file, out_file in gen:
    print("exposure -a 50 {}.jpg {}.jpg".format(in_file, out_file))

def add_jpg_ext(file_name):
  gen = stream(file_name)
  for in_file in gen:
    print("{}.jpg".format(in_file))

def cp(file_name):
  print("#!/bin/sh")
  gen = stream(file_name)
  for in_file in gen:
    #print("\cp ~/data/VOC/VOCdevkit/VOC2018/JPEGImages/{}.jpg .".format(in_file))
    #print("\cp {}.jpg mov-7785-1080x1080/".format(in_file))
    print("\cp {}.jpg ~/data/VOC/VOCdevkit/VOC2000/JPEGImages/".format(in_file))
    

def flop(file_name):
  print("#!/bin/sh")
  gen = addPrefixInVocIndex(file_name, 3)
  for in_file, out_file in gen:
    print("convert {}.jpg -flop {}.jpg".format(in_file, out_file))

def flop_anno(file_name):
  gen = addPrefixInVocIndex(file_name, 3)
  for in_file, out_file in gen:
    flipBBInVocXml(in_file+".xml", out_file+".xml")

def ln(file_name):
  print("#!/bin/sh")
  gen = stream(file_name)
  for in_file in gen:
    print("ln -s ../{}.jpg {}.jpg".format(in_file, in_file))


def createAnnoXMLObj(name, image_ext, image_width = 544, image_height = 544):
  '''
  name: e.g. IMG_6148
  image_ext: extension of image file, .e.g, jpg
  '''
  root = ET.Element('annotation')
  ET.SubElement(root, 'folder').text = 'JPEGImages'
  ET.SubElement(root, 'filename').text = name + image_ext
  ET.SubElement(root, 'path').text = name
  source = ET.SubElement(root, 'source')
  ET.SubElement(source, 'database').text = 'Unknown'
  size = ET.SubElement(root, 'size')
  ET.SubElement(size, 'width').text = str(image_width)
  ET.SubElement(size, 'height').text = str(image_height)
  ET.SubElement(size, 'depth').text = '3'
  ET.SubElement(root, 'segmented').text = '0'
  
  '''
  # Write to file
  tree = ET.ElementTree(root)
  filename = name + '.xml'
  with open(filename, 'w', encoding='utf-8') as file:
      tree.write(file, encoding='unicode')
  '''
  return root

def addBBoxToXMLObj(anno_obj, label, bbox):
  '''
  obj: ElementTree Element
  bbox: Bounding box in this format:
    'bbox' : {
                'xmin' : int
                'ymin' : int
                'xmax' : int
                'ymax' : int
              }

  Return: obj modified
  '''
  obj = ET.SubElement(anno_obj, 'object')
  ET.SubElement(obj, 'name').text = label
  ET.SubElement(obj, 'pose').text = 'Unspecified'
  ET.SubElement(obj, 'truncated').text = '0'
  ET.SubElement(obj, 'difficult').text = '0'
  bndbox = ET.SubElement(obj, 'bndbox')
  ET.SubElement(bndbox, 'xmin').text = str(bbox['xmin'])
  ET.SubElement(bndbox, 'ymin').text = str(bbox['ymin'])
  ET.SubElement(bndbox, 'xmax').text = str(bbox['xmax'])
  ET.SubElement(bndbox, 'ymax').text = str(bbox['ymax'])
  


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file")
  args = parser.parse_args()

  #flipBBInVocXml(args.file, "output.xml")

  #gen = changePrefixInVocIndex(args.file, "X")
  #gen = addPrefixInVocIndex(args.file, 3)
  #gen = stream(args.file)
  #for item in gen:
  #  print(item)

  '''
  for in_file, out_file in gen:
    print(in_file, out_file)
    flipBBInVocXml(in_file + ".xml", out_file + ".xml")
  '''

  #cp(args.file)
  #ln(args.file)

  #do_expo(args.file)
  #gen_anno_expo(args.file)
  #gen_list_expo(args.file)

  #flop_anno(args.file)
  #flop(args.file)
  #gen_tar_list(args.file)
  #add_jpg_ext(args.file)

  ## results file to XML
  '''
  #readComp4DetTest_TEST(args.file)
  anno = createAnnoXMLObj(args.file, '.jpg', 544, 544)
  #xmlstr = ET.dump(anno)
  xmlstr = ET.tostring(anno)
  print(xmlstr)
  '''
  #anno = createAnnoXMLObj(args.file, '.jpg', 544, 544)
  #with open('output.xml', 'w') as f:
  #  tree.write(f)


  '''
  import lxml.etree as etree
  x = etree.fromstring(xmlstr)
  print(etree.tostring(x, pretty_print=True))
  '''