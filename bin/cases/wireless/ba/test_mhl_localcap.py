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


class MHLLocalCapTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager().getCurrentContext()
        self.txunit, self.rxunit = context.resource.acquire_pair()
        logger.debug("Before test, change mode to mhl first")
        self.make_mode(self.txunit, "mhl")

    @parametrize("localoffset", type=int, iteration=random.sample(range(0x0F), 15))
    @parametrize("local", type=int, iteration=random.sample(range(0xFF), 10))
    def test_local_capabilities_write_read(self):
        """ should set localoffset(0x00-0x0f address) firstly ,then set local(0x00-0xFF)value,
        sometimes we choose local with random 10 times to test every localoffset
        """
        self.name = "localoffset is 0x%02X and local is 0x%02X" % (self.localoffset, self.local)
        logger.debug("current write support local cap offset is 0%#X" % self.localoffset)
        resp1 = self.txunit.device.setMHLLocalCapOffset(self.localoffset)
        self.assertFalse(resp1, "should set local cap offset successful and return value is 0 or none")
        time.sleep(0.5)
        resp2 = self.txunit.device.getMHLLocalCapOffset()
        self.assertEqual(hex(self.localoffset), hex(int(resp2, 10)), "shoule get local cap offset is same as setting value 0x%02X" % self.localoffset)

        resp3 = self.txunit.device.setMHLLocalCap(hex(self.local))
        time.sleep(0.5)
        self.assertFalse(resp3, "should set local cap succesful and return value is 0 or none ")
        resp4 = self.txunit.device.getMHLLocalCap()
        time.sleep(0.5)
        self.assertEqual(hex(self.local), hex(int(resp4, 16)), "shoule get local cap  is same as setting value 0x%02X" % self.local)


    @parametrize("unsupportlocaloffset", type=int, iteration=random.sample(range(0x10, 0xFF), 10))
    def test_localoffset_capabilites_unsupport_write_read(self):
        self.name = "unsupportlocalOffset is 0x%02X " % self.unsupportlocaloffset
        logger.debug("current write unsupport local cap offset is 0x%02x" % self.unsupportlocaloffset)
        resp1 = self.txunit.device.setMHLLocalCapOffset(self.unsupportlocaloffset)
        time.sleep(0.5)
        self.assertFalse(resp1, "should set remote cap offset unsuccessful and return value is none ")
        logger.debug("now get current  remote cap offset ")
        resp2 = self.txunit.device.getMHLLocalCapOffset()
        self.assertIn(int(resp2,10),range(16), "shoule get remote cap value is between 0x00 and  0xFF,current is 0x%02x" % int(resp2,10))

    @parametrize("unsupportlocal", type=int, iteration=random.sample(range(256, 65535), 10))
    def test_local_capabilites_unsupport_write_read(self):
        self.name = "unsupportlocal is 0x%02X " % self.unsupportlocal
        logger.debug("current write unsupport local cap offset is 0x%02x" % self.unsupportlocal)
        resp1 = self.txunit.device.setMHLLocalCap(self.unsupportlocal)
        time.sleep(0.5)
        self.assertFalse(resp1, "should set remote cap offset unsuccessful and return value is none ")
        logger.debug("now get current  remote cap offset ")
        resp2 = self.txunit.device.getMHLLocalCap()
        self.assertIn(int(resp2,16),range(256), "shoule get remote cap value is between 0x00 and  0xFF,current is 0x%02x" % int(resp2,16))

    def tearDown(self):
        self.txunit.device.setMHLLocalCap("0x00")
        self.txunit.device.setMHLLocalCapOffset("0x00")











