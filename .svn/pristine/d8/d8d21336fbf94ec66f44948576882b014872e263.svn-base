#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import re
import time
import json
import socket
import serial
import threading
import collections
import subprocess

from Queue import Queue, Empty
from abc import ABCMeta, abstractmethod
from simg.pattern.observer import BaseSubject, BaseListener


class BaseLogSubject(BaseSubject):
    __metaclass__ = ABCMeta

    def __init__(self):
        BaseSubject.__init__(self)
        self._should_stop = threading.Event()
        self._thread = None

    def open(self):
        self._should_stop.clear()
        self._thread = threading.Thread(target=self._notify)
        # framework using runner name to collect case log, if not set the runner sub-thread name same as the runner name
        # this sub-thread's log will not be add into case log file
        self._thread.name = threading.current_thread().name
        self._thread.start()

    def close(self):
        self._should_stop.set()
        if self._thread:
            self._thread.join()

    @abstractmethod
    def _notify(self):
        pass


class SerialLogListener(BaseListener):
    pass


class SerialLogSubject(BaseLogSubject):
    Listener = SerialLogListener

    def __init__(self, comport, baudrate=19200, logname=None):
        BaseLogSubject.__init__(self)
        self.__serial = serial.Serial()
        self.__serial.port = comport
        self.__serial.baudrate = baudrate
        self.logname = logname

    def open(self):
        self.__serial.open()
        BaseLogSubject.open(self)

    def close(self):
        BaseLogSubject.close(self)
        self.__serial.close()

    def _notify(self):
        buff = ""
        while not self._should_stop.is_set():
            num_of_bytes = self.__serial.inWaiting()
            if num_of_bytes > 0:
                recv = self.__serial.read(num_of_bytes)
                if self.logname is not None:
                    with open(self.logname, "a") as logfile:
                        logfile.write(recv)
                buff += recv

                if buff.count("\n") > 0:
                    slices = buff.split("\n")
                    lines = slices[:-1]
                    remind = slices[-1]
                    logger.debug("%s CHIP LOG:\n%s",
                                 self.__serial.port,
                                 "\n".join([line.replace("\r", "") for line in lines]))
                    for line in lines:
                        with self._lock:
                            for listener in self._listeners:
                                if listener.keyword is None or listener.keyword in line:
                                    listener.queue.put(line)
                    buff = remind
            time.sleep(0.5)

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.__serial.port)

    def __str__(self):
        return self.__repr__()


class FileLogListener(BaseListener):
    pass


class FileLogSubject(BaseLogSubject):
    Listener = FileLogListener

    def __init__(self, logname):
        BaseLogSubject.__init__(self)
        self.logname = logname

    def _notify(self):
        lineno = 0
        while not self._should_stop.is_set():
            with open(self.logname, "r") as logfile:
                lines = logfile.readlines()

            for index in range(lineno, len(lines)):
                line = lines[index]
                with self._lock:
                    for listener in self._listeners:
                        if listener.keyword in line:
                            listener.queue.put(line)
            lineno = len(lines)
            time.sleep(0.5)

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.logname)

    def __str__(self):
        return self.__repr__()


class QueueLogListener(BaseListener):
    pass


class QueueLogSubject(BaseLogSubject):
    Listener = QueueLogListener

    def __init__(self, queue):
        BaseLogSubject.__init__(self)
        self.queue = queue

    def _notify(self):
        buff = ""
        while not self._should_stop.is_set():
            recv = ""
            try:
                recv = self.queue.get(block=False, timeout=0.5)
                self.queue.task_done()
            except Empty:
                pass
            buff += recv

            if buff.count("\n") > 0:
                slices = buff.split("\n")
                lines = slices[:-1]
                remind = slices[-1]
                logger.debug("CHIP LOG:\n%s", "\n".join([line.replace("\r", "") for line in lines]))
                for line in lines:
                    with self._lock:
                        for listener in self._listeners:
                            if listener.keyword is None or listener.keyword in line:
                                listener.queue.put(line)
                buff = remind

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.queue)

    def __str__(self):
        return self.__repr__()

Event = collections.namedtuple("Event", ["type", "data", "timestamp"])


