#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import sys
import time
import threading
from .resource import TestResource


class TestContext(object):
    """
    TestContext is a thread local object which used to transmit the data between TestRunner, TestSuite, TestCase and etc
    """
    def __init__(self):
        self.logdir = None
        self.log_level = "DEBUG"
        self.log_layout = "%(asctime)-15s - %(thread)-5d [%(levelname)-8s] - %(message)s"

        # indicate resource name, must be set if enable loop module
        self.rsrcname = None

        # indicate resource object
        # if enable loop module, it would be used by TestLoop
        # otherwise it should be set outside when defining a context
        self.resource = None

        # indicate current running TestSuite, would be used by TestCase. Set by TestSuite.
        self.cursuite = None

    def __getstate__(self):
        keys = ("logdir", "log_level", "log_layout", "rsrcname", "resource")
        d = {}
        for key in keys:
            d[key] = self.__dict__[key]
        return d


class TestContextManager(object):
    @staticmethod
    def getCurrentContext():
        thread = threading.current_thread()
        try:
            return thread.context
        except AttributeError:
            context = TestContext()
            bindir = os.path.dirname(sys.executable) if hasattr(sys, '_MEIPASS') else sys.path[0]
            context.logdir = os.path.join(os.path.dirname(bindir), "logs", time.strftime("%Y-%m-%d_%H-%M-%S"))
            context.resource = TestResource()
            return context

    current_context = getCurrentContext

if __name__ == "__main__":
    pass