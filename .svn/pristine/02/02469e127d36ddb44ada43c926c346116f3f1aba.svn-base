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


def resetchip(device):
    with device.evt_subject.listen(SII_DRV_ADAPT_EVENT__VBUS_REQUEST) as evt_listener:
        SiiHalChipReset()
        __event = evt_listener.get(timeout=10)
        if __event is None:
            raise ValueError("Can't get event 'SII_DRV_ADAPT_EVENT__VBUS_REQUEST' in 10s")
    VbusPowerReq = SiiDrvAdaptVbusReq_t()
    # SiiDrvAdaptVbusRequestGet(device.sii_instance, byref(VbusPowerReq))
    # device.assertIn(VbusPowerReq.value, (1, 2), device.__VbusPowerReq_enum[VbusPowerReq.value])
    logger.debug("The VBUS Power request is %s", VbusPowerReq.value)
    if VbusPowerReq.value == SII_DRV_ADAPT_VBUS_REQ__PROVIDE_POWER:
        GPIO_power = bool_t(True)
        SiiDrvAdaptChipGpioCtrl(device.sii_instance, 3, GPIO_power)
        SiiDrvAdaptVbusRequestGrant(device.sii_instance)
        SiiDrvAdaptVbusRequestGet(device.sii_instance, byref(VbusPowerReq))
        #self.assertEqual(VbusPowerReq.value, 0, "The VBUS REQ should be NONE")
        CbusPow = SiiDrvAdaptPow_t(0)
        SiiDrvAdaptCbusPowSet(device.sii_instance, CbusPow)
    if VbusPowerReq.value == SII_DRV_ADAPT_VBUS_REQ__REMOVE_POWER:
        GPIO_power = bool_t(False)
        SiiDrvAdaptChipGpioCtrl(device.sii_instance, 3, GPIO_power)
        SiiDrvAdaptVbusRequestGrant(device.sii_instance)
        SiiDrvAdaptVbusRequestGet(device.sii_instance, byref(VbusPowerReq))
        #self.assertEqual(VbusPowerReq.value, 0, "The VBUS REQ should be NONE")
        CbusPow = SiiDrvAdaptPow_t(1)
        SiiDrvAdaptCbusPowSet(device.sii_instance, CbusPow)
#####Issue for HTC one######
    if VbusPowerReq.value == SII_DRV_ADAPT_VBUS_REQ__NONE:
        GPIO_power = bool_t(True)
        SiiDrvAdaptChipGpioCtrl(device.sii_instance, 3, GPIO_power)
        SiiDrvAdaptVbusRequestGrant(device.sii_instance)
        SiiDrvAdaptVbusRequestGet(device.sii_instance, byref(VbusPowerReq))
        #self.assertEqual(VbusPowerReq.value, 0, "The VBUS REQ should be NONE")
        CbusPow = SiiDrvAdaptPow_t(0)
        SiiDrvAdaptCbusPowSet(device.sii_instance, CbusPow)


class BaseSiiDrvAdaptMhlTestCase(BaseSiiDrvAdaptTestCase):
    def setUp(self):
        if self.device.us_linktype == SII_DRV_LINK_HDMI and self.device.ds_linktype == SII_DRV_LINK_HDMI:
            self.skipTest("Skip test when us_linktype and ds_linktype is SII_DRV_LINK_HDMI")


