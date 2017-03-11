import win32gui, win32con, win32api, re

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd
            return hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
        return self._window_enum_callback(self._handle, wildcard)

    def set_foreground(self, id=None):
        """put the window in the foreground"""
        if not id:
            id = self._handle
        win32gui.ShowWindow(id, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(self._handle)