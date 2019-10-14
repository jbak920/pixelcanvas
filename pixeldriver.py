# Pixel Canvas main program
# Author: Jonathan Baker
#
# This script manages the display for the Pixel Canvas LED display.

import argparse

import pixelcanvas
from tetris.tetris import playTetris
from snake.snake   import playSnake
from art.art import displayArt

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
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-p', '--program', help='specify what program to play (tetris, snake)')
    args = parser.parse_args()

    # Create PixelCanvas object with appropriate configuration.
    canvas = pixelcanvas.PixelCanvas(CANVAS_WIDTH, CANVAS_HEIGHT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    canvas._strip.begin()
    
    
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        if ('tetris' in args.program.lower()):
            playTetris(canvas)
        elif ('snake' in args.program.lower()):
            print 'snek'
        elif ('art' in args.program.lower()):
            displayArt(canvas)

    except KeyboardInterrupt:
        if args.clear:
            canvas.turnOff()