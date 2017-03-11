#TODO
# Finish main loop structure, including main features
#   night
#   notifications
# Implement better human-mouse
#   Implement current mouse position mouse data selection.
# Get better mouse data.
# Decide tooltip display
#   If decided to use system tray icon, create icons for it.

## BEGIN WORK ON PARENT CLASS, REWRITING IN CLASS FORM

import sys
import math
import DataLog
import winsound
import datetime
import Tooltip
import multiprocessing
import random
import atexit
import tkinter
import numpy, PIL
from tkinter import *
from PIL import Image, ImageGrab
from HotkeyThread import *
from WindowMgr import *


def anti_afk(user_data):
    try:
        hotkey_state = 0
        if user_data['tooltip_mouse'] == 1 and user_data['tooltip'] == 0:
            log.add_log("error", "tooltip mouse selected without tooltip")
            raise OptionMismatch("Tooltip mouse selected without tooltip.")
        thread = multiprocessing.Process(target=hotkey, args=[win32con.VK_ESCAPE])
        thread.start()
        max_time = time.time() + (int(user_data['max_time'])*60)
        mouse_pos = 0
        m = 1
        log.add_log("log", "Beginning anti-AFK routine...")
        while time.time() < max_time:
            date_time = []
            date_time += time.strftime("%H,%M,%S").split(',')
            hour = date_time[0]
            minute = date_time[1]
            sec = date_time[2]
            print("########################################### " + str(hour) + ":" + str(minute) + ":" + str(sec) + " ############################################")
            print("Loop iteration: " + str(m))
            print("Maximum time: " +str(math.floor((max_time - time.time())/60)))
            if (hotkey_state < 0):
                print("Hotkey: ESCAPE pressed. Exiting...")
                raise EscapeError

            quick_chance = random.random()
            if quick_chance > .6:
                print("Time mode: Short")
                loop_time = random.randint(0, 150)
            else:
                print("Time mode: Normal")
                loop_time = random.randint(250, 290)

            action_times = []

            j=0
            while j < 5:
                num = random.random() / 2
                action_times.append(num)
                j+=1

            time.sleep(action_times[random.randint(0,4)])
            movement_data = get_movement_data()

            maximize()
            if not logged_in() and m>1:
                winsound.Beep(250, 100)
                continue

            move_mouse(movement_data)

            if(user_data['min_max'] == 1):
                minimize()
            end_time = time.time() + loop_time

            if (user_data['tooltip'] == 1):
                tooltip_thread = multiprocessing.Process(target=tooltip_gui, args=[loop_time])
                tooltip_thread.start()

            mouse_pos = win32gui.GetCursorPos()
            last_int = math.floor(end_time - time.time())

            while time.time() <= end_time:
                #print("Test")
                if (hotkey_state < 0):
                    print("Hotkey ESCAPE pressed: Exiting...")
                    raise EscapeError
                if math.floor(end_time - time.time()) != last_int:
                    sys.stdout.write(str(math.floor(end_time - time.time())) + "\r")
                    sys.stdout.flush()
                    last_int = math.floor(end_time - time.time())
            m+=1
            print("#################################################################################################")
            try:
                tooltip_thread.terminate()
            except NameError:
                pass
    except EscapeError:
        show_gui()
    except OptionMismatch:
        show_gui()
    finally:
        end_sequence()

def show_gui():
    global top, min_max, tooltip_data, tooltip_mouse, beep, notif, night, max_time
    top = Tk()
    min_max = IntVar()
    tooltip_data = IntVar()
    tooltip_mouse = IntVar()
    beep = IntVar()
    notif = IntVar()
    night = IntVar()
    max_time = StringVar()

    min_max_c = Checkbutton(top, text="Min/Max", variable=min_max)
    tooltip_c = Checkbutton(top, text="Tooltip", variable=tooltip_data)
    tooltip_mouse_c = Checkbutton(top, text="Mouse", variable=tooltip_mouse)
    beep_c = Checkbutton(top, text="Beep", variable=beep)
    notif_c = Checkbutton(top, text="Notifications", variable=notif)
    night_c = Checkbutton(top, text="Night", variable=night)
    max_time_c = Entry(top, text="Max Time", textvariable=max_time)
    btn = tkinter.Button(top, text="Submit", command=submit)

    min_max_c.pack()
    tooltip_c.pack()
    tooltip_mouse_c.pack()
    max_time_c.pack()
    notif_c.pack()
    night_c.pack()
    btn.pack()

    top.mainloop()

