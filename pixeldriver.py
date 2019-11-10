#!/usr/bin/python

# Pixel Canvas main program
# Author: Jonathan Baker
#
# This script manages the display for the Pixel Canvas LED display.

import argparse
import random
import time

import pixelcanvas
from tetris.tetris import playTetris
from snake.snake   import playSnake
from animation.animation import animate
from digital_clock.digital_clock import displayClock
from conway.conway import life
from cyclic_evolutionary_game.cyclic_evolutionary_game import evolve

CANVAS_WIDTH   = 20      # Number of pixels per row
CANVAS_HEIGHT  = 32      # Number of pixels per column
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--program', default='random', help='specify what program to play (tetris, snake, animation)')
    parser.add_argument('-o', '--option', default='random', help='specify what options on a program-by-program basis')
    args = parser.parse_args()

    random.seed(a=None)
       
    # Create PixelCanvas object with appropriate configuration.
    canvas = pixelcanvas.PixelCanvas(CANVAS_WIDTH, CANVAS_HEIGHT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    canvas._strip.begin()

    try:
        while(True):
            if ('tetris' in args.program.lower()):
                playTetris(canvas)
            elif ('snake' in args.program.lower()):
                print 'snek'
            elif('animation' in args.program.lower()):
                animate(canvas, args.option.lower())
            elif('digital_clock' in args.program.lower()):
                displayClock(canvas)
            elif('conway' in args.program.lower()):
                life(canvas, args.option.lower())
            elif('cyclic_evolutionary_game' in args.program.lower()):
                evolve(canvas)
            else:
                canvas.turnOff()
                
                # Weight the programs differently
                # Keys are programs, values are weights
                options = {'playTetris(canvas)': 1, 'animate(canvas,args.option.lower())': 3, 'displayClock(canvas)': 1, 'life(canvas, args.option.lower())': 1, 'evolve(canvas)' : 1}
                weighted_options = [k for k in options for dummy in range(options[k])]
                exec(random.choice(weighted_options))

    except KeyboardInterrupt:
        canvas.turnOff()