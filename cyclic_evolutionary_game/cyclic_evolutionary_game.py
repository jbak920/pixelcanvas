import time
import random

from utils import Color

def determineAction(actor, neighbor):
    if actor == 0:
        return 'do_nothing'
    if neighbor == 0:
        return 'reproduce'
    if actor == neighbor:
        return 'do_nothing'
    elif actor == 0xFF0000 and neighbor == 0xFF00:
        return 'eat'
    elif actor == 0xFF00 and neighbor == 0xFF:
        return 'eat'   
    elif actor == 0xFF and neighbor == 0xFF0000:
        return 'eat'
    else:
        return 'do_nothing'

def swap(canvas, pixel_row, pixel_col, neighbor_row, neighbor_col):
    temp = canvas_array[pixel_row][pixel_col]
    canvas_array[pixel_row][pixel_col] = canvas_array[neighbor_row][neighbor_col]
    canvas_array[neighbor_row][neighbor_col] = temp

def evolve(canvas, num_timesteps=100):
    canvas._array = [[random.choice([0, 0xFF0000, 0xFF00, 0xFF]) for pixel in col] for col in canvas._array]

    for i in range(num_timesteps):
        for j in range(canvas._height*canvas._width):
            pixel_row = random.randint(0, canvas._width-1)
            pixel_col = random.randint(0, canvas._height-1)
            neighbor = random.randint(0, 3)
            if neighbor == 0:
                neighbor_row = pixel_row
                neighbor_col = (pixel_col + 1) % canvas._height
            elif neighbor == 1:
                neighbor_row = pixel_row
                neighbor_col = (pixel_col - 1) % canvas._height
            elif neighbor == 2:
                neighbor_row = (pixel_row + 1) % canvas._width
                neighbor_col = pixel_col
            else:
                neighbor_row = (pixel_row - 1) % canvas._width
                neighbor_col = pixel_col
            options = {'swap': 7, 'action' : 3}
            weighted_options = [k for k in options for dummy in range(options[k])]
            choice = random.choice(weighted_options)
            if 'swap' in choice:
                temp = canvas._array[pixel_row][pixel_col]
                canvas._array[pixel_row][pixel_col] = canvas._array[neighbor_row][neighbor_col]
                canvas._array[neighbor_row][neighbor_col] = temp
            if 'action' in choice:
                action = determineAction(canvas._array[pixel_row][pixel_col], canvas._array[neighbor_row][neighbor_col])
                if 'reproduce' in action:
                    canvas._array[neighbor_row][neighbor_col] = canvas._array[pixel_row][pixel_col]
                elif 'eat' in action:
                    canvas._array[neighbor_row][neighbor_col] = 0
    
        canvas.display()
        time.sleep(0.1)