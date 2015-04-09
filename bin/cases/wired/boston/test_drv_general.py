#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import time
from ctypes import byref

from base import BaseBostonDriverTestCase, BOOT_STATUS_MAPPER, RX_PORT_MAPPER
from simg import fs
from simg.test.framework import name, parametrize, skip, TestContextManager, LinkedTestCase
from simg.devadapter.wired.boston.Sii9777RxLib import *


class GeneralTestCase(BaseBostonDriverTestCase):
    @name("Sii9777Create")
    def test_Sii9777Create(self):
        self._pass("already been tested when open device adapter.")

    @name("Sii9777Delete")
    def test_Sii9777Delete(self):
        self._pass("already been tested when close device adapter.")

    @name("Sii9777Handle")
    def test_Sii9777Handle(self):
        self._pass("already been tested when open device adapter event subject.")

    @name("Sii9777ChipIdQuery")
    def test_Sii9777ChipIdQuery(self):
        chip_id = uint32_t()
        with self.device.lock:
            retcode = Sii9777ChipIdQuery(self.device.drv_instance, byref(chip_id))
        self.assertEquals(retcode, 0, "Sii9777ChipIdQuery return code should be SII_RETVAL__SUCCESS")
        self.assertEquals(chip_id.value, 0x9777, "The chip id should be 0x9777")

    @name("Sii9777ChipRevisionQuery")
    @parametrize("expect_chip_revision", type=int)
    def test_Sii9777ChipRevisionQuery(self):
        chip_revision = uint32_t()
        with self.device.lock:
            retcode = Sii9777ChipRevisionQuery(self.device.drv_instance, byref(chip_revision))
        self._test_api_retcode("Sii9777ChipRevisionQuery", retcode)
        self.assertEquals(chip_revision.value, self.expect_chip_revision,
                          msg="The chip id should be %d" % self.expect_chip_revision)

    @name("Sii9777ProductIdQuery")
    def test_Sii9777ProductIdQuery(self):
        product_id = uint32_t()
        with self.device.lock:
            retcode = Sii9777ProductIdQuery(self.device.drv_instance, byref(product_id))
        self._test_api_retcode("Sii9777ProductIdQuery", retcode)
        self.assertEquals(product_id.value, 0x9777, "The product id should be 0x9777")

    @name("Sii9777FirmwareVersionQuery")
    @parametrize("expect_firmware_version", type=int)
    def test_Sii9777FirmwareVersionQuery(self):
        actual_firmware_version = uint32_t()
        with self.device.lock:
            retcode = Sii9777FirmwareVersionQuery(self.device.drv_instance, byref(actual_firmware_version))
        self._test_api_retcode("Sii9777FirmwareVersionQuery", retcode)
        self.assertEquals(actual_firmware_version.value, self.expect_firmware_version,
                          msg="The firmware version should be 0X%X" % self.expect_firmware_version)

    @name("Sii9777ReleaseTimeStampQuery")
    def test_Sii9777ReleaseTimeStampQuery(self):
        actual_release_timestamp = uint32_t()
        with self.device.lock:
            retcode = Sii9777ReleaseTimeStampQuery(self.device.drv_instance, byref(actual_release_timestamp))
        self._test_api_retcode("Sii9777ReleaseTimeStampQuery", retcode)
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(actual_release_timestamp.value))
        self._pass("The release timestamp is 0x%x, convert to local_time is %s " % (actual_release_timestamp.value,
                                                                                    local_time))


    @name("Sii9777BootStatusQuery")
    def test_Sii9777BootStatusQuery(self):
        status = Sii9777BootStat_t()
        with self.device.lock:
            retcode = Sii9777BootStatusQuery(self.device.drv_instance, byref(status))
        self._test_api_retcode("Sii9777BootStatusQuery", retcode)
        logger.debug("Current boot status is %s", BOOT_STATUS_MAPPER[status.value])
        self.assertIn(status.value, BOOT_STATUS_MAPPER.keys(),
                      msg="Boot status should in %s" % BOOT_STATUS_MAPPER.values())

    @name("Sii9777EventFlagsMaskSet")
    def test_Sii9777EventFlagsMaskSet(self):
        self._pass("already been tested when open device adapter.")

    @name("Sii9777EventFlagsMaskGet")
    def test_Sii9777EventFlagsMaskGet(self):
        actual_event_flags_mask = uint32_t()
        with self.device.lock:
            retcode = Sii9777EventFlagsMaskGet(self.device.drv_instance, byref(actual_event_flags_mask))
        self._test_api_retcode("Sii9777EventFlagsMaskGet", retcode)
        self.assertEquals(actual_event_flags_mask.value, 0xFFFFFFFF,
                          msg="The event flags mark should be 0xFFFFFFFF")

    @name("Sii9777EventFlagsQuery")
    @skip("TODO")
    def test_Sii9777EventFlagsQuery(self):
        actual_event_flags = uint32_t()
        with self.device.lock:
            retcode = Sii9777EventFlagsQuery(self.device.drv_instance, byref(actual_event_flags))
        self._test_api_retcode("Sii9777EventFlagsQuery", retcode)
        self.assertNotEquals(actual_event_flags.value, 0x00000000L, msg="The event flags should be 0x00000000")