#7.2.3.1 MHL Link Version Interrogation
class SiiDrvAdaptMhlVersionGetTestCase(BaseSiiDrvAdaptMhlTestCase):
    __Mhlversion_enum = {0: "NONE",
                         1: "MHL12",
                         2: "MHL3"}

    __RxTxLinkType_enum = {0: "DISCONNECTED",
                           1: "HDMI",
                           2: "MHL12",
                           3: "MHL3"}

    def test_SiiDrvAdaptMhlVersionGet(self):
        with self.device.log_subject.listen("AVI INFO recv") as log_listener:
            with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__MHL_VER_CHNG) as cvt_listener:
                logger.debug("Reset chip here!!!!!!!!!!!!")
                resetchip(self.device)
                __event = cvt_listener.get(timeout=10)
                self.assertIsNotNone(__event, "'SII_DRV_ADAPT_EVENT__MHL_VER_CHNG' is sent when bootup.")
            __log = log_listener.get(timeout=10)
            self.assertIsNotNone(__log, "Video and Audio is output")
        RxType = SiiDrvAdaptLinkType_t()
        SiiDrvAdaptRxLinkTypeGet(self.device.sii_instance, byref(RxType))
        logger.debug("The Rx Linktype is %s", self.__RxTxLinkType_enum[RxType.value])
        self.assertEqual(RxType.value, self.device.us_linktype, "Rx Link type Check")
        TxType = SiiDrvAdaptLinkType_t()
        SiiDrvAdaptTxLinkTypeGet(self.device.sii_instance, byref(TxType))
        logger.debug("The Tx Linktype is %s", self.__RxTxLinkType_enum[TxType.value])
        self.assertEqual(TxType.value, self.device.ds_linktype, "Tx Link type Check")
        MhlVersion = SiiDrvAdaptMhlVersion_t()
        SiiDrvAdaptMhlVersionGet(self.device.sii_instance, byref(MhlVersion))
        logger.debug("The MHL Version is %s", self.__Mhlversion_enum[MhlVersion.value])
        if self.device.us_linktype == 2 or self.device.ds_linktype == 2:
            self.assertEqual(MhlVersion.value, 1, "MHL version should be 'MHL12'")
        elif self.device.us_linktype == 3 or self.device.ds_linktype == 3:
            self.assertEqual(MhlVersion.value, 2, "MHL version should be 'MHL3'")
        else:
            self.assertEqual(MhlVersion.value, 0, "MHL version should be 'NONE'")


#7.2.3.2 CBUS Mode Interrogation
class SiiDrvAdaptCbusModeGetTestCase(BaseSiiDrvAdaptMhlTestCase):
    __CbusMode_enum = {0: "SII_DRV_ADAPT_CBUS_MODE__NONE",
                       1: "SII_DRV_ADAPT_CBUS_MODE__OCBUS",
                       2: "SII_DRV_ADAPT_CBUS_MODE__ECBUS_S",
                       4: "SII_DRV_ADAPT_CBUS_MODE__ECBUS_D"}

    def test_SiiDrvAdaptCbusModeGet(self):
        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__CBUS_MODE_CHNG) as cvt_listener:
            SiiHalChipReset()
            __event = cvt_listener.get(timeout=10)
            self.assertIsNotNone(__event, "'SII_DRV_ADAPT_EVENT__CBUS_MODE_CHNG' is sent when bootup.")
        CbusMode = SiiDrvAdaptCbusMode_t()
        SiiDrvAdaptCbusModeGet(self.device.sii_instance, byref(CbusMode))
        self.assertIn(CbusMode.value, self.__CbusMode_enum.keys(), self.__CbusMode_enum[CbusMode.value])
        logger.debug("The Cbus Mode is %s", self.__CbusMode_enum[CbusMode.value])
        logger.debug("The Cbus Mode is %s", CbusMode)


#7.2.3.3 MHL 3 AV Link Data Rate Interrogation
@unittest.skip("SW team not implement yet")
class SiiDrvAdapterAvLinkDataRateGetTestCase(BaseSiiDrvAdaptMhlTestCase):
    pass


#7.2.3.4 CBUS Impedance Control
@unittest.skip("Do not know how to test")
class SiiDrvAdaptRxCbusImpedanceSetTestCase(BaseSiiDrvAdaptMhlTestCase):
    pass
    #TODO


