#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import time
import ImageGrab
import ctypes
import win32gui
from pywinauto import application


class RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long), ('top', ctypes.c_long), ('right', ctypes.c_long), ('bottom', ctypes.c_long)]

    def __str__(self):
        return str((self.left, self.top, self.right, self.bottom))


def capture_soundrecorder_image(imgname):
    """
    Open windows SoundRecorder and capture it's picture
    """
    logger.debug("Launch SoundRecorder")
    app = application.Application.start(os.path.join("c:\\windows\\sysnative", "SoundRecorder.exe"))
    time.sleep(3)
    logger.debug("Capture SoundRecorder picture")
    rect = RECT()
    HWND = win32gui.GetForegroundWindow()   # get handler of current window
    ctypes.windll.user32.GetWindowRect(HWND, ctypes.byref(rect))    # get coordinate of current window
    rangle = (rect.left+2, rect.top+2, rect.right-2, rect.bottom-2)     # adjust coordinate
    img = ImageGrab.grab(rangle)    # capture current window
    img.save(imgname, 'JPEG')
    logger.debug("Exit SoundRecorder")
    app.kill_()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )

    capture_soundrecorder_image(r"d:\13.jpg")

