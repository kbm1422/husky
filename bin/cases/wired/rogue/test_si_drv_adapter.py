#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import time
import unittest
from ctypes import *
from simg.devadapter.wired.rogue.api import *
from base import BaseSiiDrvAdaptTestCase


class SiiDrvAdaptCreateTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptCreate(self):
        self.assertTrue(1)


class SiiDrvAdaptDeleteTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdatDelete(self):
        self.assertTrue(1)


class SiiDrvAdaptConfigureTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptConfigure(self):
        self.assertTrue(1)


class SiiDrvAdaptStartTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptStart(self):
        self.assertTrue(1)


class SiiDrvAdaptStopTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptStop(self):
        self.assertTrue(1)


class SiiDrvAdaptTaskExecuteTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptTaskExecute(self):
        self.assertTrue(1)


class SiiDrvAdaptBootStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptBootStatusGet(self):
        boot_status = SiiDrvAdaptBootStatus_t()
        boot_status_mapping = {SII_DRV_ADAPTER_BOOTING__FAILURE: "SII_DRV_ADAPTER_BOOTING__FAILURE",
                               SII_DRV_ADAPTER_BOOTING__IN_PROGRESS: "SII_DRV_ADAPTER_BOOTING__IN_PROGRESS",
                               SII_DRV_ADAPTER_BOOTING__SUCCESS: "SII_DRV_ADAPTER_BOOTING__SUCCESS"}
        SiiDrvAdaptBootStatusGet(self.device.sii_instance, byref(boot_status))
        self.assertIn(boot_status.value, boot_status_mapping.keys(),
                      msg="Adapter boot status should be in %s" % boot_status_mapping.values())
        logger.debug("Adatper boot status: %s" % boot_status_mapping[boot_status.value])


class SiiDrvAdaptVersionGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptVersionGet(self):
        time.sleep(10)
        version = SiiDrvAdaptVersionInfo_t()
        SiiDrvAdaptVersionGet(self.device.sii_instance, byref(version))
        logger.debug("Device ID: 0X%04x", version.chipId)
        logger.debug("Firmware Version: %02x.%02x.%02x" % (version.fwVersion >> 13,
                                                           (version.fwVersion & 0x1FFF) >> 5,
                                                           version.fwVersion & 0x001F))
        self.assertEquals(version.chipId, self.device.id, "The chip id should be %04x" % self.device.id)


class SiiDrvAdaptChipIDGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptChipIdGet(self):
        chip_id = uint16_t()
        SiiDrvAdaptChipIdGet(self.device.sii_instance, chip_id)
        logger.debug("chip id: %s" % hex(chip_id.value))
        self.assertEquals(chip_id.value, self.device.id, "chip id should be %s" % hex(self.device.id))