#7.2.3.5 CBUS Event Interrogation
class SiiDrvAdaptCbusEventGetTestCase(BaseSiiDrvAdaptMhlTestCase):
    __CbusEvent_enum = {1: "SII_DRV_ADAPT_CBUS_EVT__NO_PENDING_EVENTS",
                        2: "SII_DRV_ADAPT_CBUS_EVT__MSC_MESSAGE_RECEIVED",
                        4: "SII_DRV_ADAPT_CBUS_EVT__SCRATCH_PAD_CHANGED",
                        8: "SII_DRV_ADAPT_CBUS_EVT__REMOTE_DEVCAP_CHANGED",
                        16: "SII_DRV_ADAPT_CBUS_EVT__FEEDBACK_RECEIVED",
                        32: "SII_DRV_ADAPT_CBUS_EVT__MSC_SENDING_FAILED",
                        64: "SII_DRV_ADAPT_CBUS_EVT__BURST_WRITE_FAILED",
                        128: "SII_DRV_ADAPT_CBUS_EVT__BURST_WRITE_SUCCEEDED",
                        256: "SII_DRV_ADAPT_CBUS_EVT__DEVCAP_NOTIFICATION_FAILED",
                        512: "SII_DRV_ADAPT_CBUS_EVT__DEVCAP_NOTIFICATION_SUCCEEDED",
                        1024: "SII_DRV_ADAPT_CBUS_EVT__MSC_SEND_SUCCESSFULLY"}

    def test_SiiDrvAdaptCbusEventGet(self):
        CbusPow = SiiDrvAdaptPow_t(1)
        SiiDrvAdaptCbusPowSet(self.device.sii_instance, CbusPow)
        SiiDrvAdaptVbusRequestGrant(self.device.sii_instance)
        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__CBUS_EVENT) as cvt_listener:
            resetchip(self.device)
            __event = cvt_listener.get(timeout=10)
            self.assertIsNotNone(__event, "'SII_DRV_ADAPT_EVENT__CBUS_EVENT' is sent when bootup.")
        CbusEvt = SiiDrvAdaptCbusEvt_t()
        SiiDrvAdaptCbusEventGet(self.device.sii_instance, byref(CbusEvt))
        self.assertIn(CbusEvt.value, self.__CbusEvent_enum.keys(), self.__CbusEvent_enum[CbusEvt.value])
        logger.debug("The CBUS event is %s", self.__CbusEvent_enum[CbusEvt.value])