class _NonBlockingStreamReader(threading.Thread):
    def __init__(self, stream):
        self.__stream = stream
        self.__queue = Queue()
        super(_NonBlockingStreamReader, self).__init__()
        self.start()

    def run(self):
        while True:
            line = self.__stream.readline()
            if line:
                self.__queue.put(line)
            else:
                break

    def readlines_in_buffer(self):
        lines = []
        try:
            qsize = self.__queue.qsize()
            if qsize > 0:
                for _ in range(qsize):
                    line = self.__queue.get_nowait()
                    self.__queue.task_done()
                    lines.append(line.rstrip()+"\n")
        except Empty:
            pass
        finally:
            return lines


class UeventListener(BaseListener):
    pass


class UeventLogSubject(BaseLogSubject):
    Listener = UeventListener

    def __init__(self, exepath, android_serial=None, logname=None):
        BaseLogSubject.__init__(self)
        self.__exepath = exepath
        self.__android_serial = android_serial
        self.__logname = logname
        self.__process = None
        self.__noblocking_stdout = None

    def __str__(self):
        return "<%s(serial:%s, exepath:%s)>" % (self.__class__.__name__, self.__android_serial, self.__exepath)

    @property
    def logname(self):
        return self.__logname

    @logname.setter
    def logname(self, logname):
        logger.debug("Set %s logname to '%s'", self, logname)
        self.__logname = logname
        with open(self.logname, "a") as logfile:
            logfile.write("")

    def open(self):
        logger.info("Start %s", self)
        # if os.path.exists(self.__logname):
        #     os.remove(self.__logname)
        # with open(self.logname, "w") as logfile:
        #     logfile.write("")

        if self.__android_serial:
            cmd = 'adb -s %s shell %s' % (self.__android_serial, self.__exepath)
            logger.debug("run ueventListen with cmd: %s", cmd)
            self.__process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        else:
            self.__process = subprocess.Popen(self.__exepath, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                              shell=False)
        self.__noblocking_stdout = _NonBlockingStreamReader(self.__process.stdout)
        BaseLogSubject.open(self)

    def close(self):
        logger.info("Stop %s" % self)
        BaseLogSubject.close(self)
        try:
            self.__process.terminate()
            self.__process = None
            self.__noblocking_stdout.join()
            self.__noblocking_stdout = None
        except NameError as err:
            logger.error("handle jython error: %s", str(err))
        finally:
            if self.__android_serial:
                os.system('adb -s %s shell "killall ueventListen"' % self.__android_serial)
            else:
                os.system("killall uevent_listen")

    def _notify(self):
        while not self._should_stop.is_set():
            lines = self.__noblocking_stdout.readlines_in_buffer()
            if lines and self.logname is not None:
                with open(self.logname, "a") as logfile:
                    logfile.writelines(lines)

            for index in range(len(lines)):
                matchedEvent = re.search(r"_EVENT=(.*)", lines[index])
                if matchedEvent:
                    try:
                        devent = json.loads(matchedEvent.group(1))
                        matchedTimestamp = re.search(r"\[(\d+)\]", lines[index - 4])
                        timestamp = int(matchedTimestamp.group(1))

                        event = Event(devent["event"], devent["data"], timestamp)
                        with self._lock:
                            for listener in self._listeners:
                                if event.type == listener.keyword:
                                    listener.queue.put(event)
                    except KeyboardInterrupt:
                        raise
                    except (ValueError, TypeError):
                        logger.exception("")
            time.sleep(0.5)


class UeventSocketSubject(BaseLogSubject):
    NETLINK_KOBJECT_UEVENT = 15

    def _notify(self):
        sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, self.NETLINK_KOBJECT_UEVENT)
        try:
            sock.setblocking(0)
            sock.bind((0, 1))
            while not self._should_stop.is_set():
                try:
                    s = sock.recv(4096)
                except socket.error:
                    pass
                else:
                    timestamp = round(time.time(), 3)
                    founds = re.findall(r"_EVENT=(\{.*\})", s)
                    for found in founds:
                        try:
                            devent = json.loads(found)
                            event = Event(devent["event"], devent["data"], timestamp)

                            with self._lock:
                                for listener in self._listeners:
                                    if event.type == listener.keyword:
                                        listener.queue.put(event)
                        except KeyboardInterrupt:
                            raise
                        except (ValueError, TypeError):
                            logger.exception("")
        finally:
            sock.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )