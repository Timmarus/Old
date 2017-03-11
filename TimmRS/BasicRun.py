import time, win32api, random
from random import *


with open('test.txt') as f:
    mylist = [tuple(map(float, i.split())) for i in f]

def move_mouse(list):
    oldposx = 0
    oldposy = 0
    same_count = 0
    for i in list:
        rand = random()/50
        posx = int(i[0])
        posy = int(i[1])
        if posx == oldposx or posy == oldposy:
            same_count += 1
        else:
            same_count = 0
        oldposx = posx
        oldposy = posy
        if same_count <= 10:
            win32api.SetCursorPos((posx, posy))
        else:
            continue
        time.sleep(rand)

start_index = round(random()*len(mylist)/2 -1)
end_index = start_index + randint(50, 100)
while (True):
    quick_chance = random()
    if quick_chance >= .6:
        loop_time = randint(0, 150)
        print("Long time.")
    else:
        loop_time = randint(250, 290)
    if (start_index >= len(mylist) or end_index >= len(mylist)):
        start_index = round(random()*len(mylist)/2 -1)
        end_index = start_index + randint(50, 100)
        print("Resetting...")
    move_mouse(mylist[start_index:end_index])
    #win32api.SendKeys(")
    start_index = end_index
    end_index = start_index + randint(50, 100)
    print("Test)")
    time.sleep(loop_time)

