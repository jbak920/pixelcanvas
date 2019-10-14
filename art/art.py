import time
import sys
sys.path.insert(0,'/home/pi/pixelcanvas')

from PIL import Image

from utils import Color

def displayArt(canvas):
    f1 = Image.open('/home/pi/pixelcanvas/art/standing_mario.png')
    f2 = Image.open('/home/pi/pixelcanvas/art/standing_mario_2.png')
    rgb_f1 = f1.convert('RGB')
    rgb_f2 = f2.convert('RGB')
    frame1 = rgb_f1.load()
    frame2 = rgb_f2.load()
    
    if (f1.size == (canvas._width, canvas._height)) or (f2.size == (canvas._width, canvas._height)):
       
        frame1_array = [[Color(0,0,0) for i in range(canvas._height)] for j in range(canvas._width)]
        frame2_array = [[Color(0,0,0) for i in range(canvas._height)] for j in range(canvas._width)]
        for i,col in enumerate(frame1_array):
            for j,pix in enumerate(col):
                r, g, b = frame1[i,j]
                frame1_array[i][j] = Color(r, g, b)

        for i,col in enumerate(frame2_array):
            for j,pix in enumerate(col):
                r, g, b = frame2[i,j]
                frame2_array[i][j] = Color(r, g, b)
                
        for col in frame1_array:
            col.reverse()  
            
        for col in frame2_array:
            col.reverse()  
        
        while(True):
            canvas._array = frame1_array
            canvas.display()
            time.sleep(0.1)
            canvas._array = frame2_array
            canvas.display()
            time.sleep(0.1)
            
    else:
        print "Image sizes do not match canvas dimensions!"