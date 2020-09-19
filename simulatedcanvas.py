from pixelcanvas import PixelCanvas
from utils import Color
import math
import utils
import os
from colored import fg
from __future__ import print_function

colors=[
  {'Color': 'Black', 'r': 0, 'g': 0, 'b': 0, 'FG': 30, 'code': '\033[30m'},
  {'Color': 'Red', 'r': 205, 'g': 0, 'b': 0, 'FG': 31, 'code': '\033[31m'},
  {'Color': 'Green', 'r': 0, 'g': 205, 'b': 0, 'FG': 32, 'code': '\033[32m'},
  {'Color': 'Yellow', 'r': 205, 'g': 205, 'b': 0, 'FG': 33, 'code': '\033[33m'},
  {'Color': 'Blue', 'r': 0, 'g': 0, 'b': 238, 'FG': 34, 'code': '\033[34m'},
  {'Color': 'Magenta', 'r': 205, 'g': 0, 'b': 205, 'FG': 35, 'code': '\033[35m'},
  {'Color': 'Cyan', 'r': 0, 'g': 205, 'b': 205, 'FG': 36, 'code': '\033[36m'},
  {'Color': 'White', 'r': 229, 'g': 229, 'b': 229, 'FG': 37, 'code': '\033[37m'},
  {'Color': 'Gray', 'r': 127, 'g': 127, 'b': 127, 'FG': 38, 'code': '\033[38m'}
]

ENDC = '\033[0m'

def closestColor(color):
  r = (color >> 16) & 0xFF
  g = (color >> 8) & 0xFF
  b = color & 0xFF

  dist = 200000
  retVal = 'Black'
  for color in colors:
    temp = math.sqrt( (r - color['r'])**2 + (g - color['g'])**2 + (b - color['b'])**2)
    if temp < dist:
      retVal = color['Color']
      dist = temp
  return retVal

def printPixel(pixel):
  if closestColor(pixel) is 'Black':
    print('- ', end='')
  else:
    for color in colors:
      if closestColor(pixel) is color['Color']:
        code = color['code']
        print(code + 'o ' + ENDC, end='')
        return

class SimulatedCanvas(PixelCanvas):
  def __init__(self, width=20, height=32, pin=18, freq_hz=800000, dma=5, invert=False,
	  brightness=50):
    self._width = width
    self._height = height

    # Color data for each pixel, in list-of-lists format
    self._array = [[Color(0,0,0) for i in range(height)] for j in range(width)] #Index as _array[row][col]

    # List to use for indexing into led strip (vectorization)
    self._indices = [i for i in range(width*height)]

  def display(self):
    print('+-----------------------------------------+')
    rows = list(map(list, zip(*self._array)))
    for row in rows:
      print('| ', end='')
      for pixel in row:
        printPixel(pixel)
      print('|')
    print('+-----------------------------------------+')





