#!/usr/bin/python
# -*- coding: utf-8 -*-


import logging
logger = logging.getLogger(__name__)

import os
import time
import random

from simg.test.framework import TestContextManager

from base import BaseTestCase


class ResetTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager().getCurrentContext()
        self.resobj = context.resobj
        self.srcdut = None
        self.sinkdut = None

    def tearDown(self):
        imgpath = os.path.join(self.logdir, "%s_%s.jpg" % (self.name, self.cycleindex))
        self.resobj.webcam.capImage(imgpath)

    def test_srcreset(self):
        resetTime = time.time()
        self.srcdut.reset()
        self._test_connecttime(self.sinkdut.logname, resetTime)

    def test_sinkreset(self):
        resetTime = time.time()
        self.srcdut.reset()
        self._test_connecttime(self.sinkdut.logname, resetTime)

    def test_fixedreset(self):
        self.srcdut.reset()
        resetTime = time.time()
        self.sinkdut.reset()
        self._test_connecttime(self.sinkdut.logname, resetTime)

    def test_randomseqreset(self):
        devs = random.shuffle([self.srcdut, self.sinkdut])
        devs[0].reset()
        resetTime = time.time()
        devs[1].reset()
        self._test_connecttime(self.sinkdut.logname, resetTime)

    def test_variablereset(self):
        self.srcdut.reset()
        time.sleep(0.5 * self.cycleindex)
        resetTime = time.time()
        self.sinkdut.reset()
        self._test_connecttime(self.sinkdut.logname, resetTime)

    def test_nvramsetdefaultreset(self):
        self.srcdut.sendcmd("nvram_set_defaults")
        self.sinkdut.sendcmd("nvram_set_defaults")
        resetTime = time.time()
        self.srcdut.reset()
        self.sinkdut.reset()
        self._test_connecttime(self.sinkdut.logname, resetTime)

    def test_nvramsetdefaultresetsrc(self):
        self.srcdut.sendcmd("nvram_set_defaults")
        resetTime = time.time()
        self.srcdut.reset()
        self._test_connecttime(self.sinkdut.logname, resetTime)

    def test_nvramsetdefaultresetsink(self):
        self.sinkdut.sendcmd("nvram_set_defaults")
        resetTime = time.time()
        self.sinkdut.reset()
        self._test_connecttime(self.sinkdut.logname, resetTime)

if __name__ == "__main__":
    pass
