#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from base import BaseBostonDriverTestCase
from simg.devadapter.wired.base import Mhl3Interface
from simg.test.framework import parametrize, skip, LinkedTestCase, TestContextManager
from simg.devadapter.wired.boston.Sii9777RxLib import *
from test_drv_rx_mhl_common import *


# FIXME: will cause conflict when mul-threads TestRunner
parametrize("expect_cd_sense", default="SII9777_CD_SENSE__MHL_CABLE")(RxCdSenseQueryTestCase)
parametrize("expect_mhl_version", default="SII9777_MHL_VERSION__MHL3")(MHLVersionQueryTestCase)
parametrize("expect_cbus_mode", default="SII9777_CBUS_MODE__ECBUS_S")(CbusModeQueryTestCase)


@skip("TODO")
class CbusEventQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777CbusEventQuery(self):
        pass


# @parametrize("peer_device", type=Mhl3Interface, fetch=parametrize.FetchType.LAZY)
class CbusLocalXDevcapTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = ("test_golden_local_x_devcap",
                   "test_Sii9777CbusLocalXDevcapSet")

    GOLDEN_LOCAL_X_DEVCAP = [0x03, 0x07, 0x02, 0x00]

    def tearDown(self):
        self.device.set_local_x_devcap(self.GOLDEN_LOCAL_X_DEVCAP)

    def test_golden_local_x_devcap(self):
        pData = (uint8_t * 4)()
        offset = uint8_t(0)
        length = uint8_t(4)

        with self.device.lock:
            retcode = Sii9777CbusLocalXDevcapGet(self.device.drv_instance, pData, offset, length)
        self._test_api_retcode("Sii9777CbusLocalXDevcapGet", retcode)

        actual_local_x_devcap = [pData[index] for index in range(4)]
        self.assertSequenceEqual(actual_local_x_devcap, self.GOLDEN_LOCAL_X_DEVCAP,
                                 "should get the same devcap as golden local x devcap")

    def test_Sii9777CbusLocalXDevcapSet(self):
        expect_local_x_devcap = (0x01, 0x07, 0x17, 0x01)
        pData = (uint8_t * 4)()
        for i in range(4):
            pData[i] = expect_local_x_devcap[i]
        offset = uint8_t(0)
        length = uint8_t(4)
        with self.device.lock:
            retcode = Sii9777CbusLocalXDevcapSet(self.device.drv_instance, pData, offset, length)
        self._test_api_retcode("Sii9777CbusLocalXDevcapSet", retcode)

        actual_local_x_devcap = self.device.get_local_x_devcap()
        self.assertSequenceEqual(actual_local_x_devcap, expect_local_x_devcap,
                                 "should get the same devcap as expect local x devcap")


@parametrize("peer_device", type=Mhl3Interface, fetch=parametrize.FetchType.LAZY)
class CbusRemoteXDevcapQueryTestCase(BaseBostonDriverTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Sii9777CbusRemoteXDevcapQuery(self):
        pData = (uint8_t * 4)()
        offset = uint8_t(0)
        length = uint8_t(4)

        with self.device.lock:
            retcode = Sii9777CbusRemoteXDevcapQuery(self.device.drv_instance, pData, offset, length)
        self._test_api_retcode("Sii9777CbusRemoteXDevcapQuery", retcode)
        actual_remote_x_devcap = [pData[index] for index in range(4)]

        expect_remote_x_devcap = self.peer_device.get_local_x_devcap()
        self.assertSequenceEqual(actual_remote_x_devcap, expect_remote_x_devcap,
                                 "the remote x devcap should be %s" % expect_remote_x_devcap)


@skip("TODO")
class CbusBurstSendReceiveTestCase(BaseBostonDriverTestCase):
    def test_CbusBurstSendReceive(self):
        self.assertEqual(self.data_from_send, self.data_from_receive,
                         "The value gotten from sent is same as the value received manually.")

    def _send(self):
        pData = uint8_t()
        offset = uint8_t()
        length = uint8_t()

        with self.device.lock:
            retcode = Sii9777CbusBurstSend(self.device.drv_instance, pData, offset, length)

        self._test_api_retcode("Sii9777CbusBurstSend", retcode)

        self.data_from_send = pData

    def _receive(self):
        pData = uint8_t()
        offset = uint8_t()
        length = uint8_t()

        with self.device.lock:
            retcode = Sii9777CbusBurstReceive(self.device.drv_instance, pData, offset, length)

        self._test_api_retcode("Sii9777CbusBurstReceive", retcode)

        self.data_from_receive = pData


__test_suite__ = {
    "name": "Boston Driver RX MHL3 Test Suite"
}