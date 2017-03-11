import sys
import math
import winsound
import datetime
import Tooltip
import multiprocessing
import random
import atexit
import tkinter
import numpy, PIL
import time
from tkinter import *
from PIL import Image, ImageGrab
from HotkeyThread import *
from WindowMgr import *
import time
import __main__

class DataLog:
    def __init__(self):
        self.time = time
        self.__main__ = __main__
        self.debug = []
        self.warning = []
        self.log = []
        self.output = []
        self.error = []

    def add_log(self, type, message):
        time = self.time.strftime("%Y-%m-%d, %I:%M:%S %p")
        if type == "debug":
            self.debug.append(time + " - " + self._main_.file + " - DEBUG - " + message)
        if type == "warning":
            self.warning.append(time + " - " + self._main_.file + " - WARNING - " + message)
        if type == "log":
            self.log.append(time + " - " + self._main_.file + " - LOG - " + message)
        if type == "output":
            self.output.append(time + " - " + self._main_.file + " - OUTPUT - " + message)
        if type == "error":
            self.error.append(time + " - " + self._main_.file + " - ERROR - " + message)