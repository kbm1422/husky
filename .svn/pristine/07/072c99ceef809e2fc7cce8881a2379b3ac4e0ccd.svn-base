#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import time
import random
from ctypes import byref

from base import BaseBostonDriverTestCase, TX_PORT_MAPPER
from simg import fs
from simg.test.framework import name, parametrize, skip, TestContextManager, LinkedTestCase
from simg.devadapter.wired.boston.Sii9777RxLib import *


@name("Sii9777TmdsEnableSet, Sii9777TmdsEnableGet")
@parametrize("tx_port", type=str, choice=TX_PORT_MAPPER.keys())
class TmdsEnableSetTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_golden_tmds_enable_value",
        "test_Sii9777TmdsEnableSet_OFF",
        "test_Sii9777TmdsEnableSet_ON"
    )

    def setUp(self):
        self.__tx_port = Sii9777TxPort_t(TX_PORT_MAPPER[self.tx_port])

        context = TestContextManager.current_context()
        resource = context.resource
        self.webcam = resource.webcam
        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)

    def test_golden_tmds_enable_value(self):
        is_enabled = bool_t()
        with self.device.lock:
            retcode = Sii9777TmdsEnableGet(self.device.drv_instance, self.__tx_port, byref(is_enabled))
        self._test_api_retcode("Sii9777TmdsEnableGet", retcode)
        self.assertTrue(is_enabled.value, msg="Golden TMDS status should be True")

    def test_Sii9777TmdsEnableSet_OFF(self):
        try:
            with self.device.log_subject.listen("TMDS ENABLE=0") as listener:
                expect_is_enabled = bool_t(False)
                with self.device.lock:
                    retcode = Sii9777TmdsEnableSet(self.device.drv_instance, self.__tx_port, byref(expect_is_enabled))
                self._test_api_retcode("Sii9777TmdsEnableSet(OFF)", retcode)

                event = listener.get(timeout=5)
                self.assertIsNotNone(event, "should get log keyword 'TMDS ENABLE=0'")

                actual_is_enabled = bool_t()
                with self.device.lock:
                    retcode = Sii9777TmdsEnableGet(self.device.drv_instance, self.__tx_port, byref(actual_is_enabled))
                self._test_api_retcode("Sii9777TmdsEnableGet(OFF)", retcode)
                self.assertEqual(actual_is_enabled.value, expect_is_enabled.value,
                                 msg="TMDS status should be %s after setting ON" % expect_is_enabled.value)
        finally:
            time.sleep(5)
            capture_image_name = os.path.join(self.capture_image_dir, self.name+"(OFF).jpg")
            self.webcam.capture_image(capture_image_name)

    def test_Sii9777TmdsEnableSet_ON(self):
        try:
            with self.device.log_subject.listen("AVMUTE=0") as listener:
                expect_is_enabled = bool_t(True)
                with self.device.lock:
                    retcode = Sii9777TmdsEnableSet(self.device.drv_instance, self.__tx_port, byref(expect_is_enabled))
                self._test_api_retcode("Sii9777TmdsEnableSet(ON)", retcode)

                event = listener.get(timeout=5)
                self.assertIsNotNone(event, "should get log keyword 'AVMUTE=0'")

                actual_is_enabled = bool_t()
                with self.device.lock:
                    retcode = Sii9777TmdsEnableGet(self.device.drv_instance, self.__tx_port, byref(actual_is_enabled))
                self._test_api_retcode("Sii9777TmdsEnableGet(ON)", retcode)
                self.assertEqual(actual_is_enabled.value, expect_is_enabled.value,
                                 msg="TMDS status should be %s after setting ON" % expect_is_enabled.value)
        finally:
            time.sleep(5)
            capture_image_name = os.path.join(self.capture_image_dir, self.name+"(ON).jpg")
            self.webcam.capture_image(capture_image_name)

