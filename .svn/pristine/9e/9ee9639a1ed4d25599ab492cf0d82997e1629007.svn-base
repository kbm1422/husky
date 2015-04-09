#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import time

from simg.devadapter.wired.base import MscMessage, Mhl2Interface
from simg.test.framework import TestCase, skip, parametrize, TestContextManager


"""
RCP: Remote Control Protocol


RAP: Request Action Protocol
    0x00 – POLL
    0x10 – CONTENT_ON
    0x11 – CONTENT_OFF
    0x20 – CBUS_MODE_DOWN request to change from eCBUS mode to MHL1/MHL2 mode
    0x21 – CBUS_MODE_UP request to change from MHL1/MHL2 mode to eCBUS mode

UCP: UTF-8 Character Protocol
"""

RCP = 0x10
RCPK = 0x11
RCPE = 0x12

RAP = 0x20
RAPK = 0x21

UCP = 0x30
UCPK = 0x31
UCPE = 0x32

RAP_STATUS_CODE__NO_ERROR = 0x00
RAP_STATUS_CODE__UNRECOGNIZED_ACTION_CODE = 0x01
RAP_STATUS_CODE__UNSUPPORTED_ACTION_CODE = 0x02
RAP_STATUS_CODE__RESPONDER_BUSY = 0x03

RCP_STATUS_CODE__NO_ERROR = 0x00
RCP_STATUS_CODE__INEFFECTIVE_KEY_CODE = 0x01
RCP_STATUS_CODE__RESPONDER_BUSY = 0x02

UCP_STATUS_CODE__NO_ERROR = 0x00
UCP_STATUS_CODE__INEFFECTIVE_KEY_CODE = 0x01


RCP_SUPPORTED_KEY_CODES = [
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x09, 0x0D,
    0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2B, 0x2C,
    0x33, 0x44, 0x45, 0x46, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x60, 0x61, 0x64
]

RCP_RESERVED_KEY_CODES = [
    0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B,
    0x1C, 0x1D, 0x1E, 0x1F, 0x2D, 0x2E, 0x2F, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3F, 0x40, 0x52, 0x53,
    0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x67, 0x69, 0x6A, 0x6B,
    0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7F
]

UCP_RESERVED_CODES = [
    192, 193, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255
]

UCP_SUPPORTED_CODES = range(0, 256)


@parametrize("peer_device", type=Mhl2Interface, fetch=parametrize.FetchType.LAZY)
@parametrize("device", type=Mhl2Interface, fetch=parametrize.FetchType.LAZY)
class Mhl2MscMessageSendTestCase(TestCase):
    @parametrize("rap_code", type=int, iteration=[0x00, 0x10, 0x11])
    def test_rap_supported(self):
        try:
            expect_rap_msg = MscMessage(RAP, self.rap_code)
            self.device.send_msc_message(expect_rap_msg)
            time.sleep(3)
            actual_rap_msg = self.peer_device.recv_msc_message()
            self.assertEqual(actual_rap_msg, expect_rap_msg,
                             "peer device should receive rap %s, actual is %s" % (expect_rap_msg, actual_rap_msg))

            expect_rapk_msg = MscMessage(RAPK, RAP_STATUS_CODE__NO_ERROR)
            actual_rapk_msg = self.device.recv_msc_message()
            self.assertEqual(actual_rapk_msg, expect_rapk_msg,
                             "dut should receive rapk %s, actual is %s" % (expect_rapk_msg, actual_rapk_msg))
        finally:
            self.peer_device.send_rap(0x10)

    @parametrize("rcp_code", type=int, iteration=RCP_SUPPORTED_KEY_CODES)
    def test_rcp_supported(self):
        expect_rcp_msg = MscMessage(RCP, self.rcp_code)
        self.device.send_msc_message(expect_rcp_msg)
        time.sleep(3)

        actual_rcp_msg = self.peer_device.recv_msc_message()
        self.assertEqual(actual_rcp_msg, expect_rcp_msg,
                         "peer device should receive rcp %s, actual is %s" % (expect_rcp_msg, actual_rcp_msg))

        expect_rcpk_msg = MscMessage(RCPK, self.rcp_code)
        actual_rcpk_msg = self.device.recv_msc_message()
        self.assertEqual(actual_rcpk_msg, expect_rcpk_msg,
                         "dut should receive rcpk %s, actual is %s" % (expect_rcpk_msg, actual_rcpk_msg))

    @skip("sometimes the device receive rcpk directly, can't recv rcpe")
    @parametrize("rcp_code", type=int, iteration=RCP_RESERVED_KEY_CODES)
    def test_rcp_reserved(self):
        expect_rcp_msg = MscMessage(RCP, self.rcp_code)
        self.device.send_msc_message(expect_rcp_msg)

        expect_rcpe_msg = MscMessage(RCPE, RCP_STATUS_CODE__INEFFECTIVE_KEY_CODE)
        actual_rcpe_msg = self.device.recv_msc_message()
        self.assertEqual(actual_rcpe_msg, expect_rcpe_msg,
                         "dut should receive rcpe %s, actual is %s" % (expect_rcpe_msg, actual_rcpe_msg))
        time.sleep(5)
        expect_rcpk_msg = MscMessage(RCPK, self.rcp_code)
        actual_rcpk_msg = self.device.recv_msc_message()
        self.assertEqual(actual_rcpk_msg, expect_rcpk_msg,
                         "dut should receive rcpk %s, actual is %s" % (expect_rcpk_msg, actual_rcpk_msg))

    @parametrize("ucp_code", type=int, iteration=UCP_SUPPORTED_CODES)
    def test_ucp(self):
        expect_ucp_msg = MscMessage(UCP, self.ucp_code)
        self.device.send_msc_message(expect_ucp_msg)
        time.sleep(3)

        actual_ucp_msg = self.peer_device.recv_msc_message()
        self.assertEqual(actual_ucp_msg, expect_ucp_msg,
                         "peer device should receive ucp %s, actual is %s" % (expect_ucp_msg, actual_ucp_msg))

        expect_ucpk_msg = MscMessage(UCPK, self.ucp_code)
        actual_ucpk_msg = self.device.recv_msc_message()
        self.assertEqual(actual_ucpk_msg, expect_ucpk_msg,
                         "dut should receive ucpk %s, actual is %s" % (expect_ucpk_msg, actual_ucpk_msg))


@parametrize("peer_device", type=Mhl2Interface, fetch=parametrize.FetchType.LAZY)
@parametrize("device", type=Mhl2Interface, fetch=parametrize.FetchType.LAZY)
class Mhl2MscMessageRecvTestCase(TestCase):
    pass