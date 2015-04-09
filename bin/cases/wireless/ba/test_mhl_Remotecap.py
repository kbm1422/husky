#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

#B&A mhl ID impedance test suite
#Include cases: localoffset_write_read and localcap_write_read,
#Note: before test, make sure B&A has connected with Linux PC thru USB cable, driver has been installed

import logging
logger = logging.getLogger(__name__)

import time
from .base import BaseTestCase
from simg.test.framework import TestContextManager, parametrize
import random


class MHLRemoteCapTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager().getCurrentContext()
        self.txunit, self.rxunit = context.resource.acquire_pair()
        logger.debug("Before test, change mode to mhl first")
        self.make_mode(self.txunit, "mhl")

    @parametrize("remoteoffset", type=int, iteration=random.sample(range(0x0F),15))
    @parametrize("remote", type=int, iteration=random.sample(range(0xFF), 10))
    def test_remote_capabilities_write_read(self):
        """ should set Remoteoffset(0x00-0x0f address) firstly ,then set remote (0x00-0xFF)value
        sometimes we choose remote with random 10 times to test every remoteoffset
        """
        self.name = "remoteOffset is 0x%02X and remote is 0x%2X" % (self.remoteoffset, self.remote)
        logger.debug("current write support remote cap offset is 0x%2x" % self.remoteoffset)
        resp1 = self.txunit.device.setMHLRemoteCapOffset(self.remoteoffset)
        self.assertFalse(resp1, "should set remote cap offset successful and return value is 0 or none")
        time.sleep(0.5)
        resp2 = self.txunit.device.getMHLRemoteCapOffset()
        self.assertEqual(hex(self.remoteoffset), hex(int(resp2, 10)), "shoule get remote cap offset is same as setting value 0x%02X" % self.remoteoffset)

        resp3 = self.txunit.device.setMHLRemoteCap(hex(self.remote))
        time.sleep(0.5)
        self.assertRegexpMatches(resp3, ".*Permission denied", "should not set remote and feeback is Permission denied ")
        resp4 = self.txunit.device.getMHLRemoteCap()
        time.sleep(0.5)
        self.assertIn(int(resp4,16),range(0xFF), "shoule get remote cap value is between 0x00 and  0xFF,current is 0x%02x" % int(resp4,16))

    @parametrize("unsupportremoteoffset", type=int, iteration=random.sample(range(0x10, 0xFF), 10))
    def test_remote_capabilites_unsupport_write_read(self):
        self.name = "unsupportremoteOffset is 0x%02X " % self.unsupportremoteoffset
        logger.debug("current write unsupport remote cap offset is 0x%02x" % self.unsupportremoteoffset)
        resp1 = self.txunit.device.setMHLRemoteCapOffset(self.unsupportremoteoffset)
        time.sleep(0.5)
        self.assertFalse(resp1, "should set remote cap offset unsuccessful and return value is none ")
        logger.debug("now get current  remote cap offset ")
        resp2 = self.txunit.device.getMHLRemoteCapOffset()
        self.assertIn(int(resp2,10),range(16), "shoule get remote cap value is between 0x00 and  0xFF,current is 0x%02x" % int(resp2,10))






    def tearDown(self):
        self.txunit.device.setMHLRemoteCap("0x00")
        self.txunit.device.setMHLRemoteCapOffset("0x00")