@name("Sii9777AvMuteSet, Sii9777AvMuteGet")
@parametrize("tx_port", type=str, choice=TX_PORT_MAPPER.keys())
class AvMuteTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_golden_avmute_value",
        "test_Sii9777AvMuteSet_ON",
        "test_Sii9777AvMuteSet_OFF"
    )

    def setUp(self):
        self.__tx_port = Sii9777TxPort_t(TX_PORT_MAPPER[self.tx_port])

        context = TestContextManager.current_context()
        resource = context.resource
        self.webcam = resource.webcam
        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)
        self.capture_image_name = os.path.join(self.capture_image_dir, self.name+".jpg")

    def test_golden_avmute_value(self):
        is_muted = bool_t()
        with self.device.lock:
            retcode = Sii9777AvMuteGet(self.device.drv_instance, self.__tx_port, byref(is_muted))
        self._test_api_retcode("Sii9777AvMuteGet", retcode)
        self.assertFalse(is_muted.value, msg="Golden AvMute status should be True")

    def test_Sii9777AvMuteSet_ON(self):
        try:
            with self.device.log_subject.listen("AVMUTE=1") as listener:
                expect_is_muted = Sii9777AvMute_t(SII9777_AVMUTE__SET)
                with self.device.lock:
                    retcode = Sii9777AvMuteSet(self.device.drv_instance, self.__tx_port, byref(expect_is_muted))
                self._test_api_retcode("Sii9777AvMuteSet(ON)", retcode)

                event = listener.get(timeout=5)
                self.assertIsNotNone(event, "should get log keyword 'AVMUTE=1' after Sii9777AvMuteSet ON")

                actual_is_muted = Sii9777AvMute_t()
                with self.device.lock:
                    retcode = Sii9777AvMuteGet(self.device.drv_instance, self.__tx_port, byref(actual_is_muted))
                self._test_api_retcode("Sii9777AvMuteGet(ON)", retcode)
                self.assertEqual(actual_is_muted.value, expect_is_muted.value,
                                 msg="AvMute status should be %s" % expect_is_muted.value)
        finally:
            time.sleep(5)
            capture_image_name = os.path.join(self.capture_image_dir, self.name+"(ON).jpg")
            self.webcam.capture_image(capture_image_name)

    def test_Sii9777AvMuteSet_OFF(self):
        try:
            with self.device.log_subject.listen("AVMUTE=0") as listener:
                expect_is_muted = Sii9777AvMute_t(SII9777_AVMUTE__CLEAR)
                with self.device.lock:
                    retcode = Sii9777AvMuteSet(self.device.drv_instance, self.__tx_port, byref(expect_is_muted))
                self._test_api_retcode("Sii9777AvMuteSet(OFF)", retcode)

                event = listener.get(timeout=5)
                self.assertIsNotNone(event, "should get log keyword 'AVMUTE=1' after Sii9777AvMuteSet OFF")

                actual_is_muted = Sii9777AvMute_t()
                with self.device.lock:
                    retcode = Sii9777AvMuteGet(self.device.drv_instance, self.__tx_port, byref(actual_is_muted))
                self._test_api_retcode("Sii9777AvMuteGet(OFF)", retcode)
                self.assertEqual(actual_is_muted.value, expect_is_muted.value,
                                 msg="AvMute status should be %s" % expect_is_muted.value)
        finally:
            time.sleep(5)
            capture_image_name = os.path.join(self.capture_image_dir, self.name+"(OFF).jpg")
            self.webcam.capture_image(capture_image_name)


@name("Sii9777TmdsSwingLevelSet, Sii9777TmdsSwingLevelGet")
@skip("not ready")
class TmdsSwingLevelTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_golden_swing_level",
        "test_Sii9777TmdsSwingLevelSet",
    )

    def tearDown(self):
        pass

    def test_golden_swing_level(self):
        pass

    def test_Sii9777TmdsSwingLevelSet(self):
        pass


@name("Sii9777TmdsPinSwapSet, Sii9777TmdsPinSwapGet")
@skip("not ready")
class TmdsPinSwapTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_golden_swap_pin",
        "test_Sii9777TmdsPinSwapSet",
    )

    def tearDown(self):
        pass

    def test_golden_swap_pin(self):
        pass

    def test_Sii9777TmdsPinSwapSet(self):
        pass


@name("Sii9777PrimTxPortSet, Sii9777PrimTxPortGet")
@parametrize("tx_port", type=str, choice=TX_PORT_MAPPER.keys())
class PrimTxPortTestCase(BaseBostonDriverTestCase):
    """
    Controls which output is defined as primary output port.
    Only the primary output allows HPD and EDID to be replicated to input port(s).
    """
    def setUp(self):
        self.__old_prim_tx_port = Sii9777TxPort_t()
        with self.device.lock:
            Sii9777PrimTxPortGet(self.device.drv_instance, byref(self.__old_prim_tx_port))

        if self.__old_prim_tx_port.value == self.tx_port:
            remain_tx_ports = TX_PORT_MAPPER.values()
            remain_tx_ports.remove(TX_PORT_MAPPER[self.tx_port])
            non_prim_tx_port = Sii9777TxPort_t(random.choice(remain_tx_ports))
            logger.debug("current primary tx port is same with the setting value, change it another value %s" % non_prim_tx_port)
            with self.device.lock:
                Sii9777PrimTxPortSet(self.device.drv_instance, byref(non_prim_tx_port))

    def tearDown(self):
        with self.device.lock:
            Sii9777PrimTxPortSet(self.device.drv_instance, byref(self.__old_prim_tx_port))
        time.sleep(5)

    def test_Sii9777PrimTxPortSet(self):
        expect_prim_tx_port = Sii9777TxPort_t(TX_PORT_MAPPER[self.tx_port])
        with self.device.lock:
            retcode = Sii9777PrimTxPortSet(self.device.drv_instance, byref(expect_prim_tx_port))
            self._test_api_retcode("Sii9777PrimTxPortSet", retcode)

        actual_prim_tx_port = Sii9777TxPort_t()
        with self.device.lock:
            retcode = Sii9777PrimTxPortGet(self.device.drv_instance, byref(actual_prim_tx_port))
            self._test_api_retcode("Sii9777PrimTxPortGet", retcode)
            self.assertEqual(actual_prim_tx_port.value, expect_prim_tx_port.value,
                             msg="Primary TX port should be %s" % expect_prim_tx_port.value)


@name("Sii9777HdcpEnableSet, Sii9777HdcpEnableGet")
@parametrize("tx_port", type=str, choice=("SII9777_TX_PORT__0", "SII9777_TX_PORT__1"))
class HdcpEnableTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_golden_hdcp_enable",
        "test_HdcpEnableSet_ON",
        "test_HdcpEnableSet_OFF"

    )

    def setUp(self):
        self.__port = Sii9777TxPort_t(TX_PORT_MAPPER[self.tx_port])

    def test_golden_hdcp_enable(self):
        is_enabled = bool_t()
        with self.device.lock:
            retcode = Sii9777HdcpEnableGet(self.device.drv_instance, self.__port, byref(is_enabled))
        self._test_api_retcode("Sii9777HdcpEnableGet", retcode)
        self.assertFalse(is_enabled.value, "The golden value of HdcpEnable should be False.")

    def test_HdcpEnableSet_ON(self):
        is_enabled = bool_t(True)
        with self.device.lock:
            retcode = Sii9777HdcpEnableSet(self.device.drv_instance, self.__port, byref(is_enabled))
        self._test_api_retcode("Sii9777HdcpEnableSet", retcode)

        is_enabled = bool_t()
        with self.device.lock:
            Sii9777HdcpEnableGet(self.device.drv_instance, self.__port, byref(is_enabled))
        self.assertTrue(is_enabled.value, "Sii9777HdcpEnableSet true should be successfully.")
        time.sleep(5)

    def test_HdcpEnableSet_OFF(self):
        is_enabled = bool_t(False)
        with self.device.lock:
            retcode = Sii9777HdcpEnableSet(self.device.drv_instance, self.__port, byref(is_enabled))
        self._test_api_retcode("Sii9777HdcpEnableSet", retcode)

        is_enabled = bool_t()
        with self.device.lock:
            Sii9777HdcpEnableGet(self.device.drv_instance, self.__port, byref(is_enabled))
        self.assertFalse(is_enabled.value, "Sii9777HdcpEnableSet true should be successfully.")
        time.sleep(5)

__test_suite__ = {
    "name": "Boston Driver TX HDMI Test Suite",
}