#7.2.3.6 VBUS Event Interrogation
#7.2.3.7 Confirmation of VBUS Request Processing
#7.2.3.8 POW Value of Local DEV_CAT Register Setting
class SiiDrvAdaptVbusRequestGetTestCase(BaseSiiDrvAdaptMhlTestCase):
    __VbusPowerReq_enum = {0: "SII_DRV_ADAPT_VBUS_REQ__NONE",
                           1: "SII_DRV_ADAPT_VBUS_REQ__PROVIDE_POWER",
                           2: "SII_DRV_ADAPT_VBUS_REQ__REMOVE_POWER"}

    def test_SiiDrvAdaptVbusRequestGet(self):
        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__VBUS_REQUEST) as cvt_listener:
            SiiHalChipReset()
            __event = cvt_listener.get(timeout=10)
            self.assertIsNotNone(__event, "'SII_DRV_ADAPT_EVENT__VBUS_REQUEST' is sent when bootup.")
        VbusPowerReq = SiiDrvAdaptVbusReq_t()
        SiiDrvAdaptVbusRequestGet(self.device.sii_instance, byref(VbusPowerReq))
        logger.debug("The VBUS Power request is %s", self.__VbusPowerReq_enum[VbusPowerReq.value])
        if VbusPowerReq.value == SII_DRV_ADAPT_VBUS_REQ__NONE:
            GPIO_power = bool_t(True)
            SiiDrvAdaptChipGpioCtrl(self.device.sii_instance, 3, GPIO_power)
            SiiDrvAdaptVbusRequestGrant(self.device.sii_instance)
            SiiDrvAdaptVbusRequestGet(self.device.sii_instance, byref(VbusPowerReq))
            self.assertEqual(VbusPowerReq.value, 0, "The VBUS REQ should be NONE")
            CbusPow = SiiDrvAdaptPow_t(0)
            SiiDrvAdaptCbusPowSet(self.device.sii_instance, CbusPow)
            with self.device.log_subject.listen("AVI INFO recv") as log_listener:
                __log = log_listener.get(timeout=10)
                self.assertIsNotNone(__log, "Video and Audio is output")
            LocalDevcap = (uint8_t*16)()
            memset(byref(LocalDevcap), 0, sizeof(LocalDevcap))
            SiiDrvAdaptCbusLocalDevcapRead(self.device.sii_instance, LocalDevcap, 0, 16)
            __Devcap_bin = []
            for i in LocalDevcap:
                __Devcap_bin.append(bin(i))
            self.assertEqual(__Devcap_bin[2][-5], "0", "POW is 0")
        if VbusPowerReq.value == SII_DRV_ADAPT_VBUS_REQ__PROVIDE_POWER:
            GPIO_power = bool_t(True)
            SiiDrvAdaptChipGpioCtrl(self.device.sii_instance, 3, GPIO_power)
            SiiDrvAdaptVbusRequestGrant(self.device.sii_instance)
            SiiDrvAdaptVbusRequestGet(self.device.sii_instance, byref(VbusPowerReq))
            self.assertEqual(VbusPowerReq.value, 0, "The VBUS REQ should be NONE")
            CbusPow = SiiDrvAdaptPow_t(0)
            SiiDrvAdaptCbusPowSet(self.device.sii_instance, CbusPow)
            with self.device.log_subject.listen("AVI INFO recv") as log_listener:
                __log = log_listener.get(timeout=10)
                self.assertIsNotNone(__log, "Video and Audio is output")
            LocalDevcap = (uint8_t*16)()
            memset(byref(LocalDevcap), 0, sizeof(LocalDevcap))
            SiiDrvAdaptCbusLocalDevcapRead(self.device.sii_instance, LocalDevcap, 0, 16)
            __Devcap_bin = []
            for i in LocalDevcap:
                __Devcap_bin.append(bin(i))
            self.assertEqual(__Devcap_bin[2][-5], "0", "POW is 0")
        if VbusPowerReq.value == SII_DRV_ADAPT_VBUS_REQ__REMOVE_POWER:
            GPIO_power = bool_t(False)
            SiiDrvAdaptChipGpioCtrl(self.device.sii_instance, 3, GPIO_power)
            SiiDrvAdaptVbusRequestGrant(self.device.sii_instance)
            SiiDrvAdaptVbusRequestGet(self.device.sii_instance, byref(VbusPowerReq))
            self.assertEqual(VbusPowerReq.value, 0, "The VBUS REQ should be NONE")
            CbusPow = SiiDrvAdaptPow_t(1)
            SiiDrvAdaptCbusPowSet(self.device.sii_instance, CbusPow)
            with self.device.log_subject.listen("AVI INFO recv") as log_listener:
                __log = log_listener.get(timeout=10)
                self.assertIsNotNone(__log, "Video and Audio is output")
            LocalDevcap = (uint8_t*16)()
            memset(byref(LocalDevcap), 0, sizeof(LocalDevcap))
            SiiDrvAdaptCbusLocalDevcapRead(self.device.sii_instance, LocalDevcap, 0, 16)
            __Devcap_bin = []
            for i in LocalDevcap:
                __Devcap_bin.append(bin(i))
            self.assertEqual(__Devcap_bin[2][-5], "0", "POW is 1")

    @unittest.skip("test on test_SiiDrvAdaptVbusRequestGet")
    def test_SiiDrvAdaptVbusRequestGrant(self):
        pass

    @unittest.skip("test on test_SiiDrvAdaptVbusRequestGet")
    def test_SiiDrvAdaptCbusPowSet(self):
        pass


#7.2.3.9 Local DEVCAP Registers Reading
#7.2.3.10 Local DEVCAP Video Link Mode Set
#7.2.3.11 Local DEVCAP Audio Link Mode Set
#7.2.3.12 Local DEVCAP Video Type Set
#7.2.3.13 Local DEVCAP Feature Flag Set
#7.2.3.14 Local DEVCAP Registers Writing
#7.2.3.15 Local DEVCAP Value
class SiiDrvAdaptCbusLocalDevcapSetTestCase(BaseSiiDrvAdaptMhlTestCase):

