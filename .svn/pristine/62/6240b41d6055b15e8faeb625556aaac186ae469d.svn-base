__author__ = 'dzhang1'
"""
Running on cyg_server with special video card which works as a QD.
nircmd.exe should be deposited during the same folder.
Default dir "C:\cygwin\home\cyg_server\sqa_at"
usage:
kick off this script and it will keep on running by itself.
"""

from abc import ABCMeta, abstractmethod
from win32api import *
import time
import subprocess
import os
import logging
logger = logging.getLogger(__name__)


class NirCmd(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _para_make(self):
        """
        make the parameters which could be used in this script from users' parameters input
        """
        pass

    @abstractmethod
    def _cmd_make(self):
        """
        make the cmd sent to Nircmd.exe
        """
        pass

    @abstractmethod
    def _cmd_send(self):
        """
        send Nircmd.exe xxxxx cmd by subprocess
        """
        pass


class NirMethod(NirCmd):
    def __init__(self):
        super(NirMethod, self).__init__()

    @staticmethod
    def _cmd_make(cmd_maker):
        cmd_maker.insert(0, r"nircmd.exe")
        return cmd_maker

    @staticmethod
    def _cmd_send(__cmd_list):
        return subprocess.Popen(' '.join(__cmd_list))

    @staticmethod
    def _para_make(parameters_maker):
        return parameters_maker


class NirAction(NirMethod):
    def __init__(self, args):
        super(NirAction, self).__init__()
        self.args = args.upper().strip()

    def _resolution_make(self):
        return self.args.split('_')

    def _setdisplay_cmd_make(self):
        __cmd_list = self._resolution_make()
        __cmd_list.insert(0, "setdisplay")
        return __cmd_list

    def setdisplay(self):
        self._para_make(self._resolution_make())
        __cmd = self._cmd_make(self._setdisplay_cmd_make())
        self._cmd_send(__cmd)


class ResolutionMethod():
    def __init__(self):
        self.width = str(GetSystemMetrics(0))
        self.height = str(GetSystemMetrics(1))
        self.resolution = ["width", "height"]

    def get_current_resolution(self):
        self.resolution[0] = self.width
        self.resolution[1] = self.height
        return "_".join(self.resolution)

if __name__ == "__main__":
    resolution_path = "C:\\cygwin\\home\\cyg_server\\sqa_at\\resolution\\"
    while 1:
        resolution = os.listdir(resolution_path)
        if len(resolution) == 1:
            TV = NirAction(resolution[0])
            TV.setdisplay()
            time.sleep(1)
            os.rmdir(resolution_path + resolution[0])
            monitor = ResolutionMethod()
            if resolution[0][:-6] == monitor.get_current_resolution():
                os.mkdir(resolution_path + monitor.get_current_resolution())
            else:
                os.system("taskkill/f /im nircmd.exe")
            time.sleep(2)
            for i in resolution:
                if os.path.exists(resolution_path + i):
                    os.rmdir(resolution_path + i)
        else:
            continue
