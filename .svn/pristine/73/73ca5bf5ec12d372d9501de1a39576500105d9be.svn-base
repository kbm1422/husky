#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import time

from simg.devadapter.wired.base import MscMessage, Mhl3Interface
from simg.test.framework import parametrize, TestContextManager
from test_mhl2_msc_msg import Mhl2MscMessageSendTestCase

"""
RBP: Remote Button Protocol
"""

RBP = 0x22
RBPK = 0x23
RBPE = 0x24

RBP_STATUS_CODE__NO_ERROR = 0x00
RBP_STATUS_CODE__INEFFECTIVE_BUTTON_CODE = 0x01
RBP_STATUS_CODE__RESPONDER_BUSY = 0x02

RBP_SUPPORTED_CODES = [
    0x0, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x20, 0x21, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35
]

RBP_RESERVED_CODES = list(set(range(256))-set(RBP_SUPPORTED_CODES))


@parametrize("peer_device", type=Mhl3Interface, fetch=parametrize.FetchType.LAZY)
@parametrize("device", type=Mhl3Interface, fetch=parametrize.FetchType.LAZY)
class Mhl3MscMessageSendTestCase(Mhl2MscMessageSendTestCase):
    @parametrize("rbp_code", type=int, iteration=RBP_SUPPORTED_CODES)
    def test_msc_msg_rbp_supported(self):
        expect_rbp_msg = MscMessage(RBP, self.rbp_code)
        self.device.send_msc_message(expect_rbp_msg)
        time.sleep(3)

        actual_rbp_msg = self.peer_device.recv_msc_message()
        self.assertEqual(actual_rbp_msg, expect_rbp_msg,
                         "peer device should receive rbp %s, actual is %s" % (expect_rbp_msg, expect_rbp_msg))

        expect_rbpk_msg = MscMessage(RBPK, self.rbp_code)
        actual_rbpk_msg = self.device.recv_msc_message()
        self.assertEqual(actual_rbpk_msg, expect_rbpk_msg,
                         "dut should receive rbpk %s, actual is %s" % (expect_rbpk_msg, actual_rbpk_msg))

    @parametrize("rbp_code", type=int, iteration=RBP_RESERVED_CODES)
    def test_msc_msg_rbp_reserved(self):
        self.device.send_msc_message(MscMessage(RBP, self.rbp_code))
        time.sleep(3)

        expect_rbpe_msg = MscMessage(RBPE, RBP_STATUS_CODE__INEFFECTIVE_BUTTON_CODE)
        actual_rbpe_msg = self.device.recv_msc_message()
        self.assertEqual(actual_rbpe_msg, expect_rbpe_msg,
                         "dut should receive rbpe %s, actual is %s" % (expect_rbpe_msg, actual_rbpe_msg))

        expect_rbpk_msg = MscMessage(RBPK, self.rbp_code)
        actual_rbpk_msg = self.device.recv_msc_message()
        self.assertEqual(actual_rbpk_msg, expect_rbpk_msg,
                         "dut should receive rbpk %s, actual is %s" % (expect_rbpk_msg, actual_rbpk_msg))
