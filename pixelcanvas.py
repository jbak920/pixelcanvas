# Pixel Canvas object
# Author: Jonathan Baker
#
# This script manages the display for the Pixel Canvas LED display

import rpi_ws281x

import tetrisBoard
from utils import Color

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
                self._array[j][i] = utils.rainbowColor(radius, 10)

    def tetris2pixel_array(self, tetris):
        for i,col in enumerate(tetris):
            for j,pixel in enumerate(col):
                self._array[2*j]  [2*i]   = pixel
                self._array[2*j]  [2*i+1] = pixel
                self._array[2*j+1][2*i]   = pixel
                self._array[2*j+1][2*i+1] = pixel
