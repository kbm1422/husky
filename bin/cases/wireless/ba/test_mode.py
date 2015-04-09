import logging
logger = logging.getLogger(__name__)

import time
from .base import BaseTestCase
from simg.test.framework import TestContextManager


class ModeOffChangeToOtherTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager.getCurrentContext()
        self.txunit, self.rxunit = context.resource.acquire_pair()
        logger.debug("Before test, change mode to off first")
        self.make_mode(self.txunit, "off")

    def test__off_to_wihd(self):
        self._test_mode(self.txunit, "wihd")
        time.sleep(1)
        self._test_mode(self.txunit, "off")

    def test__off_to_mhl(self):
        self._test_mode(self.txunit, "mhl")
        time.sleep(1)
        self._test_mode(self.txunit, "off")

    def test__wihd_to_mhl(self):
        self._test_mode(self.txunit, "wihd")
        time.sleep(1)
        self._test_mode(self.txunit, "mhl")


class WihdScanToOtherModeTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager.getCurrentContext()
        self.txunit, self.rxunit = context.resource.acquire_pair()
        self.make_mode(self.txunit, "wihd")
        self.txunit.device.stop_scan()
        self.txunit.device.setMacAddress("11:22:33:44:55:66")

        logger.debug("Before test, make sure it is in scan state")
        duration = 20
        attempts = 3
        for i in range(attempts):
            try:
                self.make_scan(duration, interval=0, uevent_listen_timeout=3)
            except self.failureException:
                logger.exception("")
                if i != attempts - 1:
                    logger.debug("scan failed, current try times is %s, retry scan.", duration, i)
                    continue
                else:
                    logger.debug("scan try times is reach the max attempt count, stop retry.", duration, i)
                    raise
            else:
                break

    def test__scan_to_off(self):
        self._test_mode(self.txunit, "off")

    def test__scan_to_mhl(self):
        self._test_mode(self.txunit, "mhl")


class WihdAssociatedToOtherModeTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager.getCurrentContext()
        self.txunit, self.rxunit = context.resource.acquire_pair()
        self.make_mode(self.txunit, "wihd")
        self.make_disassociated(self.txunit)
        self.txunit.device.setMacAddress("11:22:33:44:55:66")
        self.make_associated(self.txunit, self.rxunit)

    def test__associated_to_off(self):
        self._test_mode(self.txunit, "off")

    def test__associated_to_mhl(self):
        self._test_mode(self.txunit, "mhl")


class WihdConnectedToOtherModeTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager.getCurrentContext()
        self.txunit, self.rxunit = context.resource.acquire_pair()
        self.make_mode(self.txunit, "wihd")
        self.make_disassociated(self.txunit)
        self.txunit.device.setMacAddress("11:22:33:44:55:66")
        self.make_connected(self.txunit, self.rxunit)

    def test__connected_to_off(self):
        self._test_mode(self.txunit, "off")

    def test__connected_to_mhl(self):
        self._test_mode(self.txunit, "mhl")


__test_suite__ = {
    "name": "BA Driver Mode Change Test Suite",
    "subs": [
        ModeOffChangeToOtherTestCase.test__off_to_wihd,
        ModeOffChangeToOtherTestCase.test__off_to_mhl,
        ModeOffChangeToOtherTestCase.test__wihd_to_mhl,

        WihdScanToOtherModeTestCase.test__scan_to_off,
        WihdScanToOtherModeTestCase.test__scan_to_mhl,

        WihdAssociatedToOtherModeTestCase.test__associated_to_off,
        WihdAssociatedToOtherModeTestCase.test__associated_to_mhl,

        WihdConnectedToOtherModeTestCase.test__connected_to_off,
        WihdConnectedToOtherModeTestCase.test__connected_to_mhl,
    ]
}