@name("Sii9777ConfigureSet, Sii9777ConfigureGet")
class ConfigureTestCase(BaseBostonDriverTestCase):
    def setUp(self):
        self.__config = Sii9777Config_t()
        with self.device.lock:
            Sii9777ConfigureGet(self.device.drv_instance, byref(self.__config))

    def test_Sii9777ConfigureSet(self):
        expect_config = Sii9777Config_t()
        expect_config.pNameStr = "test-cfg"
        expect_config.bDeviceReset = bool_t(False)
        with self.device.lock:
            retcode = Sii9777ConfigureSet(self.device.drv_instance, byref(expect_config))
        self._test_api_retcode("Sii9777ConfigureSet", retcode)

        actual_config = Sii9777Config_t()
        with self.device.lock:
            retcode = Sii9777ConfigureGet(self.device.drv_instance, byref(actual_config))
        self._test_api_retcode("Sii9777ConfigureGet", retcode)

        self.assertSequenceEqual((actual_config.pNameStr, actual_config.bDeviceReset),
                                 (expect_config.pNameStr, expect_config.bDeviceReset),
                                 msg="The config should be (pNameStr=%s, bDeviceReset=%s)" % (expect_config.pNameStr,
                                                                                              expect_config.bDeviceReset))

    def tearDown(self):
        with self.device.lock:
            Sii9777ConfigureSet(self.device.drv_instance, byref(self.__config))


@name("Sii9777InputSelectSet, Sii9777InputSelectGet(%(rx_port)s)")
@parametrize("rx_port", type=str, choice=RX_PORT_MAPPER.keys())
class InputSelectTestCase(BaseBostonDriverTestCase):
    def setUp(self):
        context = TestContextManager.current_context()
        resource = context.resource
        self.webcam = resource.webcam
        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)
        self.capture_image_name = os.path.join(self.capture_image_dir, self.name+".jpg")

    def test_Sii9777InputSelect(self):
        try:
            expect_rx_port = Sii9777RxPort_t(RX_PORT_MAPPER[self.rx_port])
            with self.device.log_subject.listen("AVMUTE=0") as listener:
                with self.device.lock:
                    retcode = Sii9777InputSelectSet(self.device.drv_instance, byref(expect_rx_port))
                self._test_api_retcode("Sii9777InputSelectSet", retcode)

                event = listener.get(timeout=10)
                self.assertIsNotNone(event, msg="should get log keyword 'AVMUTE=0' in 10s")

            actual_rx_port = Sii9777RxPort_t()
            with self.device.lock:
                retcode = Sii9777InputSelectGet(self.device.drv_instance, byref(actual_rx_port))
            self._test_api_retcode("Sii9777InputSelectGet", retcode)
            self.assertEquals(actual_rx_port.value, expect_rx_port.value,
                              msg="the input port should be %s" % expect_rx_port.value)
            time.sleep(10)
        finally:
            self.webcam.capture_image(self.capture_image_name)


@name("Sii9777StandbyGet, Sii9777StandbySet")
class StandbySetTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_standby_golden_value",
        "test_Sii9777StandbySet_ON",
        "test_Sii9777StandbySet_OFF"
    )

    def setUp(self):
        context = TestContextManager.current_context()
        resource = context.resource
        self.webcam = resource.webcam
        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)

    def test_standby_golden_value(self):
        is_standby = bool_t()
        with self.device.lock:
            retcode = Sii9777StandbyGet(self.device.drv_instance, byref(is_standby))
        self._test_api_retcode("Sii9777StandbyGet", retcode)
        self.assertFalse(is_standby.value, "golden standby should be False")

    def test_Sii9777StandbySet_ON(self):
        self.capture_image_name = os.path.join(self.capture_image_dir, self.name+"(ON).jpg")
        try:
            expect_is_standby = bool_t(True)
            with self.device.lock:
                retcode = Sii9777StandbySet(self.device.drv_instance, byref(expect_is_standby))
            self._test_api_retcode("Sii9777StandbySet", retcode)

            actual_is_standby = bool_t()
            with self.device.lock:
                Sii9777StandbyGet(self.device.drv_instance, byref(actual_is_standby))
            self.assertTrue(actual_is_standby.value, "standby should be True after setting.")
        finally:
            time.sleep(5)
            self.webcam.capture_image(self.capture_image_name)

    def test_Sii9777StandbySet_OFF(self):
        self.capture_image_name = os.path.join(self.capture_image_dir, self.name+"(OFF).jpg")
        try:
            expect_is_standby = bool_t(False)
            with self.device.log_subject.listen("AVMUTE=0") as listener:
                with self.device.lock:
                    retcode = Sii9777StandbySet(self.device.drv_instance, byref(expect_is_standby))
                self._test_api_retcode("Sii9777StandbySet", retcode)
                event = listener.get(timeout=10)
                self.assertIsNotNone(event, "should receive AVMUTE=0 is 5s")
        finally:
            time.sleep(5)
            self.webcam.capture_image(self.capture_image_name)


@skip("TODO")
class GPIOControlTestCase(BaseBostonDriverTestCase):
    @name("Sii9777GpioConfigSet")
    def test_Sii9777GpioConfigSet(self):
        pass

    @name("Sii9777GpioConfigGet")
    def test_Sii9777GpioConfigGet(self):
        pass

    @name("Sii9777GpioOutputSet")
    def test_Sii9777GpioOutputSet(self):
        pass

    @name("Sii9777GpioOutputCl")
    def test_Sii9777GpioOutputClr(self):
        pass

    @name("Sii9777GpioQuery")
    def test_Sii9777GpioQuery(self):
        pass


__test_suite__ = {
    "name": "Boston Driver General Functions Test Suite",
    "subs": [
        GeneralTestCase,
        ConfigureTestCase,
        StandbySetTestCase,
        GPIOControlTestCase
    ]
}