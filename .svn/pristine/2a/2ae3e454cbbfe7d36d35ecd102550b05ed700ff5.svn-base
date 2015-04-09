#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

try:
    import _winreg as winreg
except ImportError:
    import winreg


__all__ = ['Registry', 'setreg', 'getreg', 'delreg',
           'sethostname',
           'Daemon', 'DaemonService']


class Registry(object):
    def __init__(self, key=None):
        self.__key = None
        self.__obj = None
        if key:
            self.open(key)

    def open(self, key):
        tup = key.partition('\\')
        self.__key = key
        self.__obj = winreg.OpenKey(getattr(winreg, tup[0]), tup[2], 0, winreg.KEY_ALL_ACCESS)

    def set_key(self, key, value=None, valuetype=None):
        logger.info("setKey: key=[%s\\%s], value=[%s], valuetype=[%s]", self.__key, key, value, valuetype)
        if value:
            winreg.SetValue(self.__obj, key, valuetype, value)
        else:
            winreg.CreateKey(self.__obj, key)

    def del_key(self, key):
        logger.info("delKey: key=[%s\\%s]", self.__key, key)

        def del_subkey(hkey, subkey):
            hsubkeyobj = winreg.OpenKey(hkey, subkey)
            subkeyinfo = winreg.QueryInfoKey(hsubkeyobj)
            subsubkeynum = subkeyinfo[0]
            if subsubkeynum != 0:
                for index in range(subsubkeynum):
                    subsubkey = winreg.EnumKey(hsubkeyobj, index)
                    del_subkey(hsubkeyobj, subsubkey)
            winreg.CloseKey(hsubkeyobj)
            logger.debug("delKey: delete key '%s\\%s'", self.__key, subkey)
            winreg.DeleteKeyEx(hkey, subkey, None, None)
        del_subkey(self.__obj, key)

    def set_value(self, name, value, valuetype):
        winreg.SetValueEx(self.__obj, name, 0, valuetype, value)

    def get_value(self, name=None):
        return winreg.QueryValueEx(self.__obj, name)[0]

    def del_value(self, name):
        winreg.DeleteValue(self.__obj, name)

    def close(self):
        winreg.CloseKey(self.__obj)


def sethostname(name):
    reg = Registry()
    reg.open('HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters')
    reg.set_value('Hostname', name, winreg.REG_SZ)
    reg.set_value('NV Hostname', name, winreg.REG_SZ)
    reg.close()

    setreg('HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName',
           'ComputerName',
           name,
           winreg.REG_SZ)
    setreg('HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\ComputerName\ActiveComputerName',
           'ComputerName',
           name,
           winreg.REG_SZ)


def setreg(key, name=None, value=None, valuetype=None):
    reg = Registry()
    try:
        reg.open(key)
    except winreg.error:
        tup = key.partition('\\')
        reg.open(tup[0])
        reg.set_key(tup[2])
        reg.close()
    else:
        reg.close()
    
    reg.open(key)
    if name:
        reg.set_value(name, value, valuetype)
    else:
        if value:
            reg.set_key(value, valuetype)
    reg.close()


def getreg(key, name=None):
    reg = Registry()
    reg.open(key)
    reg.get_value(name)
    reg.close()


def delreg(key, name=None):
    reg = Registry()
    if name:
        reg.open(key)
        reg.del_value(name)
    else:
        tup = key.rpartition("\\")
        reg.open(tup[0])
        reg.del_key(tup[2])
    reg.close()


import re
import win32api
import win32gui
import win32con
import win32process


def killProcess(pid):
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
    win32api.TerminateProcess(handle, 0)
    win32api.CloseHandle(handle)


def findWindowProcessIds(regex):
    if not isinstance(regex, re._pattern_type):
        regex = re.compile(regex)
    pids = []
    def _filter(hwnd, regex):
        s = win32gui.GetWindowText(hwnd)
        if regex.match(s):
            pid = win32process.GetWindowThreadProcessId(hwnd)
            pids.append(pid)
    win32gui.EnumChildWindows(0, _filter, regex)
    return pids


