#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from base import BaseBostonDriverTestCase
from simg.test.framework import parametrize, skip


@skip("the firmware has already been updated before doing test")
@parametrize("upgrade_firmware_filename")
class FirmwareUpdateTestCase(BaseBostonDriverTestCase):
    def test_firmware_update(self):
        self.device.update_firmware(self.upgrade_firmware_filename)
        # self.device.psoutlet.cycle()
        # time.sleep(20)
        # self.device.close()
        # self.device.open()

    @skip("not ready")
    def test_edid_update(self):
        pass

__test_suite__ = {
    "name": "Boston Driver Flash Test Suite",
}