#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import time
import unittest
from ctypes import *
from simg.test.framework import skipif
from simg.devadapter.wired.rogue.api import *
from base import BaseSiiDrvAdaptTestCase


"""
Real EDID read from SiiMon:

Edid Block 0 Data:

00 ff ff ff ff ff ff 00 4d 10 8e 10 00 00 00 00
ff 15 01 03 80 52 2e 78 2a 1b be a2 55 34 b3 26
14 4a 52 af ce 00 01 01 01 01 01 01 01 01 01 01
01 01 01 01 01 01 01 1d 00 bc 52 d0 1e 20 b8 28
55 40 34 cc 31 00 00 1e 66 21 50 b0 51 00 1b 30
40 70 36 00 34 cc 31 00 00 1e 00 00 00 fc 00 53
48 41 52 50 20 48 44 4d 49 0a 20 20 00 00 00 fd
00 17 4c 0e 44 0f 00 0a 20 20 20 20 20 20 01 4f

Edid Block 1 Data

02 03 2e 72 50 93 84 1f 10 20 14 05 12 03 11 02
16 07 15 06 01 23 09 07 01 83 01 00 00 e3 05 00
00 6c 03 0c 00 10 00 80 1e 80 11 11 00 00 01 1d
00 72 51 d0 1e 20 6e 28 55 00 34 cc 31 00 00 1e
02 3a 80 d0 72 38 2d 40 10 2c 45 80 34 cc 31 00
00 1e 02 3a 80 18 71 38 2d 40 58 2c 45 00 34 cc
31 00 00 1e 01 1d 80 d0 72 1c 16 20 10 2c 25 80
34 cc 31 00 00 9e 00 00 00 00 00 00 00 00 00 c0
"""

sony_edid = [
    0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x4d, 0xd9, 0x03, 0x24, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x17, 0x01, 0x03, 0x80, 0x7a, 0x44, 0x78, 0x0a, 0x0d, 0xc9, 0xa0, 0x57, 0x47, 0x98, 0x27,
    0x12, 0x48, 0x4c, 0x21, 0x08, 0x00, 0x81, 0x80, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x3a, 0x80, 0x18, 0x71, 0x38, 0x2d, 0x40, 0x58, 0x2c,
    0x45, 0x00, 0xc2, 0xad, 0x42, 0x00, 0x00, 0x1e, 0x01, 0x1d, 0x00, 0x72, 0x51, 0xd0, 0x1e, 0x20,
    0x6e, 0x28, 0x55, 0x00, 0xc2, 0xad, 0x42, 0x00, 0x00, 0x1e, 0x00, 0x00, 0x00, 0xfc, 0x00, 0x53,
    0x4f, 0x4e, 0x59, 0x20, 0x54, 0x56, 0x20, 0x20, 0x2a, 0x30, 0x37, 0x0a, 0x00, 0x00, 0x00, 0xfd,
    0x00, 0x30, 0x3e, 0x0e, 0x46, 0x0f, 0x00, 0x0a, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x01, 0x7a,
    0x02, 0x03, 0x43, 0xf0, 0x53, 0x1f, 0x10, 0x14, 0x05, 0x13, 0x04, 0x20, 0x22, 0x3c, 0x3e, 0x12,
    0x16, 0x03, 0x07, 0x11, 0x15, 0x02, 0x06, 0x01, 0x26, 0x09, 0x07, 0x07, 0x15, 0x07, 0x50, 0x83,
    0x01, 0x00, 0x00, 0x78, 0x03, 0x0c, 0x00, 0x40, 0x00, 0xb8, 0x3c, 0x2f, 0xd0, 0x8a, 0x01, 0x02,
    0x03, 0x04, 0x01, 0x40, 0x00, 0x7f, 0x20, 0x30, 0x70, 0x80, 0x90, 0x76, 0xe2, 0x00, 0xfb, 0xe3,
    0x05, 0x1f, 0x01, 0x02, 0x3a, 0x80, 0xd0, 0x72, 0x38, 0x2d, 0x40, 0x10, 0x2c, 0x45, 0x80, 0xc2,
    0xad, 0x42, 0x00, 0x00, 0x1e, 0x01, 0x1d, 0x00, 0xbc, 0x52, 0xd0, 0x1e, 0x20, 0xb8, 0x28, 0x55,
    0x40, 0xc2, 0xad, 0x42, 0x00, 0x00, 0x1e, 0x01, 0x1d, 0x80, 0xd0, 0x72, 0x1c, 0x16, 0x20, 0x10,
    0x2c, 0x25, 0x80, 0xc2, 0xad, 0x42, 0x00, 0x00, 0x9e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40
]

sii_edid = [
    0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x4D, 0x10, 0xE8, 0x0F, 0x01, 0x01, 0x01, 0x01,
    0x00, 0x10, 0x01, 0x03, 0x80, 0x73, 0x41, 0x78, 0x2A, 0x1B, 0xBE, 0xA2, 0x55, 0x34, 0xB3, 0x26,
    0x14, 0x4A, 0x52, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0xD0, 0x72, 0x38, 0x2D, 0x40, 0x10, 0x2C,
    0x45, 0x80, 0x80, 0x88, 0x42, 0x00, 0x00, 0x1E, 0x00, 0x00, 0x00, 0x18, 0x71, 0x38, 0x2D, 0x40,
    0x58, 0x2C, 0x45, 0x00, 0x80, 0x88, 0x42, 0x00, 0x00, 0x1E, 0x00, 0x00, 0x00, 0xFC, 0x00, 0x53,
    0x48, 0x41, 0x52, 0x50, 0x20, 0x48, 0x44, 0x4D, 0x49, 0x0A, 0x20, 0x20, 0x00, 0x00, 0x00, 0xFD,
    0x00, 0x31, 0x3D, 0x0F, 0x4B, 0x11, 0x00, 0x0A, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x01, 0xD1,
    0x02, 0x03, 0x23, 0x71, 0x4F, 0x00, 0x00, 0x14, 0x05, 0x13, 0x04, 0x12, 0x03, 0x11, 0x02, 0x16,
    0x07, 0x15, 0x06, 0x01, 0x23, 0x09, 0x07, 0x07, 0x83, 0x01, 0x00, 0x00, 0x66, 0x03, 0x0C, 0x00,
    0x00, 0x10, 0x80, 0x01, 0x1D, 0x80, 0xD0, 0x72, 0x1C, 0x16, 0x20, 0x10, 0x2C, 0x25, 0x80, 0x80,
    0x88, 0x42, 0x00, 0x00, 0x9E, 0x01, 0x1D, 0x80, 0x18, 0x71, 0x1C, 0x16, 0x20, 0x58, 0x2C, 0x25,
    0x00, 0x80, 0x88, 0x42, 0x00, 0x00, 0x9E, 0x01, 0x1D, 0x00, 0xBC, 0x52, 0xD0, 0x1E, 0x20, 0xB8,
    0x28, 0x55, 0x40, 0x80, 0x88, 0x42, 0x00, 0x00, 0x1E, 0x01, 0x1D, 0x00, 0x72, 0x51, 0xD0, 0x1E,
    0x20, 0x6E, 0x28, 0x55, 0x00, 0x7E, 0x88, 0x42, 0x00, 0x00, 0x1E, 0x8C, 0x0A, 0xD0, 0x90, 0x20,
    0x40, 0x31, 0x20, 0x0C, 0x40, 0x55, 0x00, 0x80, 0x88, 0x42, 0x00, 0x00, 0x18, 0x00, 0x00, 0xBE
]


