import time
import sys
sys.path.insert(0,'/home/pi/pixelcanvas')
import os
import random

import json
from PIL import Image

from utils import Color

def animate(canvas, dir):
    '''Displays animation based on the directory given as argument.
    
    inputs: 
        - canvas is a PixelCanvas object
        - dir is a string with the directory that the animation should pull from
        - but if dir is 'random', then choose a random animation to play
    '''
    
    if dir is 'random':
        dirs = [x[0] for x in os.walk('.')]
        print dirs
    
    dir = '/home/pi/pixelcanvas/animation/'+ dir 
    fname = dir + '/frames.json'
    with open(fname) as json_data:
        json_object = json.load(json_data)
        json_data.close()
        frames = []
        for line,frame_data in enumerate(json_object):
            filename = frame_data["filename"]
            interval = frame_data["interval"] #seconds
            f = Image.open(dir + '/' + filename)
            rgb_f = f.convert('RGB')
            image = rgb_f.load()
            image_array =  [[Color(0,0,0) for i in range(canvas._height)] for j in range(canvas._width)]
            
            if (f.size == (canvas._width, canvas._height)):
                for i,col in enumerate(image_array):
                    for j,pix in enumerate(col):
                        r, g, b = image[i,j]
                        image_array[i][j] = Color(r, g, b)
                for col in image_array:
                    col.reverse()
                frame = {"image": image_array, "interval": interval}
                frames.append(frame)
                
            else:
                print filename + "does not match canvas dimensions!"
                
    while(True):
        for frame in frames:
            canvas._array = frame["image"]
            canvas.display()
            time.sleep(float(frame["interval"]))