def submit():
    global data
    print("Retrieving data...")
    if max_time.get() == '':
        _max_time = 999999
    else:
        _max_time = max_time.get()
    user_data = {'min_max': min_max.get(),
           'tooltip': tooltip_data.get(),
           'tooltip_mouse': tooltip_mouse.get(),
           'beep': beep.get(),
           'max_time': _max_time,
           'notif': notif.get(),
           'night': night.get()}
    data = UserData(user_data)
    top.quit()
    top.destroy()

def hotkey(self, hotkey=win32con.VK_ESCAPE):
    global hotkey_state
    while True:
        hotkey_state = win32api.GetAsyncKeyState(hotkey)

def maximize():
    try:
        window = WindowMgr()
        window.find_window_wildcard("RuneScape")
        window.set_foreground()
        print("Maximizing")
    except:
        maximize()


def minimize():
    try:
        window = WindowMgr()
        hwnd = window.find_window_wildcard("RuneScape")
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        print("Minimizing...")
    except:
        maximize()

def logged_in():
    import math, operator, functools
    from PIL import ImageChops, Image  # $ pip install pillow
    from pyscreenshot import grab  # $ pip install pyscreenshot
    import pyscreenshot

    pic = grab(bbox=(570, 530, 801, 581))
    pic.save("screen.png")
    im1 = pic
    im2 = Image.open("PlayNow.png")
    h = ImageChops.difference(im1.convert("RGB"), im2.convert("RGB")).histogram()

    # calculate rms
    val = math.sqrt(functools.reduce(operator.add,
                                     map(lambda h, i: h * (i ** 2), h, range(256))
                                     ) / (float(im1.size[0]) * im1.size[1]))
    if val > 5:
        return True
    return False


def move_mouse(list):
    """ Move mouse according to data given from list """
    oldposx = 0
    oldposy = 0
    same_count = 0
    print("Attempting to move cursor to " + str(list[-1][0]) + ":" + str(list[-1][1]) + " from " + str(list[0][0]) + ":" + str(list[0][1]))
    for i in list:
        try:
            # noinspection PyUnboundLocalVariable
            randinterval
        except NameError:
            randinterval = random.random()*50+25
        else:
            randnum = random.random()
            if randnum >= .5:
                randinterval = randinterval + math.floor(random.random()*5)
            else:
                randinterval = randinterval - math.floor(random.random()*5)
        if randinterval <= 0:
            randinterval = random.random()*50+25
        rand = random.random()
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
        time.sleep(.01 + (random.random()/100))

def tooltip_gui(loop_time):
    """ Main code for tooltip """
    global tooltip
    print("Time until next iteration: " + str(loop_time))
    tooltip = Tooltip.Tooltip(count=int(loop_time))
    pos = win32gui.GetCursorPos()
    posx = pos[0]
    posy = pos[1]
    tooltip.geometry('%dx%d+%d+%d' % (50, 20, 0, 0))
    tooltip.overrideredirect(True)
    tooltip.attributes("-topmost", True)
    tooltip.mainloop()

def is_int(some_number):
    """ Return True if number is an integer """
    inNumber = some_number
    inNumberint = int(inNumber)
    return inNumber == inNumberint

def checkEqual(iterator):
    """ Return True iff all values in iterator are equal """
    return len(set(iterator)) <= 1