# print EDID as 16 * 16 matrix
def _print_edid(edid_data):
    import sys

    print "   | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F"
    print "-" * 52
    for i in range(256):
        if (i + 1) % 16 == 0:
            sys.stdout.write(str("%0.2x " % edid_data[i]).upper())
            print
        else:
            if (i + 1) % 16 == 1:
                sys.stdout.write(str("%0.2x | " % ((i + 1) / 16)).upper())
            sys.stdout.write(str("%0.2x " % edid_data[i]).upper())


"""
HDMI pin definition (Type A):
   19  17  15  13  11  9   7   5   3   1
\--==--==--==--==--==--==--==--==--==--==--/
 \                                        /
  \  18  16  14  12  10  8   6   4   2   /
   --==--==--==--==--==--==--==--==--==--

pin1 	TMDS Data2+ (TMDS = Transition Minimized Different Signaling)
pin2 	TMDS Data2 Shield
pin3 	TMDS Data2–
pin4 	TMDS Data1+
pin5 	TMDS Data1 Shield
pin6 	TMDS Data1–
pin7 	TMDS Data0+
pin8 	TMDS Data0 Shield
pin9 	TMDS Data0–
pin10 	TMDS Clock+
pin11 	TMDS Clock Shield
pin12 	TMDS Clock–
pin13 	CEC (Consumer Electronics Control)
pin14 	Reserved (N.C. on device)
pin15 	SCL
pin16 	SDA
pin17 	DDC/CEC Ground
pin18 	+5 V Power
pin19 	Hot Plug Detect
"""

# 7.4.4.1 RX EDID SRAM Updating
"""
This API is to write the data into EDID Sram. Before writing the data make sure to call
SiiDrvAdaptAccessStatusGet() to detect whether it is available to write data into SRAM.

SiiDrvAdaptAccessStatus_t:
0    SII_DRV_ADAPTER_ACCESS__SUCCESS,     //!< Reading/writing is done successfully
1    SII_DRV_ADAPTER_ACCESS__IN_PROGRESS, //!< Reading/writing is in progress
2    SII_DRV_ADAPTER_ACCESS__FAILURE,     //!< Reading/writing failed
"""
# noinspection PyCallingNonCallable
class SiiDrvRxEDIDSramUpdatingTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptEdidSramWrite(self):
        poUpdateStatus = SiiDrvAdaptAccessStatus_t()
        SiiDrvAdaptAccessStatusGet(self.device.sii_instance, poUpdateStatus)

        self.assertEquals(poUpdateStatus.value, SII_DRV_ADAPTER_ACCESS__SUCCESS,
                          "SiiDrvAdaptAccessStatus should be 0(SUCCESS)")

        offset = uint16_t(0)
        pData = (uint8_t * 256)()
        length = sizeof(pData)

        SiiDrvAdaptRxEdidSramWrite(self.device.sii_instance, offset, byref(pData), length)


# 7.4.4.2 RX EDID SRAM Reading
# noinspection PyCallingNonCallable
class SiiDrvRxEDIDSramReadingTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptEdidSramRead(self):
        poUpdateStatus = SiiDrvAdaptAccessStatus_t()
        SiiDrvAdaptAccessStatusGet(self.device.sii_instance, poUpdateStatus)

        self.assertEquals(poUpdateStatus.value, SII_DRV_ADAPTER_ACCESS__SUCCESS,
                          "SiiDrvAdaptAccessStatus should be 0(SUCCESS)")

        offset = uint16_t(0)

        """
        unsigned char Edid[256];
        Need above array for pData, refer to https://docs.python.org/2/library/ctypes.html:

        ctypes      C type
        c_ushort    unsigned char

        (c_ushort * 256)() will initialize a 256 unsigned char C array.
        """

        pwData = (uint8_t * 256)()
        prData = (uint8_t * 256)()
        # pData = cast(pData, POINTER(uint8_t))
        length = sizeof(prData)

        for i in range(256):
            pwData[i] = sony_edid[i]

        print 'Prepared EDID for SRAM'
        _print_edid(pwData)

        # SiiDrvAdaptRxEdidSramWrite(self.device.sii_instance, offset, pwData, length)
        # time.sleep(15)
        SiiDrvAdaptRxEdidSramRead(self.device.sii_instance, offset, prData, length)

        print

        print 'After write prepared SRAM, read EDID into console'
        _print_edid(prData)

        # for idx, data in enumerate(prData):
        # print hex(idx).upper(), ("%0.2x" % data).upper()


# 7.4.4.3 RX EDID EEPROM Updating
# noinspection PyCallingNonCallable
class SiiDrvAdaptRxEDIDEepRomUpdatingTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptEepromEdidWrite(self):
        poUpdateStatus = SiiDrvAdaptAccessStatus_t()
        SiiDrvAdaptAccessStatusGet(self.device.sii_instance, poUpdateStatus)

        self.assertEquals(poUpdateStatus.value, SII_DRV_ADAPTER_ACCESS__SUCCESS,
                          "SiiDrvAdaptAccessStatus should be 0(SUCCESS)")

        offset = uint8_t(0)

        pwData = (uint8_t * 256)()
        prData = (uint8_t * 256)()

        length = sizeof(prData)

        for i in range(256):
            pwData[i] = sony_edid[i]

        pwData = cast(pwData, POINTER(uint8_t))

        print 'Prepared EDID for EEPROM'
        _print_edid(pwData)

        # SiiDrvAdaptEepromEdidWrite(inst, offset, poData, length)
        # SiiDrvAdaptEepromEdidWrite.argtypes = [SiiInst_t, uint8_t, POINTER(uint8_t), uint16_t]
        # SiiDrvAdaptEepromEdidWrite(self.device.sii_instance, offset, pwData, length)
        # time.sleep(15)
        SiiDrvAdaptEepromEdidRead(self.device.sii_instance, offset, prData, length)

        print

        print 'After write prepared EDID into EEPROM, read EDID into console'
        _print_edid(prData)


