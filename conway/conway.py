import time
import sys
import random
sys.path.insert(0,'/home/pi/pixelcanvas')

import numpy as np

from utils import multiply

def num_neighbors(row, col, array):
    neighbors = 0
    try:
        neighbors += array[row][col+1]
    except:
        pass
    try:
        neighbors += array[row][col-1]
    except:
        pass
    try:
        neighbors += array[row+1][col+1]
    except:
        pass
    try:
        neighbors += array[row+1][col]
    except:
        pass
    try:
        neighbors += array[row+1][col-1]
    except:
        pass
    try:
        neighbors += array[row-1][col+1]
    except:
        pass
    try:
        neighbors += array[row-1][col]
    except:
        pass
    try:
        neighbors += array[row-1][col-1]
    except:
        pass
    return neighbors

def step(array):
    new_array = np.full_like(array, 0)
    for i,row in enumerate(array):
        for j,pixel in enumerate(row):
            neighbors = num_neighbors(i, j, array)
            if int(pixel) is 1:
                if neighbors < 2 or neighbors > 3:
                    new_array[i][j] = 0
                else:
                    new_array[i][j] = 1
            else:
                if neighbors == 3:
                    new_array[i][j] = 1
            
    return new_array

def life(canvas, init_file):
    if 'random' not in init_file:
        init_file = '/home/pi/pixelcanvas/conway/' + init_file
        with open(init_file, "r") as file:
            result = [[int(x) for x in line.split()] for line in file]
        array = np.array(result)
        array = array.T
    else:
        array = [[random.choice([0, 1]) for pixel in col] for col in canvas._array]
    
    t_end = time.time() + 60 # Loop for 60 seconds
    while time.time() < t_end:
        colored_array = multiply(array, 0xFFFFFF)
        canvas._array = colored_array
        canvas.display()
        time.sleep(0.3)
        new_array = step(array)
        if (new_array == array).all():
            break
        else:
            array = new_array
        