class SiiDrvAdaptChipGpioCtrl(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptChipGpioCtrl(self):
        self.assertTrue(1)


@unittest.skip("Not supported yet")
class SiiDrvAdaptFirmwareUpdateTestCase(BaseSiiDrvAdaptTestCase):
    """
    SiiDrvAdaptFirmwareUpdateInit
    SiiDrvAdaptFirmwareUpdate
    SiiDrvAdaptAccessStatusGet
    """
    """
    def test_SkAppFWUpdate(self):
        FwBuffer = SiiDrvAdaptFwBuffer_t()

        # bgn: used for local testing
        fw_bin = open(r'D:\project\rogue api\rogue firmware\SiI9679_FW_1.01.09_SVN20679_20140218.bin', 'rb')
        pBin = c_char_p()
        pBin.value = fw_bin.readline()
        FwBuffer.pBuffer = cast(pBin, POINTER(uint8_t))
        print(id(pBin.value))
        print(FwBuffer.pBuffer)
        FwBuffer.ucBufferSize = uint32_t(fw_bin.__sizeof__())
        FwBuffer.ucOffset = uint32_t(5)
        # end: used for local testing

        SiiDrvAdaptFirmwareUpdateInit(self.device.sii_instance)
        time.sleep(4)
        SiiDrvAdaptFirmwareUpdate(self.device.sii_instance, byref(FwBuffer))
        FwAccessStatus = c_long(1)
        FwAccessStatus_mapping = {SII_DRV_ADAPTER_ACCESS__FAILURE: "SII_DRV_ADAPTER_ACCESS__FAILURE",
                                  SII_DRV_ADAPTER_ACCESS__IN_PROGRESS: "SII_DRV_ADAPTER_ACCESS__IN_PROGRESS",
                                  SII_DRV_ADAPTER_ACCESS__SUCCESS: "SII_DRV_ADAPTER_ACCESS__SUCCESS"}
        while FwAccessStatus.value == 1:
            SiiDrvAdaptAccessStatusGet(self.device.sii_instance, FwAccessStatus)
            self.assertIn(FwAccessStatus.value, FwAccessStatus_mapping.keys(),
                          msg="Firmware access status should be in %s" % FwAccessStatus_mapping.values())
        logger.debug("Firmware access status: %s" % FwAccessStatus_mapping[FwAccessStatus.value])
    """

    def test_SkAppFWUpdate(self):
        #fw_data = (uint8_t*102404)()
        with open(r'D:\project\rogue api\rogue firmware\SiI9679_FW_1.01.09_SVN20679_20140218.bin', 'rb') as binfile:
            s = binfile.read()
            fw_data = create_string_buffer(s)
            # for i in range(len(s)):
            #     fw_data[i] = uint8_t(ord(s[i]))

        # with open(r'H:\test1.bin', "wb") as test1file:
        #     test1file.write(s)
        #
        # print type(fw_data), sizeof(fw_data), fw_data[0]
        # print addressof(fw_data)
        # print cast(addressof(fw_data), POINTER(uint8_t))
        # print cast(fw_data[0], POINTER(uint8_t))
        # dst = (uint8_t*102404)()
        # memmove(dst, addressof(fw_data), 102404)
        # with open(r'H:\test2.bin', "wb") as test2file:
        #     for i in dst:
        #         test2file.write(chr(i))
        fw_buffer = SiiDrvAdaptFwBuffer_t()
        fw_buffer.pBuffer = addressof(fw_data)
        fw_buffer.ucBufferSize = 102404
        fw_buffer.ucOffset = uint32_t(0)
        #
        SiiDrvAdaptFirmwareUpdateInit(self.device.sii_instance)
        time.sleep(4)
        SiiDrvAdaptFirmwareUpdate(self.device.sii_instance, byref(fw_buffer))
        fw_access_status = c_long(1)
        fw_access_status_mapper = {SII_DRV_ADAPTER_ACCESS__FAILURE: "SII_DRV_ADAPTER_ACCESS__FAILURE",
                                   SII_DRV_ADAPTER_ACCESS__IN_PROGRESS: "SII_DRV_ADAPTER_ACCESS__IN_PROGRESS",
                                   SII_DRV_ADAPTER_ACCESS__SUCCESS: "SII_DRV_ADAPTER_ACCESS__SUCCESS"}
        while fw_access_status.value == 1:
            SiiDrvAdaptAccessStatusGet(self.device.sii_instance, byref(fw_access_status))
            logger.debug("Firmware access status: %s" % fw_access_status_mapper[fw_access_status.value])
            self.assertIn(fw_access_status.value, fw_access_status_mapper.keys(),
                          msg="Firmware access status should be in %s" % fw_access_status_mapper.values())
            time.sleep(1.0)


class SiiDrvAdaptChipRegReadTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptChipRegRead(self):
        addr = addressof(uint16_t(0x08))
        rd = (uint8_t * 256)()
        SiiDrvAdaptChipRegRead(self.device.sii_instance, addr, rd, sizeof(rd))
        self.assertIsNotNone(rd, "Read adapter register test")

    def test_SiiDrvAdaptChipRegWrite(self):
        addr1, addr2 = addressof(uint16_t(0x08)), addressof((uint16_t(0x45)))
        rd1, rd2 = (uint8_t * 16)(), (uint8_t * 16)()
        SiiDrvAdaptChipRegRead(self.device.sii_instance, addr1, rd1, sizeof(rd1))
        rd_list1 = self.make_rd_list(rd1)
        SiiDrvAdaptChipRegWrite(self.device.sii_instance, addr2, rd1, sizeof(rd1))
        SiiDrvAdaptChipRegRead(self.device.sii_instance, addr2, rd2, sizeof(rd2))
        rd_list2 = self.make_rd_list(rd2)
        self.assertListEqual(rd_list1, rd_list2, "Write adapter register test")

    def make_rd_list(self, rd):
        rd_list = []
        for __i in rd:
            rd_list.append(__i)
        return rd_list

if __name__ == "__main__":
    pass