"""
# def get_movement_data_target(target_x, target_y):
#     import random
#     with open('test.txt') as f:
#         mouse_movements = [tuple(map(int, i.split())) for i in f]
#     coords = win32gui.GetCursorPos()
#     posx = coords[0]
#     posy = coords[1]
#     #print((posx, posy))
#     def spiral(X, Y):
#         x = y = 0
#         dx = 0
#         dy = -1
#         output = []
#         for i in range(max(X, Y) ** 2):
#             if (-X / 2 < x <= X / 2) and (-Y / 2 < y <= Y / 2):
#                 #print((x, y))
#                 output.append((x, y))
#             if x == y or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
#                 dx, dy = -dy, dx
#             x, y = x + dx, y + dy
#         return output
#     print("Mouse positions found in file. Looking for target data...")
#     lst = grab_all_indexes((posx, posy), mouse_movements)
#     lst2 = grab_all_indexes((target_x, target_y), mouse_movements)
#     print(lst, lst2)
#     choice = random.choice(lst)
#     choice2 = random.choice(lst2)
#     i = 0
#     while choice > choice2:
#         choice = random.choice(lst)
#         choice2 = random.choice(lst2)
#         i+=1
#         if i > 25:
#             break
#     if choice > choice2:
#         print("Sequence from current position to target position found. Sending data...")
#         start_index = choice
#         end_index = choice2
#         return mouse_movements[start_index:end_index]
#     else:
#         print("Current mouse position not found in file , searching for other positions...")
#         for i in spiral(posx, posy):
#             for j in spiral(target_x, target_y):
#                 if (i[0] + posx, i[1] + posy) in mouse_movements[0:-50] and (j[0] + target_x, j[1] + target_y) in mouse_movements:
#                     lst = grab_all_indexes((i[0] + posx, i[1] + posy), mouse_movements)
#                     lst2 = grab_all_indexes((j[0] + target_x, j[1] + target_y), mouse_movements)
#                     choice = random.choice(lst)
#                     choice2 = random.choice(lst)
#                     i=0
#                     while choice > choice2:
#                         choice = random.choice(lst)
#                         choice2 = random.choice(lst2)
#                         i += 1
#                         if i > 25:
#                             break
#                     start_index = choice
#                     end_index = choice2
#                     print("Similar mouse position found. Sending data...")
#                     return mouse_movements[start_index:end_index]
#         print("No similar mouse data found. Sending data...")
#         rand = round(random.random() * len(mouse_movements) / 2 - 1)
#         start_index = rand
#         end_index = rand + random.randint(50, 250)
#         while (checkEqual(mouse_movements[start_index:end_index])):
#             rand = random.randint(0, round(random.random() * len(mouse_movements) / 2 - 1))
#             start_index = mouse_movements[rand]
#             end_index = rand + random.randint(50, 250)
#         return mouse_movements[start_index:end_index]
#
#     pass
"""

def get_movement_data():
    import random
    with open('test.txt') as f:
        mouse_movements = [tuple(map(int, i.split())) for i in f]
    coords = win32gui.GetCursorPos()
    posx = coords[0]
    posy = coords[1]
    #print((posx, posy))
    def spiral(X, Y):
        x = y = 0
        dx = 0
        dy = -1
        output = []
        for i in range(max(X, Y) ** 2):
            if (-X / 2 < x <= X / 2) and (-Y / 2 < y <= Y / 2):
                #print((x, y))
                output.append((x, y))
            if x == y or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
                dx, dy = -dy, dx
            x, y = x + dx, y + dy
        return output

    if (posx, posy) in mouse_movements:
        print("Current mouse position found in file. Sending data...")
        lst = grab_all_indexes((posx, posy), mouse_movements)
        choice = random.choice(lst)
        start_index = choice
        end_index = start_index + random.randint(50, 250)
        return mouse_movements[start_index:end_index]
    else:
        print("Current mouse position not found in file, searching for other positions...")
        for i in spiral(posx, posy):
            if (i[0] + posx, i[1] + posy) in mouse_movements[0:-50]:
                lst = grab_all_indexes((i[0] + posx, i[1] + posy), mouse_movements)
                choice = random.choice(lst)
                start_index = choice
                end_index = start_index + random.randint(50, 250)
                print("Similar mouse position found. Sending data...")
                return mouse_movements[start_index:end_index]
        print("No similar mouse data found. Sending data...")
        rand = round(random.random()*len(mouse_movements)/2 -1)
        start_index = rand
        end_index = rand + random.randint(50, 250)
        while (checkEqual(mouse_movements[start_index:end_index])):
            rand = random.randint(0, round(random.random() * len(mouse_movements) / 2 - 1))
            start_index = mouse_movements[rand]
            end_index = rand + random.randint(50, 250)
        return mouse_movements[start_index:end_index]

def grab_all_indexes(tuple, mouse_movements):
    lst = []
    for i in range(0, len(mouse_movements)):
        if tuple == mouse_movements[i]:
            lst.append(i)
    return lst


def log():

    pass

def end_sequence():
    """ Ending sequence for program. """
    # noinspection PyBroadException
    try:
        tooltip.quit()
        log()
    except:
        pass
    return


class UserData():
    def __init__(self, data):
        if (not isinstance(data, dict)):
            raise TypeError("Class UserData only accepts dictionary parameters.")
        self._info = data

    def get(self):
        return self._info

class OptionMismatch(Exception):
    pass

class EscapeError(Exception):
    pass



if __name__ == "__main__":
    global log
    log = DataLog.DataLog
    atexit.register(end_sequence)
    while(True):
        show_gui()
        user_data = data.get()
        anti_afk(user_data)
    # noinspection PyUnboundLocalVariable
    print(user_data)