# 1: Sink device
# 2: Source device
# 3: Dongle device

    def setUp(self):
        BaseSiiDrvAdaptMhlTestCase.setUp(self)
        self.backup_devcap = self.ReadDevCap()
        # with self.device.log_subject.listen("AVI INFO recv") as log_listener:
        #     resetchip(self.device)
        #     __log = log_listener.get()
        #     self.assertIsNotNone(__log, "Audio/Video is out")

    def tearDown(self):
        for i in range(0, 7):
            __poData = uint8_t(int(self.backup_devcap[i], 16))
            SiiDrvAdaptCbusLocalDevcapWrite(self.device.sii_instance, __poData, i, 1)
            SiiDrvAdaptCbusTriggerToSendDcapChg(self.device.sii_instance)
            Temp_DevCap = self.ReadDevCap()
            self.assertEqual(__poData.value, int(Temp_DevCap[i], 16), "Write DEVCAP")

    def ReadDevCap(self):
        LocalDevcap = (uint8_t*16)()
        memset(byref(LocalDevcap), 0, sizeof(LocalDevcap))
        SiiDrvAdaptCbusLocalDevcapRead(self.device.sii_instance, LocalDevcap, 0, 16)
        Devcap = []
        Devcap_bin = []
        for i in LocalDevcap:
            Devcap.append(hex(i))
            Devcap_bin.append(bin(i))
        logger.debug("Local Devcap (Hex) is %s", Devcap)
        logger.debug("Local Devcap (Bin) is %s", Devcap_bin)
        return Devcap

    def test_SiiDrvAdaptCbusLocalDevcapRead(self):
        Localdevcap = self.ReadDevCap()
        if self.device.id == "0x9679":
            self.assertEqual(Localdevcap[2][3], "1", "This is Rx")
        if self.device.id == "0x9678":
            self.assertEqual(Localdevcap[2][3], "2", "This is Tx")
        if self.device.id == "0x9394":
            self.assertEqual(Localdevcap[2][3], "3", "This is Dongle")

    def test_SiiDrvAdaptCbusLocalDevcapVideoLinkModeSet(self):
        __vidLinkMode_enum = {
            SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_VGA: "SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_VGA",
            SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_ISLANDS: "SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_ISLANDS",
            SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_PPIXEL: "SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_PPIXEL",
            SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_YCBCR422: "SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_YCBCR422",
            SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_YCBCR444: "SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_YCBCR444",
            SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_RGB444: "SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_RGB444",
            SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_NONE: "SII_DRV_ADAPT_DEVCAP_VID_LINK_MODE__SUPP_NONE"}
        for mode in __vidLinkMode_enum.keys():
            vidLinkMode = SiiDrvAdaptDevCapVidLinkMode_t(mode)
            SiiDrvAdaptCbusLocalDevcapVideoLinkModeSet(self.device.sii_instance, vidLinkMode)
            SiiDrvAdaptCbusTriggerToSendDcapChg(self.device.sii_instance)
            Temp_DevCap = self.ReadDevCap()
            self.assertEqual(Temp_DevCap[5], hex(mode), __vidLinkMode_enum[mode] + " set in devcap")

    def test_SiiDrvAdaptCbusLocalDevcapAudioLinkModeSet(self):
        __audLinkMode_enum = {
            SII_DRV_ADAPT_DEVCAP_AUD_LINK_MODE__NONE: "SII_DRV_ADAPT_DEVCAP_AUD_LINK_MODE__NONE",
            SII_DRV_ADAPT_DEVCAP_AUD_LINK_MODE__AUD_2CH: "SII_DRV_ADAPT_DEVCAP_AUD_LINK_MODE__AUD_2CH",
            SII_DRV_ADAPT_DEVCAP_AUD_LINK_MODE__AUD_8CH: "SII_DRV_ADAPT_DEVCAP_AUD_LINK_MODE__AUD_8CH"}
        for mode in __audLinkMode_enum.keys():
            audLinkMode = SiiDrvAdaptDevCapAudLinkMode_t(mode)
            SiiDrvAdaptCbusLocalDevcapAudioLinkModeSet(self.device.sii_instance, audLinkMode)
            SiiDrvAdaptCbusTriggerToSendDcapChg(self.device.sii_instance)
            Temp_DevCap = self.ReadDevCap()
            self.assertEqual(Temp_DevCap[6], hex(mode), __audLinkMode_enum[mode] + " set in devcap")

    def test_SiiDrvAdaptCbusLocalDevcapVideoTypeSet(self):
        __videoType_enum = {
            SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__NONE: "SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__NONE",
            SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__VT_GRAPHICS: "SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__VT_GRAPHICS",
            SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__VT_PHOTO: "SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__VT_PHOTO",
            SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__VT_CINEMA: "II_DRV_ADAPT_DEVCAP_VIDEO_TYPE__VT_CINEMA",
            SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__VT_GAME: "SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__VT_GAME",
            #bit[6:7]: reserved
            SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__SUPP_VT: "SII_DRV_ADAPT_DEVCAP_VIDEO_TYPE__SUPP_VT"}
        for mode in __videoType_enum.keys():
            videoType = SiiDrvAdaptDevCapVideoType_t(mode)
            SiiDrvAdaptCbusLocalDevcapVideoTypeSet(self.device.sii_instance, videoType)
            SiiDrvAdaptCbusTriggerToSendDcapChg(self.device.sii_instance)
            Temp_DevCap = self.ReadDevCap()
            self.assertEqual(Temp_DevCap[7], hex(mode), __videoType_enum[mode] + " set in devcap")

    def test_SiiDrvAdaptCbusLocalDevcapFeatureFlagSet(self):
        __featureFlag_enum = {
            SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__NONE: "SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__NONE",
            SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__RCP_SUPPORT: "SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__RCP_SUPPORT",
            SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__RAP_SUPPORT: "SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__RAP_SUPPORT",
            SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__SP_SUPPORT: "SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__SP_SUPPORT",
            SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__UCP_SEND_SUPPORT: "SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__UCP_SEND_SUPPORT",
            SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__UCP_RCVD_SUPPORT: "SII_DRV_ADAPT_DEVCAP_FEATURE_FLAG__UCP_RCVD_SUPPORT"}
            #bit[7:5]: reserved
        for mode in __featureFlag_enum.keys():
            featureFlag = SiiDrvAdaptDevCapFeatureFlag_t(mode)
            SiiDrvAdaptCbusLocalDevcapFeatureFlagSet(self.device.sii_instance, featureFlag)
            SiiDrvAdaptCbusTriggerToSendDcapChg(self.device.sii_instance)
            Temp_DevCap = self.ReadDevCap()
            self.assertEqual(Temp_DevCap[10], hex(mode), __featureFlag_enum[mode] + " set in devcap")

    def test_SiiDrvAdaptCbusLocalDevcapWrite(self):
        self.tearDown()

    @unittest.skip("send DCAP_CHG to remote peer device, cannot check local")
    def test_SiiDrvAdaptCbusTriggerToSendDcapChg(self):
        pass


