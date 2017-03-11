import threading, time, win32api, win32con

class HotkeyThread(object):
    """ Simple class for
    threading.
    """

    def __init__(self, target, args=(), interval=1):
        """ Constructor

        :type interval: float or None
        :param interval: Check interval, in seconds
        """

        self.interval = interval
        if interval == None:
            self.interval = 999999
        thread = threading.Thread(target=self.hotkey_check, args=[win32con.VK_ESCAPE])
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            print('Doing something imporant in the background')
            time.sleep(self.interval)

    def hotkey_check(self, hotkey):
        self.state = win32api.GetAsyncKeyState(hotkey)
        #print(self.state)
        return self.state

    def hotkey_loop(self, hotkey):
        while True:
            self.state = win32api.GetAsyncKeyState(hotkey)
        return self.state