def getWindowProcessId(text):
    pid = None
    wid = win32gui.FindWindow(None, text)
    if wid:
        pid = win32process.GetWindowThreadProcessId(wid)[1]   
    return pid


from abc import ABCMeta, abstractmethod, abstractproperty
import win32serviceutil
import win32service
import win32event
import winerror
import servicemanager
import os


class Daemon(object, win32serviceutil.ServiceFramework):
    """Reference: http://code.activestate.com/recipes/551780/"""

    __metaclass__ = ABCMeta

    @abstractproperty
    def _svc_name_(self):
        pass

    @abstractproperty
    def _svc_display_name_(self):
        pass

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self._run()
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        except:
            logger.exception("")
            self._stop()
            raise

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self._stop()
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    start = SvcDoRun
    stop = SvcStop

    @abstractmethod
    def _run(self):
        pass

    @abstractmethod
    def _stop(self):
        pass


class DaemonService(object):
    def __init__(self, cls):
        if not issubclass(cls, Daemon):
            raise TypeError
        self.cls = cls
        self.svc_name = cls._svc_name_
        self.svc_clss = win32serviceutil.GetServiceClassString(cls)
        self.svc_disp = cls._svc_display_name_ if hasattr(cls, "_svc_display_name_") else self.svc_name
        self.svc_desp = cls._svc_description_ if hasattr(cls, "_svc_description_") else None
        self.svc_deps = cls._svc_deps_ if hasattr(cls, "_svc_deps_") else None
        self.exe_name = cls._exe_name_ if hasattr(cls, "_exe_name_") else None
        self.exe_args = cls._exe_args_ if hasattr(cls, "_exe_args_") else None

    def create(self, **kwargs):
        logger.info("installing service: %s", self.svc_name)
        try:
            win32serviceutil.InstallService(self.svc_clss, self.svc_name, self.svc_disp)
            self.config(**kwargs)
            logger.info("service installed")
        except win32service.error as exc:
            if exc.winerror == winerror.ERROR_SERVICE_EXISTS:
                self.config(**kwargs)
            else:
                logger.info("error installing service: %s (%d)", exc.strerror, exc.winerror)

    def delete(self):
        try:
            win32serviceutil.RemoveService(self.svc_name)
            logger.info("service '%s' removed", self.svc_name)
        except win32service.error as exc:
            logger.info("error removing service: %s (%d)", exc.strerror, exc.winerror)
    
    def config(self, svc_disp=None, svc_desp=None, svc_deps=None, username=None, password=None, exe_name=None, exe_args=None, startup=None, interactive=None):
        starttype = None
        delayedstart = None
        if startup is not None:
            mapping = {"manual": win32service.SERVICE_DEMAND_START,
                       "auto": win32service.SERVICE_AUTO_START,
                       "delayed": win32service.SERVICE_AUTO_START,
                       "disabled": win32service.SERVICE_DISABLED}
            try:
                starttype = mapping[startup.lower()]
            except KeyError:
                logger.info("'%s' is not a valid startup option", startup)
        
            if startup.lower() == "delayed":
                delayedstart = True
            elif startup.lower() == "auto":
                delayedstart = False
        
        try:
            win32serviceutil.ChangeServiceConfig(self.svc_clss, 
                                                 self.svc_name,
                                                 serviceDeps=svc_deps,
                                                 startType=starttype,
                                                 bRunInteractive=interactive,
                                                 userName=username,
                                                 password=password,
                                                 exeName=exe_name,
                                                 displayName=svc_disp,
                                                 perfMonIni=None,
                                                 perfMonDll=None,
                                                 exeArgs=exe_args,
                                                 description=svc_desp,
                                                 delayedstart=delayedstart)
            logger.info("service '%s' updated", self.svc_name)
        except win32service.error as exc:
            logger.info("error changing service '%s' configuration: %s (%d)", self.svc_name, exc.strerror, exc.winerror)

if __name__ == "__main__":
    logging.basicConfig(
        level = logging.DEBUG, 
        format= '%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )