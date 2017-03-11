# import win32api, win32gui, win32con
#
# while True:
#     print(win32api.GetKeyState(27))

import msvcrt

def test():
    while True:
        result = msvcrt.getch()
        print("test")
        print(result)

if __name__ == '__main__':
    test()