# 7.4.4.4 RX EDID EEPROM Reading
# noinspection PyCallingNonCallable
class SiiDrvAdaptRxEDIDEepRomReadingTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptEepromEdidRead(self):
        time.sleep(10)

        hpd = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__ENABLE)
        SiiDrvAdaptRxHpdSet(self.device.sii_instance, hpd)

        time.sleep(10)

        poUpdateStatus = SiiDrvAdaptAccessStatus_t()
        SiiDrvAdaptAccessStatusGet(self.device.sii_instance, poUpdateStatus)

        self.assertEquals(poUpdateStatus.value, SII_DRV_ADAPTER_ACCESS__SUCCESS,
                          "SiiDrvAdaptAccessStatus should be 0(SUCCESS)")

        offset = uint8_t(0)

        pwData = (uint8_t * 256)()
        prData = (uint8_t * 256)()

        length = sizeof(prData)

        for i in range(256):
            pwData[i] = sony_edid[i]

        # pwData = cast(pwData, POINTER(uint8_t))
        #
        # print 'Prepared EDID for EEPROM'
        # _print_edid(pwData)

        # SiiDrvAdaptEepromEdidWrite(inst, offset, poData, length)
        # SiiDrvAdaptEepromEdidWrite.argtypes = [SiiInst_t, uint8_t, POINTER(uint8_t), uint16_t]
        # SiiDrvAdaptEepromEdidWrite(self.device.sii_instance, offset, pwData, length)
        # time.sleep(15)

        logger.info("DDC ENABLE Start")
        ddc = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__ENABLE)
        SiiDrvAdaptEdidDdcSet(self.device.sii_instance, ddc)

        time.sleep(5)
        logger.info("DDC ENABLE End")

        SiiDrvAdaptEepromEdidRead(self.device.sii_instance, offset, prData, length)

        print

        print 'After write prepared EDID into EEPROM, read EDID into console'
        _print_edid(prData)


# 7.4.4.5 Receiver HPD Control
# HPD = Hot Plug Detection
"""
Set Rx Hot Plug capability.

SiiDrvAdaptInpCtrl_t:
0    SII_DRV_ADAPT_INP_CTRL__BYPASS,  //!< Copy from downstream
1    SII_DRV_ADAPT_INP_CTRL__DISABLE, //!< Disable or set LOW
2    SII_DRV_ADAPT_INP_CTRL__ENABLE,  //!< Enable or set HIGH

Issue: It's hard to know the external behaviour when the HPD is disabled or enabled.
"""
class SiiDrvAdaptReceiverHPDControlTestCase(BaseSiiDrvAdaptTestCase):
    """
    This function is not supported currently.
    """

    @unittest.skip("HPD Set to BYPASS is not supported right now")
    def test_SiiDrvAdaptHpdSet_BYPASS(self):
        hpd = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__BYPASS)
        SiiDrvAdaptRxHpdSet(self.device.sii_instance, hpd)

    def test_SiiDrvAdaptHpdSet_DISABLE(self):
        hpd = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__ENABLE)
        SiiDrvAdaptRxHpdSet(self.device.sii_instance, hpd)

        time.sleep(10)

        with self.device.log_subject.listen("TX TMDS OFF") as listener:
            hpd = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__DISABLE)
            SiiDrvAdaptRxHpdSet(self.device.sii_instance, hpd)

            time.sleep(10)

            s = listener.get(timeout=10)
            self.assertIsNotNone(s, "Should receive 'TX TMDS OFF' in log")

    def test_SiiDrvAdaptHpdSet_ENABLE(self):
        hpd = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__DISABLE)
        SiiDrvAdaptRxHpdSet(self.device.sii_instance, hpd)

        logger.info('Disable Started')
        time.sleep(10)
        logger.info('Disable Ended')

        with self.device.log_subject.listen("AVI INFO recv") as listener:
            hpd = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__ENABLE)
            SiiDrvAdaptRxHpdSet(self.device.sii_instance, hpd)

            time.sleep(10)

            s = listener.get(timeout=10)
            self.assertIsNotNone(s, "Should receive 'AVI INFO recv' in log")


# 7.4.4.6 RX Termination Control
"""
SiiDrvAdaptInpCtrl_t:
0    SII_DRV_ADAPT_INP_CTRL__BYPASS,  //!< Copy from downstream
1    SII_DRV_ADAPT_INP_CTRL__DISABLE, //!< Disable or set LOW
2    SII_DRV_ADAPT_INP_CTRL__ENABLE,  //!< Enable or set HIGH

Issue: how to assert the post status of Rx after adapter is terminated?
"""


class SiiDrvAdaptRxTerminationControlTestCase(BaseSiiDrvAdaptTestCase):
    """
    This function is not supported currently.
    """

    @unittest.skip("Termination Set to BYPASS is not supported right now")
    def test_SiiDrvAdaptTermSet_BYPASS(self):
        term = SiiDrvAdaptInpCtrl_t(0)
        SiiDrvAdaptRxTermSet(self.device.sii_instance, term)

    def test_SiiDrvAdaptTermSet_DISABLE(self):
        logger.info("HPD ENABLE Start")
        hpd = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__ENABLE)
        SiiDrvAdaptRxHpdSet(self.device.sii_instance, hpd)
        logger.info("HPD Enable End")

        with self.device.log_subject.listen("TX HDCP OFF") as listener:
            logger.info("Termination DISABLE Start")
            term = SiiDrvAdaptInpCtrl_t(1)
            SiiDrvAdaptRxTermSet(self.device.sii_instance, term)

            time.sleep(10)

            s = listener.get(timeout=10)
            self.assertIsNotNone(s, "Should receive 'TX HDCP OFF' in log")

            time.sleep(20)
            logger.info("Termination DISABLE End")

        logger.info("Termination ENABLE Start")
        term = SiiDrvAdaptInpCtrl_t(2)
        SiiDrvAdaptRxTermSet(self.device.sii_instance, term)
        time.sleep(20)
        logger.info("Termination ENABLE End")

    def test_SiiDrvAdaptTermSet_ENABLE(self):
        logger.info("HPD ENABLE Start")
        hpd = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__ENABLE)
        SiiDrvAdaptRxHpdSet(self.device.sii_instance, hpd)
        logger.info("HPD Enable End")

        with self.device.log_subject.listen("TX HDCP OFF") as listener:
            logger.info("Termination DISABLE Start")
            term = SiiDrvAdaptInpCtrl_t(1)
            SiiDrvAdaptRxTermSet(self.device.sii_instance, term)

            time.sleep(10)

            s = listener.get(timeout=10)
            self.assertIsNotNone(s, "Should receive 'TX HDCP OFF' in log")

            logger.info("Termination DISABLE End")

        with self.device.log_subject.listen("AVI INFO recv") as listener:
            logger.info("Termination ENABLE Start")
            term = SiiDrvAdaptInpCtrl_t(2)
            SiiDrvAdaptRxTermSet(self.device.sii_instance, term)

            time.sleep(20)

            s = listener.get(timeout=10)
            self.assertIsNotNone(s, "Should receive 'AVI INFO recv' in log")
            logger.info("Termination ENABLE End")

