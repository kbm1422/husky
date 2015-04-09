#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import inspect
import thread
import threading


class ThreadIdentFilter(logging.Filter):
    def __init__(self, ident=None):
        logging.Filter.__init__(self)
        self.ident = ident or thread.get_ident()

    def filter(self, record):
        return True if record.thread == self.ident else False


class ThreadNameFilter(logging.Filter):
    def __init__(self, name=None):
        logging.Filter.__init__(self)
        self.name = name or threading.current_thread().name

    def filter(self, record):
        return True if record.threadName == self.name else False


class ObjectModuleThreadIdentFilter(ThreadIdentFilter):
    def __init__(self, obj, modulename):
        ThreadIdentFilter.__init__(self)
        self.obj = obj
        self.modulename = modulename

    def filter(self, record):
        if ThreadIdentFilter.filter(self, record) and (record.name == inspect.getmodule(self.obj).__name__ or self.modulename in record.name):
            return True
        else:
            return False


class ObjectModuleThreadNameFilter(ThreadNameFilter):
    def __init__(self, obj, modulename, threadname=None):
        ThreadNameFilter.__init__(self, name=threadname)
        self.obj = obj
        self.modulename = modulename

    def filter(self, record):
        if ThreadNameFilter.filter(self, record) and (record.name == inspect.getmodule(self.obj).__name__ or self.modulename in record.name):
            return True
        else:
            return False

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.NOTSET,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )
