# Pixel Canvas main program
# Author: Jonathan Baker
#
# This script manages the display for the Pixel Canvas LED display.

import time
import math
import random
import argparse

import rpi_ws281x

import tetrisBoard
from utils import Color

CANVAS_WIDTH   = 20      # Number of pixels per row
CANVAS_HEIGHT  = 32      # Number of pixels per column
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


def rainbowColor(pos, distance):
    """Generate a RGB color based on position through a rainbow of length distance"""
    frac = (pos / float(distance)) % 1
    if frac < 0.333:
	return Color(  0,                   int(255 - frac*255),  int(255*frac) )
    elif frac < 0.666:
	return Color(  int(255*frac),       0,                    int(255 - frac*255) )
    else:
	return Color(  int(255 - 255*frac),  int(frac*255),      0 )

class PixelCanvas(object):
    def __init__(self, width, height, pin, freq_hz=800000, dma=5, invert=False,
			brightness=255):
        # 1D LED strip
        self._strip = rpi_ws281x.PixelStrip(width*height, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self._strip.begin()
	self._width = width
	self._height = height

        # Color data for each pixel, in list-of-lists format
        self._array = [[Color(0,0,0) for i in range(height)] for j in range(width)]

	# List to use for indexing into led strip (vectorization)
	self._indices = [i for i in range(width*height)]

    def array2strip(self):
        temp = [self._array[index] if index%2 is 0 else self._array[index][::-1] for index in range(len(self._array)) ]
        return [item for sublist in temp for item in sublist]

    def display(self):
	for i,color in enumerate(self.array2strip()):
            self._strip.setPixelColor(i, color)
	self._strip.show()

    def turnOff(self):
	self._array = [[Color(0,0,0) for i in range(self._height)] for j in range(self._width)]
	self.display()

    def circular_rainbow(self):
	for i in range(self._height):
	    for j in range(self._width):
		radius = math.sqrt(i*i + j*j)
		self._array[j][i] = rainbowColor(radius, 10)

    def tetris2pixel_array(self, tetris):
	for i,col in enumerate(tetris):
	    for j,pixel in enumerate(col):
		self._array[2*j]  [2*i]   = pixel
		self._array[2*j]  [2*i+1] = pixel
		self._array[2*j+1][2*i]   = pixel
		self._array[2*j+1][2*i+1] = pixel


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create PixelCanvas object with appropriate configuration.
    canvas = PixelCanvas(CANVAS_WIDTH, CANVAS_HEIGHT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    canvas._strip.begin()
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while (True)
            board = tetrisBoard.Board(16, 10)
            board.makeNewPiece()
    
            while (board.gameStep()):
                time.sleep(0.5)
                canvas.tetris2pixel_array(board.getBoard())
                canvas.display()
                board.makeMove(random.randrange(3))
    
            time.sleep(0.5)
            canvas.tetris2pixel_array(board.getBoard())
            canvas.display()


    except KeyboardInterrupt:
        if args.clear:
            canvas.turnOff()