# 7.4.4.7 RX EDID DDC Control
"""
DDC = Display Data Channel

SiiDrvAdaptInpCtrl_t:
0    SII_DRV_ADAPT_INP_CTRL__BYPASS,  //!< Copy from downstream
1    SII_DRV_ADAPT_INP_CTRL__DISABLE, //!< Disable or set LOW
2    SII_DRV_ADAPT_INP_CTRL__ENABLE,  //!< Enable or set HIGH
"""

"""
Per the DEV, this API is for enabling external EEPROM update and not for memory EDID update. So this is not required to
be verified in Rogue Rx mode.
"""
class SiiDrvAdaptRxEDIDDDCControlTestCase(BaseSiiDrvAdaptTestCase):
    """
    This function is not supported currently.
    """

    @unittest.skip("DDC Control set to BYPASS is not supported right now")
    def test_SiiDrvAdaptEdidDdcSet_BYPASS(self):
        ddc = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__BYPASS)
        SiiDrvAdaptEdidDdcSet(self.device.sii_instance, ddc)

    def test_SiiDrvAdaptEdidDdcSet_DISABLE(self):
        logger.info("HPD ENABLE Start")
        hpd = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__ENABLE)
        SiiDrvAdaptRxHpdSet(self.device.sii_instance, hpd)
        time.sleep(5)
        logger.info("HPD Enable End")

        logger.info("DDC DISABLE Start")
        ddc = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__DISABLE)
        SiiDrvAdaptEdidDdcSet(self.device.sii_instance, ddc)
        time.sleep(5)
        logger.info("DDC DISABLE End")

        # logger.info("DDC ENABLE Start")
        # ddc = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__ENABLE)
        # SiiDrvAdaptEdidDdcSet(self.device.sii_instance, ddc)
        #
        # time.sleep(20)
        # logger.info("DDC ENABLE End")

        poEdidStatus = SiiDrvAdaptDsEdidStatus_t()
        SiiDrvAdaptTxDsEdidStatusGet(self.device.sii_instance, poEdidStatus)
        print poEdidStatus.value
        self.assertEqual(SII_DRV_ADAPT_DS_EDID__AVAILABLE, poEdidStatus.value,
                         msg="Downstream EDID status should be SII_DRV_ADAPT_DS_EDID__AVAILABLE")

    def test_SiiDrvAdaptEdidDdcSet_ENABLE(self):
        ddc = SiiDrvAdaptInpCtrl_t(SII_DRV_ADAPT_INP_CTRL__ENABLE)
        SiiDrvAdaptEdidDdcSet(self.device.sii_instance, ddc)
        poEdidStatus = SiiDrvAdaptDsEdidStatus_t()
        SiiDrvAdaptTxDsEdidStatusGet(self.device.sii_instance, poEdidStatus)
        self.assertEqual(SII_DRV_ADAPT_DS_EDID__NOT_AVAILABLE, poEdidStatus.value,
                         msg="Downstream EDID status should be SII_DRV_ADAPT_DS_EDID__NOT_AVAILABLE")


# 7.4.4.8 RX 5v Status Get
"""
Once unplug the HDMI rx line, the 5V status will return false.

Issue: It's hard to automate plug/unplug HDMI line and need some proposal.
"""
class SiiDrvAdaptRx5VStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxPlus5vStatusGet(self):
        poPlus5vStat = bool_t()
        SiiDrvAdaptRxPlus5vStatusGet(self.device.sii_instance, byref(poPlus5vStat))
        logger.info("Check whether current 5V status is true: %s " % poPlus5vStat.value)
        self.assertTrue(poPlus5vStat, "Current 5V status is TRUE")


# 7.4.4.9 RX Clock Status Get
class SiiDrvAdaptRxClockStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptCkdtStatusGet(self):
        poCkdtStatus = bool_t()
        SiiDrvAdaptCkdtStatusGet(self.device.sii_instance, byref(poCkdtStatus))
        self.assertTrue(poCkdtStatus.value, "The TMDS clock should be present after initialization completes")

# 7.4.4.10 RX SCDT Status Get
"""
Get Rx Sync Detection Status
"""
class SiiDrvAdaptRxSCDTStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptScdtStatusGet(self):
        poScdtDetStatus = bool_t()
        SiiDrvAdaptScdtStatusGet(self.device.sii_instance, poScdtDetStatus)
        self.assertTrue(poScdtDetStatus.value, "SCDT status should be true and TMDS is in locked status")

