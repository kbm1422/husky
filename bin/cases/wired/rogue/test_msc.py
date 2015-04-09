#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import random
import time

from simg.devadapter.wired.rogue import RogueHostAdapter
from simg.devadapter.wired.wolverine60 import Wolverine60DeviceAdapter
from simg.test.framework import TestCase, parametrize, TestContextManager


@parametrize("device_wolverine60", type=Wolverine60DeviceAdapter, fetch=parametrize.FetchType.LAZY)
@parametrize("device_rogue", type=RogueHostAdapter, fetch=parametrize.FetchType.LAZY)
@parametrize("listen_timeout", type=float, default=3.0)
class MscTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        self.device_wolverine60.rap(0x10)

    def test_msc_rap(self):
        rap_key = [0x10, 0x11]
        key = random.choice(rap_key)
        data = (hex(key))[2:] if len((hex(key))[2:]) > 1 else (hex(key))[2:] + "0"
        listen_keyword1 = "Received sub-command >> RAP(Data 0x%s)" % data
        listen_keyword2 = "Send sub-command >> RAPK(Data 0x00)"
        listener1 = self.device_rogue.log_subject.listen(listen_keyword1)
        listener2 = self.device_rogue.log_subject.listen(listen_keyword2)

        self.device_wolverine60.send_rap(key)
        time.sleep(3)
        event1 = listener1.get(timeout=self.listen_timeout)
        self.assertIsNotNone(event1, msg="should get Received sub-command >> RAP(Data 0x%s)" % data)
        event2 = listener2.get(timeout=self.listen_timeout)
        self.assertIsNotNone(event2, msg="should get RAPK Data 0x00")

        self.device_rogue.log_subject.detach(listener1)
        self.device_rogue.log_subject.detach(listener2)

    def test_msc_rcp(self):
        rcp_key = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x41, 0x42, 0x43,
                   0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x50, 0x51, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25,
                   0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x30,
                   0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x71, 0x72, 0x73, 0x74, 0x75, 0x7E]
        key = random.choice(rcp_key)
        data = (hex(key))[2:] if len((hex(key))[2:]) > 1 else "0" + (hex(key))[2:]
        listen_keyword1 = "Received sub-command >> RCP(Data 0x%s)" % data
        listen_keyword2 = "Send sub-command >> RCPK(Data 0x%s)" % data
        listener1 = self.device_rogue.log_subject.listen(listen_keyword1)
        listener2 = self.device_rogue.log_subject.listen(listen_keyword2)

        self.device_wolverine60.send_rcp(key)
        time.sleep(5)
        event1 = listener1.get(timeout=self.listen_timeout)
        self.assertIsNotNone(event1, msg="should get Received sub-command >> RCP(Data 0x%s)" % data)
        event2 = listener2.get(timeout=self.listen_timeout)
        self.assertIsNotNone(event2, msg="should get RCPK >> RCPK (Data 0x%s)" % data)

        self.device_rogue.log_subject.detach(listener1)
        self.device_rogue.log_subject.detach(listener2)

    def test_msc_rcp_reserved(self):
        rcp_key = [0x40, 0x4D, 0x4E, 0x4F, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A,
                   0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C,
                   0x5D, 0x5E, 0x5F, 0x69, 0x6A, 0x2D, 0x2E, 0x2F, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x7F, 0x39, 0x3A,
                   0x3B, 0x3C, 0x3D, 0x3E, 0x3F]

        key = random.choice(rcp_key)

        #receiver will send RCPE to sender if accept unsupported key ,so observe wolverine logs
        with self.device_wolverine60.log_subject.listen("Received an RCPE = 01") as listener:
            self.device_wolverine60.send_rcp(key)
            time.sleep(3)
            event = listener.get(timeout=self.listen_timeout)
            self.assertIsNotNone(event, msg="should get Received RCPE 01")

    def test_msc_ucp(self):
        ucp_key = []
        for n in range(0, 256):
            ucp_key.append(n)
        while 1:
            key = random.choice(ucp_key)

            #From Unicode Standard, Version 6.0.0, page 94:following byte values are disallowed in UTF-8: C0–C1, F5–FF.
            if key in (192, 193, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255):
                continue
            else:
                data = "0x"+"%02x" % key
                listen_keyword1 = "Received sub-command >> UCP(Data %s)" % data
                listen_keyword2 = "Send sub-command >> UCPK(Data %s)" % data
                listener1 = self.device_rogue.log_subject.listen(listen_keyword1)
                listener2 = self.device_rogue.log_subject.listen(listen_keyword2)
                self.device_rogue.log_subject.attach(listener1)
                self.device_rogue.log_subject.attach(listener2)
                self.device_wolverine60.send_ucp(key)
                time.sleep(3)
                event1 = listener1.get(timeout=self.listen_timeout)
                self.assertIsNotNone(event1, msg="should get Received sub-command >> UCP(Data %s)" % data)
                event2 = listener2.get(timeout=self.listen_timeout)
                self.assertIsNotNone(event2, msg="should get UCPK >> UCPK (Data %s)" % data)
                self.device_rogue.log_subject.detach(listener1)
                self.device_rogue.log_subject.detach(listener2)
                break
