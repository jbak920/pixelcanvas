import time
import random
import sys
sys.path.insert(0,'/home/pi/pixelcanvas')

from utils import Color
from utils import multiply

ZERO =     [[1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1]]
ONE =      [[0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [1, 1, 1, 1]]
TWO =      [[1, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 1, 1]]
THREE =    [[1, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [1, 1, 1, 1]]
FOUR =     [[1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1]]
FIVE =     [[1, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [1, 1, 1, 1]]
SIX =      [[1, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1]]
SEVEN =    [[1, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1]]
EIGHT =    [[1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1]]
NINE =     [[1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1]]

ZERO.reverse()
ONE.reverse()
TWO.reverse()
THREE.reverse()
FOUR.reverse()
FIVE.reverse()
SIX.reverse()
SEVEN.reverse()
EIGHT.reverse()
NINE.reverse()

digits = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

hour_tens_loc = [22,3]
hour_ones_loc = [22,9]

minute_tens_loc = [13,5]
minute_ones_loc = [13,11]

second_tens_loc = [4,7]
second_ones_loc = [4,13]

def embed(array, digit, location):
    '''
    Add the digit to the location in array. The location is the bottom-left of the array
    '''
    for j,row in enumerate(digit):
        for i,pixel in enumerate(row):
            array[location[1]+i][location[0]+j] = pixel
      
def displayClock(canvas):
    if canvas._height is not 32 or canvas._width is not 20:
        print 'The canvas is not 20x32!'
        return
    
    else:
        t_end = time.time() + 90 # Loop for 90 seconds
        while time.time() < t_end:
            hour = time.localtime().tm_hour
            minute = time.localtime().tm_min
            sec = time.localtime().tm_sec
            
            hour_tens   = int(str(hour).zfill(2)[0])
            hour_ones   = int(str(hour).zfill(2)[1])
            minute_tens = int(str(minute).zfill(2)[0])
            minute_ones = int(str(minute).zfill(2)[1])
            second_tens = int(str(sec).zfill(2)[0])
            second_ones = int(str(sec).zfill(2)[1])
                       
            
            num = multiply(digits[hour_tens], 0xFF0000)
            embed(canvas._array, num, hour_tens_loc)
            
            num = multiply(digits[hour_ones], 0xFF0000)
            embed(canvas._array, num, hour_ones_loc)
            
            num = multiply(digits[minute_tens], 0x00FF00)
            embed(canvas._array, num, minute_tens_loc)
            
            num = multiply(digits[minute_ones], 0x00FF00)
            embed(canvas._array, num, minute_ones_loc)
            
            num = multiply(digits[second_tens], 0x0000FF)
            embed(canvas._array, num, second_tens_loc)
            
            num = multiply(digits[second_ones], 0x0000FF)
            embed(canvas._array, num, second_ones_loc)
            
            canvas.display()
            time.sleep(0.1)            
            
            