# 7.4.4.11 RX AV Mute Status Get
"""
SiiDrvAdaptMute_t:
0    SII_DRV_ADAPTER_MUTE__OFF,           //!< Neither Clear AV Mute nor Set AV Mute are send
1    SII_DRV_ADAPTER_MUTE__AV_MUTE_OFF,   //!< Send Clear AV Mute packet
2    SII_DRV_ADAPTER_MUTE__AV_MUTE_ON,    //!< Send Set AV Mute packet
3    SII_DRV_ADAPTER_MUTE__VIDEO,         //!< Blank video and send Clear AV Mute
4    SII_DRV_ADAPTER_MUTE__AUDIO,         //!< Mute audio and send Clear AV Mute
5    SII_DRV_ADAPTER_MUTE__AUDIO_VIDEO    //!< Mute audio video, blank video, and send Clear AV Mute
"""
class SiiDrvAdaptAVMuteStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    @unittest.skip("SII_DRV_ADAPTER_MUTE__OFF is not mentioned in API Spec")
    def test_SiiDrvAdaptRxAvMuteStatusGet_OFF(self):
        poMuteStat = SiiDrvAdaptMute_t(0)
        SiiDrvAdaptTxMuteSet(self.device.sii_instance, poMuteStat)
        time.sleep(5)
        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, poMuteStat)
        logger.info("Get the AV mute status from RX: %s" % poMuteStat.value)
        self.assertEqual(poMuteStat, SII_DRV_ADAPTER_MUTE__OFF, "Current mute status is : %s" % poMuteStat.value)

    def test_SiiDrvAdaptRxAvMuteStatusGet_AV_MUTE_ON(self):
        # Turn down the AV
        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__RX_AV_MUTE_STATUS_CHNG) as listener:
            poMuteStat = SiiDrvAdaptMute_t(2)
            SiiDrvAdaptTxMuteSet(self.device.sii_instance, poMuteStat)
            time.sleep(5)
            self.assertIsNotNone(listener.get(timeout=10), "The AV MUTE CHANGE event should be captured here")

        # Turn on the AV
        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__RX_AV_MUTE_STATUS_CHNG) as listener:
            poMuteStat = SiiDrvAdaptMute_t(1)
            SiiDrvAdaptTxMuteSet(self.device.sii_instance, poMuteStat)
            time.sleep(5)
            self.assertIsNotNone(listener.get(timeout=10), "The AV MUTE CHANGE event should be captured here")

        # Turn down the AV again
        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__RX_AV_MUTE_STATUS_CHNG) as listener:
            poMuteStat = SiiDrvAdaptMute_t(2)
            SiiDrvAdaptTxMuteSet(self.device.sii_instance, poMuteStat)
            time.sleep(5)
            self.assertIsNotNone(listener.get(timeout=10), "The AV MUTE CHANGE event should be captured here")

        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, poMuteStat)
        logger.info("Get the AV mute status from RX: %s" % poMuteStat.value)
        self.assertEqual(poMuteStat.value, SII_DRV_ADAPTER_MUTE__AV_MUTE_ON,
                         "Current mute status is : %s" % poMuteStat.value)

    def test_SiiDrvAdaptRxAvMuteStatusGet_AV_MUTE_OFF(self):
        # Turn down the AV
        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__RX_AV_MUTE_STATUS_CHNG) as listener:
            poMuteStat = SiiDrvAdaptMute_t(2)
            SiiDrvAdaptTxMuteSet(self.device.sii_instance, poMuteStat)
            time.sleep(5)
            self.assertIsNotNone(listener.get(timeout=10), "The AV MUTE CHANGE event should be captured here")

        # Turn on the AV
        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__RX_AV_MUTE_STATUS_CHNG) as listener:
            poMuteStat = SiiDrvAdaptMute_t(1)
            SiiDrvAdaptTxMuteSet(self.device.sii_instance, poMuteStat)
            time.sleep(5)
            self.assertIsNotNone(listener.get(timeout=10), "The AV MUTE CHANGE event should be captured here")


        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, poMuteStat)
        logger.info("Get the AV mute status from RX: %s" % poMuteStat.value)
        self.assertEqual(poMuteStat.value, SII_DRV_ADAPTER_MUTE__AV_MUTE_OFF, "Current mute status is : %s" % poMuteStat.value)

    @unittest.skip("SII_DRV_ADAPTER_MUTE__OFF is not mentioned in API Spec")
    def test_SiiDrvAdaptRxAvMuteStatusGet_VIDEO(self):
        poMuteStat = SiiDrvAdaptMute_t(3)
        SiiDrvAdaptTxMuteSet(self.device.sii_instance, poMuteStat)
        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, poMuteStat)
        logger.info("Get the AV mute status from RX: %s" % poMuteStat.value)
        self.assertEqual(poMuteStat, SII_DRV_ADAPTER_MUTE__VIDEO, "Current mute status is : %s" % poMuteStat.value)

    @unittest.skip("SII_DRV_ADAPTER_MUTE__OFF is not mentioned in API Spec")
    def test_SiiDrvAdaptRxAvMuteStatusGet_AUDIO(self):
        poMuteStat = SiiDrvAdaptMute_t(4)
        SiiDrvAdaptTxMuteSet(self.device.sii_instance, poMuteStat)
        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, poMuteStat)
        logger.info("Get the AV mute status from RX: %s" % poMuteStat.value)
        self.assertEqual(poMuteStat, SII_DRV_ADAPTER_MUTE__AUDIO, "Current mute status is : %s" % poMuteStat.value)

    @unittest.skip("SII_DRV_ADAPTER_MUTE__OFF is not mentioned in API Spec")
    def test_SiiDrvAdaptRxAvMuteStatusGet_AUDIO_VIDEO(self):
        poMuteStat = SiiDrvAdaptMute_t(5)
        SiiDrvAdaptTxMuteSet(self.device.sii_instance, poMuteStat)
        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, poMuteStat)
        logger.info("Get the AV mute status from RX: %s" % poMuteStat.value)
        self.assertEqual(poMuteStat, SII_DRV_ADAPTER_MUTE__AUDIO_VIDEO,
                         "Current mute status is : %s" % poMuteStat.value)


# 7.4.4.12 RX HDCP DDC control
"""
Upstream HDCP status interrogation
SiiDrvAdaptHdcpRxStatus_t:
0    SII_DRV_ADAPTER_HDCP_RX_STATUS__OFF,
1    SII_DRV_ADAPTER_HDCP_RX_STATUS__SUCCESS,
2    SII_DRV_ADAPTER_HDCP_RX_STATUS__AUTHENTICATING,
3    SII_DRV_ADAPTER_HDCP_RX_STATUS__FAIL,

Issue: How can we control and specify the HDCP capability in the up stream of RX?

Refer to: SiiDrvAdaptTxHdcpProtectionSet API in Tx end.
Refer to: SiiHalChipReset API in MHL end.
"""
class SiiDrvAdaptRxHDCPDDCControlTestCase(BaseSiiDrvAdaptTestCase):
    def collect_hdcp_status(self):
        ret = set()
        from time import time
        start = time()
        while True:
            poHdcpStatus = SiiDrvAdaptHdcpRxStatus_t()
            SiiDrvAdaptRxHdcpUsStatusGet(self.device.sii_instance, poHdcpStatus)
            ret.add(poHdcpStatus.value)
            if len(ret) == 3 or (time() - start) > 180:
                break
        return ret

    def test_SiiDrvAdptHdcpDdcGet_OFF(self):
        ret = self.collect_hdcp_status()
        self.assertTrue(ret == {0, 1, 2}, "HDCP Status should be OFF")

    def test_SiiDrvAdptHdcpDdcGet_SUCCESS(self):
        ret = self.collect_hdcp_status()
        self.assertTrue(ret == {0, 1, 2}, "HDCP Status should be OFF")

    def test_SiiDrvAdptHdcpDdcGet_AUTHENTICATING(self):
        ret = self.collect_hdcp_status()
        self.assertTrue(ret == {0, 1, 2}, "HDCP Status should be OFF")

    """
    Not able to mock up a fail HDCP status.
    """
    def test_SiiDrvAdptHdcpDdcGet_FAIL(self):
        poHdcpStatus = SiiDrvAdaptHdcpRxStatus_t()
        SiiDrvAdaptRxHdcpUsStatusGet(self.device.sii_instance, poHdcpStatus)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_RX_STATUS__FAIL, poHdcpStatus.value)

# 7.4.4.13 RX HDCP Status Get
"""
SiiDrvAdaptHdcpRxStatus_t:
0    SII_DRV_ADAPTER_HDCP_RX_STATUS__OFF,
1    SII_DRV_ADAPTER_HDCP_RX_STATUS__SUCCESS,
2    SII_DRV_ADAPTER_HDCP_RX_STATUS__AUTHENTICATING,
3    SII_DRV_ADAPTER_HDCP_RX_STATUS__FAIL,
"""
class SiiDrvRxHDCPStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpStatusGet_OFF(self):
        poHdcpStatus = SiiDrvAdaptHdcpRxStatus_t()
        SiiDrvAdaptRxHdcpUsStatusGet(self.device.sii_instance, poHdcpStatus)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_RX_STATUS__OFF, poHdcpStatus.value)

    def test_SiiDrvAdaptRxHdcpStatusGet_SUCCESS(self):
        poHdcpStatus = SiiDrvAdaptHdcpRxStatus_t()
        SiiDrvAdaptRxHdcpUsStatusGet(self.device.sii_instance, poHdcpStatus)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_RX_STATUS__OFF, poHdcpStatus.value)

    def test_SiiDrvAdaptRxHdcpStatusGet_AUTHENTICATING(self):
        poHdcpStatus = SiiDrvAdaptHdcpRxStatus_t()
        SiiDrvAdaptRxHdcpUsStatusGet(self.device.sii_instance, poHdcpStatus)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_RX_STATUS__AUTHENTICATING, poHdcpStatus.value)

    def test_SiiDrvAdaptRxHdcpStatusGet_FAIL(self):
        poHdcpStatus = SiiDrvAdaptHdcpRxStatus_t()
        SiiDrvAdaptRxHdcpUsStatusGet(self.device.sii_instance, poHdcpStatus)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_RX_STATUS__FAIL, poHdcpStatus.value)

# 7.4.4.14 RX BKSV Get
"""
Returns upstream (own) BKSV for HDCP 1.X.

SiiDrvAdaptHdcpKsvLoadError_t:
0    SII_DRV_ADAPTER_KSV_LOAD__OK,            //!< success
1    SII_DRV_ADAPTER_KSV_LOAD__NOT_AVAILABLE, //!< BKSV/RxID list was attempted to be read
2    SII_DRV_ADAPTER_KSV_LOAD__BUFFER_ERROR,  //!< BKSV/RxID buffer is too small to fit all BKSV/RxIDs.
"""
class SiiDrvAdaptRxBKSVGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpBksvGet(self):
        # noinspection PyCallingNonCallable
        poBksvBuffer = (uint8_t * 5)()
        ret = SiiDrvAdaptRxHdcpBksvGet(self.device.sii_instance, poBksvBuffer)
        self.assertEqual(SII_DRV_ADAPTER_KSV_LOAD__OK, ret)


# 7.4.4.15 RX Receiver ID Get
"""
Returns upstream (own) RX ID for HDCP 2.2.
"""
class SiiDrvAdaptRxReceiverIDGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpRxIdGet(self):
        # noinspection PyCallingNonCallable
        poRxIdBuffer = (uint8_t * 5)()
        SiiDrvAdaptRxHdcpRxIdGet(self.device.sii_instance, poRxIdBuffer)
        logger.info([idx for idx in poRxIdBuffer])

# 7.4.4.16 RX HDCP Version Get
"""
SiiDrvAdaptHdcpVer_t:
0    SII_DRV_ADAPTER_HDCP_VER__NOT_SUPPORTED,               //!< HDCP not supported by the source device.
1    SII_DRV_ADAPTER_HDCP_VER__1x,                          //!< HDCP 1.x supported by source device
2    SII_DRV_ADAPTER_HDCP_VER__20,                          //!< HDCP 2.0 supported by source device
3    SII_DRV_ADAPTER_HDCP_VER__21,                          //!< HDCP 2.1 supported by source device
4    SII_DRV_ADAPTER_HDCP_VER__22,                          //!< HDCP 2.2 supported by source device
"""
class SiiDrvAdaptRxHDCPVersionGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptSourceHdcpVerGet_NOT_SUPPORTED(self):
        poHdcpVer = SiiDrvAdaptHdcpVer_t()
        SiiDrvAdaptRxHdcpUsVerGet(self.device.sii_instance, poHdcpVer)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_VER__NOT_SUPPORTED, poHdcpVer.value)

    @skipif("self.device.us_hdcpversion != '1.x'", "This test cases should not be executed once HDCP is not 1.x")
    def test_SiiDrvAdaptSourceHdcpVerGet_HDCP_VER__1x(self):
        poHdcpVer = SiiDrvAdaptHdcpVer_t()
        SiiDrvAdaptRxHdcpUsVerGet(self.device.sii_instance, poHdcpVer)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_VER__1x, poHdcpVer.value)

    @skipif("self.device.us_hdcpversion != '2.0'", "This test cases should not be executed once HDCP is not 2.0")
    def test_SiiDrvAdaptSourceHdcpVerGet_HDCP_VER__20(self):
        poHdcpVer = SiiDrvAdaptHdcpVer_t()
        SiiDrvAdaptRxHdcpUsVerGet(self.device.sii_instance, poHdcpVer)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_VER__20, poHdcpVer.value)

    @skipif("self.device.us_hdcpversion != '2.1'", "This test cases should not be executed once HDCP is not 2.1")
    def test_SiiDrvAdaptSourceHdcpVerGet_HDCP_VER__21(self):
        poHdcpVer = SiiDrvAdaptHdcpVer_t()
        SiiDrvAdaptRxHdcpUsVerGet(self.device.sii_instance, poHdcpVer)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_VER__21, poHdcpVer.value)

    @skipif("self.device.us_hdcpversion != '2.2'", "This test cases should not be executed once HDCP is not 2.2")
    def test_SiiDrvAdaptSourceHdcpVerGet_HDCP_VER__22(self):
        poHdcpVer = SiiDrvAdaptHdcpVer_t()
        SiiDrvAdaptRxHdcpUsVerGet(self.device.sii_instance, poHdcpVer)
        self.assertEqual(SII_DRV_ADAPTER_HDCP_VER__22, poHdcpVer.value)

