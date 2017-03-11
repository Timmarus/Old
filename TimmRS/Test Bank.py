


### Checking for keyboard presses ###
"""
import win32con, win32api
while(True):
    print(win32api.GetAsyncKeyState(16))
"""
#####################################

### Threading Tests ###
"""
import threading
import time


class SimpleThread(object):
     Simple class for
    threading.


    def __init__(self, interval=1):
        ''' Constructor

        :type interval: int
        :param interval: Check interval, in seconds
        '''
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        ''' Method that runs forever '''
        while True:
            # Do something
            print('Doing something imporant in the background')

            time.sleep(self.interval)

example = ThreadingExample()
time.sleep(3)
print('Checkpoint')
time.sleep(2)
print('Bye')
"""
#####################
### Image finding test ###
"""
import PIL, numpy, time
import cv2
from cv2 import *
from PIL import Image, ImageGrab
def check_login_state(img1, img2):
    img1 = numpy.asarray(img1)
    img2 = numpy.asarray(img2)

    # img1=numpy.array([[1,2,3],[4,5,6],[7,8,9]])
    # img2=numpy.array([[0,0,0,0,0],[0,1,2,3,0],[0,4,5,6,0],[0,7,8,9,0],[0,0,0,0,0]])

    img1y = img1.shape[0]
    img1x = img1.shape[1]

    img2y = img2.shape[0]
    img2x = img2.shape[1]

    stopy = img2y - img1y + 1
    stopx = img2x - img1x + 1

    for x1 in range(0, stopx):
        for y1 in range(0, stopy):
            x2 = x1 + img1x
            y2 = y1 + img1y

            pic = img2[y1:y2, x1:x2]
            test = pic == img1

            if test.all():
                return True

    return False


#     screen = ImageGrab.grab()
#     haystack = screen.load()
#     haystack = Image.open("PlayNow.png")
#     haystack = haystack.load()
#     i = "PlayNow2test.png"
#     image = Image.open(i)
#     needle = image.load()
#     return set(numpy.unique(needle)).issubset(set(numpy.unique(haystack)))
small = Image.open('Particles.png')
big = Image.open('PlayNow.png')

print(check_login_state(small, big))
time.sleep(1000)
"""
#####################33
# import PIL, numpy, time
# import cv2
# from cv2 import *
# from PIL import Image, ImageGrab
#
# def check_login_state():
#     screen = ImageGrab.grab()
#     screen.save("screen.png")
#     haystack = Image.open("screen.png")
#     needle = Image.open("PlayNow.png")
#     img1=numpy.asarray(needle)
#     img2=numpy.asarray(haystack)
#
#     #img1=numpy.array([[1,2,3],[4,5,6],[7,8,9]])
#     #img2=numpy.array([[0,0,0,0,0],[0,1,2,3,0],[0,4,5,6,0],[0,7,8,9,0],[0,0,0,0,0]])
#
#     img1y=img1.shape[0]
#     img1x=img1.shape[1]
#
#     img2y=img2.shape[0]
#     img2x=img2.shape[1]
#
#     stopy=img2y-img1y+1
#     stopx=img2x-img1x+1
#
#     for x1 in range(0,stopx):
#         for y1 in range(0,stopy):
#             x2=x1+img1x
#             y2=y1+img1y
#
#             pic=img2[y1:y2,x1:x2]
#             test=pic==img1
#
#             if test.all():
#                 return x1, y1
#
#     return False
#
# print(check_login_state())
# time.sleep(1000)
# import win32api, win32gui, win32gui
#
# while True:
#     print(win32api.GetCursorPos())

while True:
    import win32api
    print(win32api.GetCursorPos())

import cv2
import numpy as np
import subprocess
import math, operator, functools
from PIL import ImageChops, Image # $ pip install pillow
from pyscreenshot import grab # $ pip install pyscreenshot
import pyscreenshot

if __name__ == '__main__':
    # im = Image.open("PlayNow.png")
    # while True: # http://effbot.org/zone/pil-comparing-images.htm
    #     pic = grab(bbox=(570, 530, 801, 581))
    #     pic.save("screen.png")
    #     diff = ImageChops.difference(pic.convert("RGB"), im.convert("RGB"))
    #     bbox = diff.getbbox()
    #     if bbox is not None: # exact comparison
    #         print("True")
    #         break
    pic = grab(bbox=(570, 530, 801, 581))
    pic.save("screen.png")
    im1 = pic
    im2 = Image.open("PlayNow.png")
    h = ImageChops.difference(im1.convert("RGB"), im2.convert("RGB")).histogram()

    # calculate rms
    print(math.sqrt(functools.reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1])))
