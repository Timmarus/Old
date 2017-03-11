import time, win32api, win32con, win32gui


end_time = time.time() + 60
list = []
f = open('test.txt', 'a')
oldposx = int()
oldposy = int()
same_count = 0
while True:
    pos = win32gui.GetCursorPos()
    posx = pos[0]
    posy = pos[1]
    if posx == oldposx or posy == oldposy:
        same_count += 1
    else:
        same_count = 0
    oldposx = posx
    oldposy = posy
    if same_count <= 10:
        list.append(str(pos[0]) + " " + str(pos[1]))
        f.write(str(pos[0]) + " " + str(pos[1]) + '\n')
        time.sleep(.01)
        print(str(pos[0]) + " " + str(pos[1]))
    else:
        print(False)
f.close()

"""
with open('test.txt') as f:
    mylist = [tuple(map(float, i.split())) for i in f]

print(mylist)
f = open('test.txt', 'r')

for i in mylist:
    posx = int(i[0])
    posy = int(i[1])
    win32api.SetCursorPos((posx, posy))
    time.sleep(.01)
"""