#7.2.3.16 Remote DEVCAP Registers Reading
class SiiDrvAdaptCbusRemoteDevcapReadTestCase(BaseSiiDrvAdaptMhlTestCase):

    def test_SiiDrvAdaptCbusRemoteDevcapRead(self):
        RemoteDevcap = (uint8_t*16)()
        memset(byref(RemoteDevcap), 0, sizeof(RemoteDevcap))
        SiiDrvAdaptCbusRemoteDevcapRead(self.device.sii_instance, RemoteDevcap, 0, 16)
        __Devcap = []
        __Devcap_bin = []
        for i in RemoteDevcap:
            __Devcap.append("0x%x" % i)
            __Devcap_bin.append(bin(i))
        logger.debug("Remote Devcap (Hex) is %s", __Devcap)
        logger.debug("Remote Devcap (Bin) is %s", __Devcap_bin)
        # if hex(self.device.id) == "0x9679":
        #     self.assertEqual(__Devcap[2][3], "1", "This is Rx")
        # if hex(self.device.id) == "0x9678":
        #     self.assertEqual(__Devcap[2][3], "2", "This is Tx")
        # if hex(self.device.id) == "0x9394":
        #     self.assertEqual(__Devcap[2][3], "3", "This is Dongle")


#7.2.3.17 Received MSC Message Withdrawal
class SiiDrvAdaptCbusMscMessageReceiveTestCase(BaseSiiDrvAdaptMhlTestCase):
    pass
    #TODO