# 7.4.4.17 RX HDCP Repeater Mode Get
"""
Get whether Rx work in HDCP repeater mode or receiver mode
"""
class SiiDrvAdaptRxHDCPRepeaterModeSetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpRepeaterModeSet(self):
        poIsDsRepeater = bool_t()
        SiiDrvAdaptRxHdcpRepeaterModeGet(self.device.sii_instance, poIsDsRepeater)

        self.assertTrue(poIsDsRepeater.value,
                        msg="The Rx should be set to Repeater mode when testing this function.")


# 7.4.4.18 RX HDCP Repeater Mode Set
"""
Enable Rx HDCP repeater bit to work as a HDCP repeater

We saw the note in si_drv_adapter_rx.c line#271: This function is only expected to be called when Tx is
used in AVR repeater case.

Issue: I think this Tx should be "RX"? Once this is as expected. How to understand Rx will be set to
       repeater mode when TX is in AVR repeater mode?
"""
class SiiDrvAdaptRxHDCPRepeaterModeGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpRepeaterModeGet(self):
        repeaterMode = bool_t(0)
        SiiDrvAdaptRxHdcpRepeaterModeSet(self.device.sii_instance, repeaterMode)
        poIsDsRepeater = bool_t()
        self.assertFalse(SiiDrvAdaptRxHdcpRepeaterModeGet(self.device.sii_instance, poIsDsRepeater),
                         "Rx Repeater should be set to false")
        repeaterMode = bool_t(1)
        SiiDrvAdaptRxHdcpRepeaterModeSet(self.device.sii_instance, repeaterMode)
        poIsDsRepeater = bool_t()
        self.assertTrue(SiiDrvAdaptRxHdcpRepeaterModeGet(self.device.sii_instance, poIsDsRepeater),
                        "Rx Repeater should be set to true")


# 7.4.4.19 RX HDCP Receiver ID List Valid Get
"""
This function is only expected to be called when Rx is used in AVR repeater case.
"""
class SiiDrvAdaptRxHDCPReceiverIDListValidGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpRxIdListValidGet(self):
        poValid = bool_t()
        SiiDrvAdaptRxHdcpRcvIdListValidGet(self.device.sii_instance, poValid)
        self.assertTrue(poValid.value, "Received ID list should be valid")


"""
This function can be seen in si_drv_adapter_rx.h line#189.
The details and description can be found in "Sii9678 and Sii9679 Software.pdf" page#72.

Issue: This function is not implemented in si_drv_adapter_rx.c and this function is duplicate with the
       "7.4.4.19 RX HDCP Receiver ID List Valid Get" in "Sii9678 and Sii9679 Software.pdf".
"""
# 7.4.4.20 RX HDCP Receiver Id List Valid Set
@unittest.skip("This function is not implemented in si_drv_adapter_rx.c")
class SiiDrvAdaptRxHDCPReceiverIDListValidSetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpRxIdListValidGet(self):
        pass


# 7.4.4.21 RX HDCP Receiver Id List Trigger to Send
"""
This function is only expected to be called when Rx is used in AVR repeater case and the attached device is a repeater.
"""
class SiiDrvAdaptRxHDCPReceiverIdListTriggerTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpRxIdListTriggerToSend(self):
        poValid = bool_t()
        SiiDrvAdaptRxHdcpRcvIdListValidGet(self.device.sii_instance, poValid)
        self.assertFalse(poValid.value,
                         "Received ID list should be invalid because the received ID is not ready to be sent")
        SiiDrvAdaptRxHdcpRxIdListTriggerToSend(self.device.sii_instance)
        poValid = bool_t()
        SiiDrvAdaptRxHdcpRcvIdListValidGet(self.device.sii_instance, poValid)
        self.assertTrue(poValid.value, "Received ID list should be valid")


"""
Clean the HDCP state.
This function is only expected to be called when Rx is used in AVR repeater case.
"""
# 7.4.4.22 Rx HDCP Ri Reset
class SiiDrvAdaptRxHDCPRiResetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpRiReset(self):
        poValid = bool_t()
        SiiDrvAdaptRxHdcpRcvIdListValidGet(self.device.sii_instance, poValid)
        self.assertTrue(poValid.value, "Received ID list should be valid")
        SiiDrvAdaptRxHdcpRiReset(self.device.sii_instance)
        SiiDrvAdaptRxHdcpRcvIdListValidGet(self.device.sii_instance, poValid)
        self.assertFalse(poValid.value, "Received ID list should NOT be valid after HDCP reset")



# 7.4.4.23 RX HDCP Receiver Id List Get
"""
Issue: Not sure about what BKSV/RxID is retrieved?
"""
class SiiDrvAdaptRxHDCPReceiverIdListSetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpRxIdListGet(self):
        poBksvNumber = uint8_t()
        poRevocBuffer = uint8_t()
        bufferSize = uint16_t()
        SiiDrvAdaptRxHdcpRxIdListGet(self.device.sii_instance, poBksvNumber, poRevocBuffer, bufferSize)

        for i in range(bufferSize.value):
            logger.info("RX ID LIST: %02x\n", poRevocBuffer[i])


# 7.4.4.24 RX Receiver ID List Set
"""
Issue: Need to know what arguments should be offered for SiiDrvAdaptRxHdcpRxIdListSet function
"""
def set_fake_Bksv(MaxKsvCount):

    _temp_list = [None] * MaxKsvCount * 5
    for i in range(MaxKsvCount):
        _temp_list[i*5 + 0] = i&0x0ff
        _temp_list[i*5 + 1] = ~_temp_list[i*5 + 0]
        _temp_list[i*5 + 2] = 0x00
        _temp_list[i*5 + 3] = 0xff
        _temp_list[i*5 + 4] = 0xf0

    bksvlist = (uint8_t * (MaxKsvCount * 5))(*_temp_list)
    return bksvlist

class SiiDrvAdaptRxReceiverIdListTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpRxIdListSet(self):
        MAXRXIDCOUNT = 100
        deviceCnt = uint8_t(MAXRXIDCOUNT)
        poDsRxIdList = set_fake_Bksv(MAXRXIDCOUNT)
        offset = uint16_t(0)
        SiiDrvAdaptRxHdcpRxIdListSet(self.device.sii_instance, deviceCnt, poDsRxIdList, offset)
        poBksvNumber = uint8_t()
        poRevocBuffer = uint8_t()
        bufferSize = uint16_t()
        SiiDrvAdaptRxHdcpRxIdListGet(self.device.sii_instance, poBksvNumber, poRevocBuffer, bufferSize)
        for i in range(bufferSize.value):
            logger.info("RX ID LIST: %02x\n", poRevocBuffer[i])

# 7.4.4.25 RX HDCP Topology Get
"""
Issue: Need to know what is the expected value from the returned SiiDrvAdaptHdcpTopology_t struct.
"""
@skipif("self.device.id==0x9394", "Cause python program exception and exit!!!!")
class SiiDrvAdaptRxHDCPTopologyGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpTopologyGet(self):
        poTopology = SiiDrvAdaptHdcpTopology_t()
        SiiDrvAdaptRxHdcpTopologyGet(self.device.sii_instance, byref(poTopology))
        logger.info(poTopology.bHdcp1DeviceDs)
        logger.info(poTopology.bHdcp20DeviceDs)
        logger.info(poTopology.bMaxCascadeExceeded)
        logger.info(poTopology.bMaxDevsExceeded)
        logger.info(poTopology.deviceCount)
        logger.info(poTopology.depth)
        logger.info(poTopology.seqNumV)

# 7.4.4.26 Rx HDCP Topology Set
"""
SiiDrvAdaptHdcpTopology_t:
0    bool_t     bHdcp1DeviceDs;         //HDCP 1.X compliant device in the topology if set to true,
                                        //HDCP 2.X use only
1    bool_t     bHdcp20DeviceDs;        //HDCP 2.0 compliant device in the topology if set to true,
                                        //HDCP 2.X use only
2    bool_t     bMaxCascadeExceeded;    //More than seven level for HDCP 1.X or four levels for HDCP 2.X
                                        //of repeaters cascaded together if set to true
3    bool_t     bMaxDevsExceeded;       //More than 31 devices (for HDCP1.X) or 127 devices (for HDCP
                                        //2.X) as attached if set to true
4    uint8_t    deviceCount;            //Total number of attached downstream devices
5    uint8_t    depth;                  //Repeater cascade depth
6    uint32_t   seqNumV;                //seq_num_V value, HDCP 2.X use only

Issue: Need to know what data should be put in the SiiDrvAdaptHdcpTopology_t structure.
"""
@skipif("self.device.id==0x9394", "Cause python program exception and exit!!!!")
class SiiDrvAdaptRxHDCPTopologySetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpTopologySet(self):

        boot_status = SiiDrvAdaptBootStatus_t()

        SiiDrvAdaptBootStatusGet(self.device.sii_instance, boot_status)
        print boot_status.value

        poTopology = SiiDrvAdaptHdcpTopology_t()
        poTopology.bHdcp1DeviceDs = bool_t(True)
        poTopology.bHdcp20DeviceDs = bool_t(True)
        poTopology.bMaxCascadeExceeded = bool_t(True)
        poTopology.bMaxDevsExceeded = bool_t(True)
        poTopology.deviceCount = uint8_t(2)
        poTopology.depth = uint8_t(3)
        poTopology.seqNumV = uint32_t(4)

        SiiDrvAdaptRxHdcpTopologySet(self.device.sii_instance, poTopology)

        poTopology = SiiDrvAdaptHdcpTopology_t()
        SiiDrvAdaptRxHdcpTopologyGet(self.device.sii_instance, poTopology)
        logger.info(poTopology.bHdcp1DeviceDs)
        logger.info(poTopology.bHdcp20DeviceDs)
        logger.info(poTopology.bMaxCascadeExceeded)
        logger.info(poTopology.bMaxDevsExceeded)
        logger.info(poTopology.deviceCount)
        logger.info(poTopology.depth)
        logger.info(poTopology.seqNumV)

# 7.4.4.27 Rx HDCP Stream Manage Message Get
"""
Get HDCP 2.x stream manage info
"""
@skipif("self.device.us_hdcpversion < '2.0'", "This test cases should not be executed once HDCP is lower than 2")
class SiiDrvAdaptRxHDCPStreamManageMessageGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpStreamManageMsgGet(self):
        poStreamManageInfo = SiiDrvAdaptHdcpStreamManageInfo_t()
        SiiDrvAdaptRxHdcpStreamManageMsgGet(self.device.sii_instance, poStreamManageInfo)
        logger.info(poStreamManageInfo.seqNumM)
        logger.info(poStreamManageInfo.k)
        logger.info(poStreamManageInfo.streamIdType)


"""
Set HDCP 2.x stream manage info

SiiDrvAdaptHdcpStreamManageInfo_t:
0    uint32_t  seqNumM;             //!< The seq_num_M for the RepeaterAuth_Stream_Manage message
1    uint16_t  k;                   //!< The K value for the RepeaterAuth_Stream_Manage message,
                                    //always be 0x001 in HDMI
2    uint16_t  streamIdType[4]      //!< The streamID_Type for the RepeaterAuth_Stream_Manage message,
                                    //the buffer length should be K
"""
# 7.4.4.28 void SiiDrvAdaptRxHdcpStreamManageMsgSet
# noinspection PyCallingNonCallable
@skipif("self.device.us_hdcpversion < '2.0'", "This test cases should not be executed once HDCP is lower than 2")
class SiiDrvAdaptRxHDCPStreamManageMessageSetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptRxHdcpStreamManageMsgSet(self):
        poStreamManageInfo = SiiDrvAdaptHdcpStreamManageInfo_t()
        seqNum = uint32_t(129)
        k = uint16_t(128)
        streamIdType = (uint16_t * 4)()
        poStreamManageInfo.seqNumM = seqNum
        poStreamManageInfo.k = k
        poStreamManageInfo.streamIdType = streamIdType
        SiiDrvAdaptRxHdcpStreamManageMsgSet(self.device.sii_instance, poStreamManageInfo)
        poStreamManageInfo = SiiDrvAdaptHdcpStreamManageInfo_t()
        SiiDrvAdaptRxHdcpStreamManageMsgGet(self.device.sii_instance, poStreamManageInfo)
        logger.info(poStreamManageInfo.seqNumM)
        logger.info(poStreamManageInfo.k)
        logger.info(poStreamManageInfo.streamIdType)


if __name__ == "__main__":
    pass