#7.2.3.18 Received MSC Message Feedback Withdrawal
class SiiDrvAdaptCbusFeedbackReceiveTestCase(BaseSiiDrvAdaptMhlTestCase):
    pass
    #TODO


#7.2.3.19 MSC Message Sending
class SiiDrvAdaptCbusMscMessageSendTestCase(BaseSiiDrvAdaptMhlTestCase):
    pass
    #TODO


#7.2.3.20 Remote Scratch Pad Data Write
class SiiDrvAdaptCbusRemoteScratchPadWriteTestCase(BaseSiiDrvAdaptMhlTestCase):
    pass
    #TODO


#7.2.3.21 Received MSC Message Confirmation
class SiiDrvAdaptCbusMscFeedbackSendTestCase(BaseSiiDrvAdaptMhlTestCase):
    pass
    #TODO


#7.2.3.22 Current CBUS Status Interrogation
class SiiDrvAdaptCbusStateGetTestCase(BaseSiiDrvAdaptMhlTestCase):
    pass
    #TODO


#7.2.3.23 MHL 3 BIST Test Configuration Set
#7.2.3.24 MHL 3 BIST Test Configuration Get
#7.2.3.25 MHL 3 BIST Test Result Get
#7.2.3.26 MHL 3 BIST Status Get
#7.2.3.27 MHL 3 BIST Test Enable
@unittest.skip("BIST can start but never ending")
class SiiDrvAdapterMHL3BistTestCase(BaseSiiDrvAdaptMhlTestCase):
    # ('ucEcbusDuration', uint8_t),
    # ('ucEcbusPattern', uint8_t),
    # ('ucEcbusFixedH', uint8_t),
    # ('ucEcbusFixedL', uint8_t),
    # ('ucAvLinkDataRate', uint8_t),
    # ('ucAvLinkPattern', uint8_t),
    # ('ucAvLinkVideoMode', uint8_t),
    # ('ucAvLinkDuration', uint8_t),
    # ('ucAvLinkFixedH', uint8_t),
    # ('ucAvLinkFixedL', uint8_t),
    # ('ucAvLinkRandomizer', uint8_t),
    # ('ucImpedanceMode', uint8_t),
    # ('ucTriggerData', uint8_t),

    def test_SiiDrvAdapterMHL3BistConfigSet(self):
        bistconfig = SiiDrvAdaptBistConf_t()
        bistconfig.ucEcbusDuration = 16
        bistconfig.ucEcbusPattern = 1
        bistconfig.ucEcbusFixedH = 0
        bistconfig.ucEcbusFixedL = 0
        bistconfig.ucAvLinkDataRate = 1
        bistconfig.ucAvLinkPattern = 1
        bistconfig.ucAvLinkVideoMode = 2
        bistconfig.ucAvLinkDuration = 16
        bistconfig.ucAvLinkFixedH = 0
        bistconfig.ucAvLinkFixedL = 0
        bistconfig.ucAvLinkRandomizer = 2
        bistconfig.ucImpedanceMode = 0
        bistconfig.ucTriggerData = 64
        SiiDrvAdaptMHL3BistConfigSet(self.device.sii_instance, byref(bistconfig))
        SiiDrvAdaptMHL3BistConfigGet(self.device.sii_instance, byref(bistconfig))
        # bistconfig = SiiDrvAdaptBistConf_t()
        # SiiDrvAdaptMHL3BistConfigGet(self.device.sii_instance, byref(bistconfig))
        logger.debug("ucEcbusDuration is %s", bistconfig.ucEcbusDuration)
        logger.debug("ucEcbusPattern is %s", bistconfig.ucEcbusPattern)
        logger.debug("ucEcbusFixedH is %s", bistconfig.ucEcbusFixedH)
        logger.debug("ucEcbusFixedL is %s", bistconfig.ucEcbusFixedL)
        logger.debug("ucAvLinkDataRate is %s", bistconfig.ucAvLinkDataRate)
        logger.debug("ucAvLinkPattern is %s", bistconfig.ucAvLinkPattern)
        logger.debug("ucAvLinkVideoMode is %s", bistconfig.ucAvLinkVideoMode)
        logger.debug("ucAvLinkDuration is %s", bistconfig.ucAvLinkDuration)
        logger.debug("ucAvLinkFixedH is %s", bistconfig.ucAvLinkFixedH)
        logger.debug("ucAvLinkFixedL is %s", bistconfig.ucAvLinkFixedL)
        logger.debug("ucAvLinkRandomizer is %s", bistconfig.ucAvLinkRandomizer)
        logger.debug("ucImpedanceMode is %s", bistconfig.ucImpedanceMode)
        logger.debug("ucTriggerData is %s", bistconfig.ucTriggerData)
        poBistStatus = SiiDrvAdaptBistStatus_t()
        SiiDrvAdaptMHL3BistStatusGet(self.device.sii_instance, byref(poBistStatus))
        logger.debug("Bist Status is %s", poBistStatus.value)
        bBistEnable = bool_t(True)
        SiiDrvAdaptMHL3BistEnable(self.device.sii_instance, bBistEnable)
        while 1:
            time.sleep(5)
            SiiDrvAdaptMHL3BistStatusGet(self.device.sii_instance, byref(poBistStatus))
            logger.debug("Bist Status is %s", poBistStatus.value)
            if poBistStatus.value == SII_DRV_ADAPT_BIST__SUCCESS:
                break
        poBistReturn = SiiDrvAdaptBistReturn_t()
        SiiDrvAdaptMHL3BistResultGet(self.device.sii_instance, byref(poBistReturn))
        logger.debug("Result is %s", poBistReturn.eCbusStatH)

    def test_SiiDrvAdapterMHL3BistConfigGet(self):
        bistconfig = SiiDrvAdaptBistConf_t()
        SiiDrvAdaptMHL3BistConfigGet(self.device.sii_instance, byref(bistconfig))
        logger.debug("ucEcbusDuration is %s", bistconfig.ucEcbusDuration)
        logger.debug("ucEcbusPattern is %s", bistconfig.ucEcbusPattern)
        logger.debug("ucEcbusFixedH is %s", bistconfig.ucEcbusFixedH)
        logger.debug("ucEcbusFixedL is %s", bistconfig.ucEcbusFixedL)
        logger.debug("ucAvLinkDataRate is %s", bistconfig.ucAvLinkDataRate)
        logger.debug("ucAvLinkPattern is %s", bistconfig.ucAvLinkPattern)
        logger.debug("ucAvLinkVideoMode is %s", bistconfig.ucAvLinkVideoMode)
        logger.debug("ucAvLinkDuration is %s", bistconfig.ucAvLinkDuration)
        logger.debug("ucAvLinkFixedH is %s", bistconfig.ucAvLinkFixedH)
        logger.debug("ucAvLinkFixedL is %s", bistconfig.ucAvLinkFixedL)
        logger.debug("ucAvLinkRandomizer is %s", bistconfig.ucAvLinkRandomizer)
        logger.debug("ucImpedanceMode is %s", bistconfig.ucImpedanceMode)
        logger.debug("ucTriggerData is %s", bistconfig.ucTriggerData)

    def test_SiiDrvAdapterMHL3BistResultGet(self):
        pass

    def test_SiiDrvAdapterMHL3BistStatusGet(self):
        pass

    def test_SiiDrvAdapterMHL3BistEnable(self):
        pass

