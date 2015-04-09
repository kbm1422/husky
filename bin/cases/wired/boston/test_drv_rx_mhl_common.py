#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from ctypes import byref

from base import BaseBostonDriverTestCase
from simg.test.framework import name, parametrize, skip, LinkedTestCase, TestContextManager
from simg.devadapter.wired.base import Mhl2Interface, Mhl3Interface, MscMessage
from simg.devadapter.wired.boston.Sii9777RxLib import *


__all__ = [
    "RxCdSenseQueryTestCase",
    "MHLVersionQueryTestCase",
    "CbusModeQueryTestCase",
    "CbusEventQueryTestCase",
    "VbusRequestGrantQueryTestCase",
    "CbusLocalDevCapTestCase",
    "CbusLocalDevcapPowTestCase",
    "CbusLocalDevcapVideoLinkModeTestCase",
    "CbusLocalDevcapAudioLinkModeTestCase",
    "CbusLocalDevcapVideoTypeTestCase",
    "CbusLocalDevcapFeatureFlagTestCase",
    "CbusRemoteDevcapQueryTestCase",
    "CbusMscMsgSendReceiveTestCase",
]

CD_SENSE = {
    "SII9777_CD_SENSE__NONE": SII9777_CD_SENSE__NONE,
    "SII9777_CD_SENSE__MHL_CABLE": SII9777_CD_SENSE__MHL_CABLE
}

MHL_VERSION = {
    "SII9777_MHL_VERSION__NONE": SII9777_MHL_VERSION__NONE,
    "SII9777_MHL_VERSION__MHL12": SII9777_MHL_VERSION__MHL12,
    "SII9777_MHL_VERSION__MHL3": SII9777_MHL_VERSION__MHL3
}

VBUS_REQ = {
    "SII9777_VBUS_REQ__NONE": SII9777_VBUS_REQ__NONE,
    "SII9777_VBUS_REQ__PROVIDE_POWER": SII9777_VBUS_REQ__PROVIDE_POWER,
    "SII9777_VBUS_REQ__REMOVE_POWER": SII9777_VBUS_REQ__REMOVE_POWER
}

CBUS_EVTS = {
    "SII9777_CBUS_EVT__NO_PENDING_EVENTS": SII9777_CBUS_EVT__NO_PENDING_EVENTS,                          # 0x0001
    "SII9777_CBUS_EVT__MSC_MESSAGE_RECEIVED": SII9777_CBUS_EVT__MSC_MESSAGE_RECEIVED,                    # 0x0002
    "SII9777_CBUS_EVT__SCRATCH_PAD_CHANGED": SII9777_CBUS_EVT__SCRATCH_PAD_CHANGED,                      # 0x0004
    "SII9777_CBUS_EVT__REMOTE_DEVCAP_CHANGED": SII9777_CBUS_EVT__REMOTE_DEVCAP_CHANGED,                  # 0x0008
    "SII9777_CBUS_EVT__FEEDBACK_RECEIVED": SII9777_CBUS_EVT__FEEDBACK_RECEIVED,                          # 0x0010
    "SII9777_CBUS_EVT__MSC_SENDING_FAILED": SII9777_CBUS_EVT__MSC_SENDING_FAILED,                        # 0x0020
    "SII9777_CBUS_EVT__BURST_WRITE_FAILED": SII9777_CBUS_EVT__BURST_WRITE_FAILED,                        # 0x0040
    "SII9777_CBUS_EVT__BURST_WRITE_SUCCEEDED": SII9777_CBUS_EVT__BURST_WRITE_SUCCEEDED,                  # 0x0080
    "SII9777_CBUS_EVT__DEVCAP_NOTIFICATION_FAILED": SII9777_CBUS_EVT__DEVCAP_NOTIFICATION_FAILED,        # 0x0100
    "SII9777_CBUS_EVT__DEVCAP_NOTIFICATION_SUCCEEDED": SII9777_CBUS_EVT__DEVCAP_NOTIFICATION_SUCCEEDED,  # 0x0200
    "SII9777_CBUS_EVT__MSC_SEND_SUCCESSFULLY": SII9777_CBUS_EVT__MSC_SEND_SUCCESSFULLY,                  # 0x0400
}

CBUS_MODES = {
    "SII9777_CBUS_MODE__NONE": SII9777_CBUS_MODE__NONE,             # 0x00
    "SII9777_CBUS_MODE__OCBUS": SII9777_CBUS_MODE__OCBUS,           # 0x01 MHL12 75Mbps
    "SII9777_CBUS_MODE__ECBUS_S": SII9777_CBUS_MODE__ECBUS_S,       # 0x02 MHL3
    "SII9777_CBUS_MODE__ECBUS_D": SII9777_CBUS_MODE__ECBUS_D        # 0x04 600Mbps
}

VID_LINK_MODES = {
    "SII9777_DEVCAP_VID_LINK_MODE__SUPP_NONE": SII9777_DEVCAP_VID_LINK_MODE__SUPP_NONE,             # 0x00
    "SII9777_DEVCAP_VID_LINK_MODE__SUPP_RGB444": SII9777_DEVCAP_VID_LINK_MODE__SUPP_RGB444,         # 0x01
    "SII9777_DEVCAP_VID_LINK_MODE__SUPP_YCBCR444": SII9777_DEVCAP_VID_LINK_MODE__SUPP_YCBCR444,     # 0x02
    "SII9777_DEVCAP_VID_LINK_MODE__SUPP_YCBCR422": SII9777_DEVCAP_VID_LINK_MODE__SUPP_YCBCR422,     # 0x04
    "SII9777_DEVCAP_VID_LINK_MODE__SUPP_PPIXEL": SII9777_DEVCAP_VID_LINK_MODE__SUPP_PPIXEL,         # 0x08
    "SII9777_DEVCAP_VID_LINK_MODE__SUPP_ISLANDS": SII9777_DEVCAP_VID_LINK_MODE__SUPP_ISLANDS,       # 0X10
    "SII9777_DEVCAP_VID_LINK_MODE__SUPP_VGA": SII9777_DEVCAP_VID_LINK_MODE__SUPP_VGA,               # 0X20
}

VBUS_POWER = {
    "SII9777_VBUS_REMOVE_POWER": SII9777_VBUS_REMOVE_POWER,
    "SII9777_VBUS_PROVIDE_POWER": SII9777_VBUS_PROVIDE_POWER
}

AUD_LINK_MODES = {
    "SII9777_DEVCAP_AUD_LINK_MODE__NONE": SII9777_DEVCAP_VID_LINK_MODE__SUPP_NONE,              # 0x00
    "SII9777_DEVCAP_AUD_LINK_MODE__AUD_2CH": SII9777_DEVCAP_VID_LINK_MODE__SUPP_RGB444,         # 0x01
    "SII9777_DEVCAP_AUD_LINK_MODE__AUD_8CH": SII9777_DEVCAP_VID_LINK_MODE__SUPP_YCBCR444,       # 0x02
}

VIDEO_TYPES = {
    "SII9777_DEVCAP_VIDEO_TYPE__NONE": SII9777_DEVCAP_VIDEO_TYPE__NONE,                 # 0x00
    "SII9777_DEVCAP_VIDEO_TYPE__VT_GRAPHICS": SII9777_DEVCAP_VIDEO_TYPE__VT_GRAPHICS,   # 0x01
    "SII9777_DEVCAP_VIDEO_TYPE__VT_PHOTO": SII9777_DEVCAP_VIDEO_TYPE__VT_PHOTO,         # 0x02
    "SII9777_DEVCAP_VIDEO_TYPE__VT_CINEMA": SII9777_DEVCAP_VIDEO_TYPE__VT_CINEMA,       # 0x04
    "SII9777_DEVCAP_VIDEO_TYPE__VT_GAME": SII9777_DEVCAP_VIDEO_TYPE__VT_GAME,           # 0x08
    "SII9777_DEVCAP_VIDEO_TYPE__SUPP_VT": SII9777_DEVCAP_VIDEO_TYPE__SUPP_VT            # 0x80
}

FEATURE_FLAGS = {
    "SII9777_DEVCAP_FEATURE_FLAG__NONE": SII9777_DEVCAP_FEATURE_FLAG__NONE,                             # 0x00
    "SII9777_DEVCAP_FEATURE_FLAG__RCP_SUPPORT": SII9777_DEVCAP_FEATURE_FLAG__RCP_SUPPORT,               # 0x01
    "SII9777_DEVCAP_FEATURE_FLAG__RAP_SUPPORT": SII9777_DEVCAP_FEATURE_FLAG__RAP_SUPPORT,               # 0x02
    "SII9777_DEVCAP_FEATURE_FLAG__SP_SUPPORT": SII9777_DEVCAP_FEATURE_FLAG__SP_SUPPORT,                 # 0x04
    "SII9777_DEVCAP_FEATURE_FLAG__UCP_SEND_SUPPORT": SII9777_DEVCAP_FEATURE_FLAG__UCP_SEND_SUPPORT,     # 0x08
    "SII9777_DEVCAP_FEATURE_FLAG__UCP_RCVD_SUPPORT": SII9777_DEVCAP_FEATURE_FLAG__UCP_RCVD_SUPPORT,     # 0x10
    "SII9777_DEVCAP_FEATURE_FLAG__XVYCC_SUPPORT": SII9777_DEVCAP_FEATURE_FLAG__XVYCC_SUPPORT,           # 0x20
    "SII9777_DEVCAP_FEATURE_FLAG__RBP_SUPPORT": SII9777_DEVCAP_FEATURE_FLAG__RBP_SUPPORT,               # 0x40
}


@parametrize("expect_cd_sense", type=str, choice=CD_SENSE)
class RxCdSenseQueryTestCase(BaseBostonDriverTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Sii9777RxCdSenseQuery(self):
        self.pCdSense = Sii9777CdSense_t()
        with self.device.lock:
            retcode = Sii9777RxCdSenseQuery(self.device.drv_instance, byref(self.pCdSense))
        self._test_api_retcode("Sii9777RxCdSenseQuery", retcode)

        self.assertEqual(self.pCdSense.value, CD_SENSE[self.expect_cd_sense],
                         "The MHL Cable Detect Sense State should be %s" % self.expect_cd_sense)


@parametrize("expect_mhl_version", type=str, choice=MHL_VERSION)
class MHLVersionQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777MHLVersionQuery(self):
        pMhlVersion = Sii9777MhlVersion_t()
        with self.device.lock:
            retcode = Sii9777MHLVersionQuery(self.device.drv_instance, byref(pMhlVersion))
        self._test_api_retcode("Sii9777MHLVersionQuery", retcode)

        self.assertEqual(pMhlVersion.value, MHL_VERSION[self.expect_mhl_version],
                         "The MHL Version should be %s." % self.expect_mhl_version)


@parametrize("expect_cbus_mode", type=str, choice=CBUS_MODES)
class CbusModeQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777CbusModeQuery(self):
        pCbusMode = Sii9777CbusMode_t()
        with self.device.lock:
            retcode = Sii9777CbusModeQuery(self.device.drv_instance, byref(pCbusMode))
        self._test_api_retcode("Sii9777CbusModeQuery", retcode)

        self.assertEqual(pCbusMode.value, CBUS_MODES[self.expect_cbus_mode],
                         "The CBUS mode should be %s." % self.expect_cbus_mode)



@parametrize("peer_device", type=Mhl2Interface, fetch=parametrize.FetchType.LAZY)
class CbusEventQueryTestCase(BaseBostonDriverTestCase):
    def test_SII9777_CBUS_EVT__NO_PENDING_EVENTS(self):
        pass

    def test_SII9777_CBUS_EVT__MSC_MESSAGE_RECEIVED(self):
        self.peer_device.send_msc_message(MscMessage(0x10, 0x00))
        pCbusEvent = Sii9777CbusEvt_t()
        with self.device.lock:
            retcode = Sii9777CbusEventQuery(self.device.drv_instance, byref(pCbusEvent))
        self._test_api_retcode("Sii9777CbusEventQuery", retcode)
        self.assertTrue(pCbusEvent.value & SII9777_CBUS_EVT__MSC_MESSAGE_RECEIVED,
                        "Sii9777CbusEventQuery should get event SII9777_CBUS_EVT__MSC_MESSAGE_RECEIVED")

    @skip("TODO")
    def test_SII9777_CBUS_EVT__SCRATCH_PAD_CHANGED(self):
        pass

    @skip("TODO")
    def test_SII9777_CBUS_EVT__REMOTE_DEVCAP_CHANGED(self):
        self.peer_device.set_local_devcap()

    def test_SII9777_CBUS_EVT__FEEDBACK_RECEIVED(self):
        self.device.send_msc_message(MscMessage(0x10, 0x00))
        pCbusEvent = Sii9777CbusEvt_t()
        with self.device.lock:
            retcode = Sii9777CbusEventQuery(self.device.drv_instance, byref(pCbusEvent))
        self._test_api_retcode("Sii9777CbusEventQuery", retcode)
        self.assertTrue(pCbusEvent.value & SII9777_CBUS_EVT__FEEDBACK_RECEIVED,
                        "Sii9777CbusEventQuery should get event SII9777_CBUS_EVT__FEEDBACK_RECEIVED")

    @skip("how to make msc sending failed")
    def test_SII9777_CBUS_EVT__MSC_SENDING_FAILED(self):
        pass

    @skip("TODO")
    def test_SII9777_CBUS_EVT__BURST_WRITE_FAILED(self):
        pass

    @skip("TODO")
    def test_SII9777_CBUS_EVT__BURST_WRITE_SUCCEEDED(self):
        pass

    @skip("how to make devcap notification failed")
    def test_SII9777_CBUS_EVT__DEVCAP_NOTIFICATION_FAILED(self):
        pass

    @skip("TODO")
    def test_SII9777_CBUS_EVT__DEVCAP_NOTIFICATION_SUCCEEDED(self):
        pCbusEvent = Sii9777CbusEvt_t()
        with self.device.lock:
            retcode = Sii9777CbusEventQuery(self.device.drv_instance, byref(pCbusEvent))
        self._test_api_retcode("Sii9777CbusEventQuery", retcode)
        self.assertTrue(pCbusEvent.value & SII9777_CBUS_EVT__DEVCAP_NOTIFICATION_SUCCEEDED,
                        "Sii9777CbusEventQuery should get event SII9777_CBUS_EVT__DEVCAP_NOTIFICATION_SUCCEEDED")

    def test_SII9777_CBUS_EVT__MSC_SEND_SUCCESSFULLY(self):
        self.device.send_msc_message(MscMessage(0x10, 0x00))
        pCbusEvent = Sii9777CbusEvt_t()
        with self.device.lock:
            retcode = Sii9777CbusEventQuery(self.device.drv_instance, byref(pCbusEvent))
        self._test_api_retcode("Sii9777CbusEventQuery", retcode)
        self.assertTrue(pCbusEvent.value & SII9777_CBUS_EVT__MSC_SEND_SUCCESSFULLY,
                        "Sii9777CbusEventQuery should get event SII9777_CBUS_EVT__MSC_SEND_SUCCESSFULLY")


@skip("TODO")
class VbusRequestGrantQueryTestCase(BaseBostonDriverTestCase):
    """
    ┌──────────────────────────────┐
    │VbusRequestQuery:                                           │
    ├──────────────────────────────┤
    │This function returns current VBUS power request.           │
    │An MHL device may provide power in Sink to Source or in     │
    │Source to Sink directions. The direction is negotiated      │
    │during the discovery process. The VBUS power switch,        │
    │however, is outside the SiI9777 and must be controlled by   │
    │the application. The driver generates a                     │
    │SII9777_EVT__VBUS_REQUEST event whenever such control is    │
    │needed. This function is expected to be called on this      │
    │notification and return the request value. The application  │
    │is required to enable or disable VBUS power according to    │
    │the request and then call Sii9777VbusRequestGrant() to      │
    │indicate that the request is processed and allow the MHL    │
    │device to continue the discovery process or power mode      │
    │changing.                                                   │
    ├──────────────────────────────┤
    │VbusGrantQuery:                                             │
    ├──────────────────────────────┤
    │This function must be called only after the VBUS power is   │
    │provided or removed per the request given through the       │
    │Sii9777VbusRequestQuery() function. After calling           │
    │Sii9777VbusRequestGrant(), the request changes to           │
    │SII9777_VBUS_REQ__NONE until a new request is generated.    │
    └──────────────────────────────┘
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    """
    Per the
        "The VBUS power switch, however, is outside the SiI9777 and must be controlled by the application. The
        driver generates a SII9777_EVT__VBUS_REQUEST event whenever such control is needed."
    TODO: we need to know how to request the VBUS power control through API invoke.
    """

    def _request_grant_vbus_power(self):
        self.pRequest = Sii9777VbusReq_t()
        with self.device.lock:
            retcode = Sii9777VbusRequestQuery(self.device.drv_instance, self.pRequest)
        self._test_api_retcode("Sii9777VbusRequestQuery", retcode)

        with self.device.lock:
            retcode = Sii9777VbusRequestGrant(self.device.drv_instance)
        self._test_api_retcode("Sii9777VbusRequestGrant", retcode)

    def test_SII9777_VBUS_REQ__NONE(self):
        self._request_grant_vbus_power()

        self.pRequest = Sii9777VbusReq_t()
        with self.device.lock:
            retcode = Sii9777VbusRequestQuery(self.device.drv_instance, self.pRequest)
        self._test_api_retcode("Sii9777VbusRequestQuery", retcode)

        self.assertEqual(SII9777_VBUS_REQ__NONE, self.pRequest)


@name("Sii9777CbusLocalDevcapSet, Sii9777CbusLocalDevcapGet, Sii9777CbusDcapChgSend, \
Sii9777CbusEventQuery(SII9777_CBUS_EVT__DEVCAP_NOTIFICATION_SUCCEEDED)")
@parametrize("peer_device", type=Mhl2Interface, fetch=parametrize.FetchType.LAZY)
class CbusLocalDevCapTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_golden_local_devcap",
        "test_Sii9777CbusLocalDevcapSet"
    )

    GOLDEN_LOCAL_DEVCAP = [
        0x00, 0x32, 0x31, 0x01, 0x41, 0x7F, 0x01, 0x8F, 0x41, 0x0F, 0x07, 0x97, 0x77, 0x10, 0x33, 0x00
    ]

    def tearDown(self):
        self.device.set_local_devcap(self.GOLDEN_LOCAL_DEVCAP)

    def test_golden_local_devcap(self):
        pData = (uint8_t * 16)()
        offset = uint8_t(0)
        length = uint8_t(16)
        with self.device.lock:
            retcode = Sii9777CbusLocalDevcapGet(self.device.drv_instance, pData, offset, length)
        self._test_api_retcode("Sii9777CbusLocalDevcapGet", retcode)
        actual_local_devcap = [pData[index] for index in range(16)]
        self.assertSequenceEqual(actual_local_devcap, self.GOLDEN_LOCAL_DEVCAP,
                                 "should get the same devcap as golden local devcap")

    def test_Sii9777CbusLocalDevcapSet(self):
        expect_local_devcap = [0x00, 0x30, 0x21, 0x00, 0x42, 0x7F, 0x07, 0x8F,
                               0x41, 0x0F, 0x5F, 0x97, 0x77, 0x10, 0x33, 0x00]
        pData = (uint8_t * 16)()
        for index in range(16):
            pData[index] = expect_local_devcap[index]
        offset = uint8_t(0)
        length = uint8_t(16)
        with self.device.lock:
            retcode = Sii9777CbusLocalDevcapSet(self.device.drv_instance, pData, offset, length)
        self._test_api_retcode("Sii9777CbusLocalDevcapSet", retcode)

        actual_local_devcap = self.device.get_local_devcap()
        self.assertSequenceEqual(actual_local_devcap, expect_local_devcap,
                                 "should get the same devcap as expect local devcap")

        with self.device.lock:
            retcode = Sii9777CbusDcapChgSend(self.device.drv_instance)
        self._test_api_retcode("Sii9777CbusDcapChgSend", retcode)

        gotten_devcap = self.peer_device.get_remote_devcap()
        self.assertSequenceEqual(gotten_devcap, expect_local_devcap,
                                 "The peer device get remote devcap should same with boston local devcap")


class CbusLocalDevcapPowTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_golden_local_devcap_pow",
        "test_Sii9777CbusLocalDevcapPowSet_SII9777_VBUS_REMOVE_POWER",
        "test_Sii9777CbusLocalDevcapPowSet_SII9777_VBUS_PROVIDE_POWER"
    )

    def test_golden_local_devcap_pow(self):
        pCbusPow = Sii9777DevCapVbusPow_t()
        with self.device.lock:
            retcode = Sii9777CbusLocalDevcapPowGet(self.device.drv_instance, byref(pCbusPow))
        self._test_api_retcode("Sii9777CbusLocalDevcapPowGet", retcode)
        self.assertEqual(pCbusPow.value, SII9777_VBUS_PROVIDE_POWER,
                         "The golden local devcap pow value should be %s" % SII9777_VBUS_PROVIDE_POWER)

    def _test_Sii9777CbusLocalDevcapPowSet(self, value):
        pCbusPow = Sii9777DevCapVbusPow_t(value)
        with self.device.lock:
            retcode = Sii9777CbusLocalDevcapPowSet(self.device.drv_instance, byref(pCbusPow))
        self._test_api_retcode("Sii9777CbusLocalDevcapPowSet", retcode)

        pCbusPow = Sii9777DevCapVbusPow_t()
        with self.device.lock:
            Sii9777CbusLocalDevcapPowGet(self.device.drv_instance, byref(pCbusPow))
        self.assertEqual(pCbusPow.value, value,
                         "The golden local devcap pow value should be %s" % value)

    def test_Sii9777CbusLocalDevcapPowSet_SII9777_VBUS_REMOVE_POWER(self):
        self._test_Sii9777CbusLocalDevcapPowSet(SII9777_VBUS_REMOVE_POWER)

    def test_Sii9777CbusLocalDevcapPowSet_SII9777_VBUS_PROVIDE_POWER(self):
        self._test_Sii9777CbusLocalDevcapPowSet(SII9777_VBUS_PROVIDE_POWER)


class CbusLocalDevcapVideoLinkModeTestCase(BaseBostonDriverTestCase):
    def test_golden_local_devcap_video_link_mode(self):
        golden_video_link_mode = 0x7F
        pVidLinkMode = Sii9777DevCapVidLinkMode_t()
        with self.device.lock:
            retcode = Sii9777CbusLocalDevcapVideoLinkModeGet(self.device.drv_instance, byref(pVidLinkMode))
        self._test_api_retcode("Sii9777CbusLocalDevcapVideoLinkModeGet", retcode)
        self.assertEqual(pVidLinkMode.value, golden_video_link_mode,
                         "The local devcap video link mode value should be %s" % golden_video_link_mode)

    @name("Sii9777CbusLocalDevcapVideoLinkModeSet, Sii9777CbusLocalDevcapVideoLinkModeGet %(vid_link_mode)s")
    @parametrize("vid_link_mode", type=str, iteration=VID_LINK_MODES)
    def test_Sii9777CbusLocalDevcapVideoLinkModeSet(self):
        with self.device.lock:
            pVidLinkMode = Sii9777DevCapVidLinkMode_t(VID_LINK_MODES[self.vid_link_mode])
            retcode = Sii9777CbusLocalDevcapVideoLinkModeSet(self.device.drv_instance, byref(pVidLinkMode))
            self._test_api_retcode("Sii9777CbusLocalDevcapVideoLinkModeSet", retcode)

        with self.device.lock:
            pVidLinkMode = Sii9777DevCapVidLinkMode_t()
            retcode = Sii9777CbusLocalDevcapVideoLinkModeGet(self.device.drv_instance, byref(pVidLinkMode))
            self._test_api_retcode("Sii9777CbusLocalDevcapVideoLinkModeGet", retcode)

            self.assertEqual(VID_LINK_MODES[self.vid_link_mode], pVidLinkMode.value,
                             "The video link mode should be %s" % self.vid_link_mode)

    def tearDown(self):
        with self.device.lock:
            pVidLinkMode = Sii9777DevCapVidLinkMode_t(0x7F)
            Sii9777CbusLocalDevcapVideoLinkModeSet(self.device.drv_instance, byref(pVidLinkMode))


class CbusLocalDevcapAudioLinkModeTestCase(BaseBostonDriverTestCase):
    def test_golden_local_devcap_audio_link_mode(self):
        golden_audio_link_mode = 0x07
        pAudLinkMode = Sii9777DevCapAudLinkMode_t()
        with self.device.lock:
            retcode = Sii9777CbusLocalDevcapAudioLinkModeGet(self.device.drv_instance, byref(pAudLinkMode))
        self._test_api_retcode("Sii9777CbusLocalDevcapAudioLinkModeGet", retcode)
        self.assertEqual(pAudLinkMode.value, golden_audio_link_mode,
                         "The local devcap audio link mode value should be %s" % golden_audio_link_mode)

    def tearDown(self):
        with self.device.lock:
            pAudLinkMode = Sii9777DevCapAudLinkMode_t(0x07)
            Sii9777CbusLocalDevcapAudioLinkModeSet(self.device.drv_instance, byref(pAudLinkMode))

    @name("Sii9777CbusLocalDevcapAudioLinkModeSet, Sii9777CbusLocalDevcapAudioLinkModeGet %(aud_link_mode)s")
    @parametrize("aud_link_mode", type=str, iteration=AUD_LINK_MODES)
    def test_Sii9777CbusLocalDevcapAudioLinkModeSet(self):
        with self.device.lock:
            pAudLinkMode = Sii9777DevCapAudLinkMode_t(AUD_LINK_MODES[self.aud_link_mode])
            retcode = Sii9777CbusLocalDevcapAudioLinkModeSet(self.device.drv_instance, byref(pAudLinkMode))
            self._test_api_retcode("Sii9777CbusLocalDevcapAudioLinkModeSet", retcode)

        with self.device.lock:
            pAudLinkMode = Sii9777DevCapAudLinkMode_t()
            retcode = Sii9777CbusLocalDevcapAudioLinkModeGet(self.device.drv_instance, byref(pAudLinkMode))
            self._test_api_retcode("Sii9777CbusLocalDevcapAudioLinkModeGet", retcode)

            self.assertEqual(AUD_LINK_MODES[self.aud_link_mode], pAudLinkMode.value,
                             "The local devcap audio link mode value should be %s" % self.aud_link_mode)


class CbusLocalDevcapVideoTypeTestCase(BaseBostonDriverTestCase):
    def test_golden_local_devcap_video_type(self):
        golden_video_type = 0x8F
        pVideoType = Sii9777DevCapVideoType_t()
        with self.device.lock:
            retcode = Sii9777CbusLocalDevcapVideoTypeGet(self.device.drv_instance, byref(pVideoType))
        self._test_api_retcode("Sii9777CbusLocalDevcapVideoTypeGet", retcode)
        self.assertEqual(pVideoType.value, golden_video_type,
                         "The local devcap video type value should be %s" % golden_video_type)

    def tearDown(self):
        with self.device.lock:
            pVideoType = Sii9777DevCapVideoType_t(0x8F)
            Sii9777CbusLocalDevcapVideoTypeSet(self.device.drv_instance, byref(pVideoType))

    @name("Sii9777CbusLocalDevcapVideoTypeSet, Sii9777CbusLocalDevcapVideoTypeGet %(video_type)s")
    @parametrize("video_type", type=str, iteration=VIDEO_TYPES)
    def test_Sii9777CbusLocalDevcapVideoTypeSet(self):
        with self.device.lock:
            pVideoType = Sii9777DevCapVideoType_t(VIDEO_TYPES[self.video_type])
            retcode = Sii9777CbusLocalDevcapVideoTypeSet(self.device.drv_instance, byref(pVideoType))
            self._test_api_retcode("Sii9777CbusLocalDevcapVideoTypeSet", retcode)

        with self.device.lock:
            pVideoType = Sii9777DevCapVideoType_t()
            retcode = Sii9777CbusLocalDevcapVideoTypeGet(self.device.drv_instance, byref(pVideoType))
            self._test_api_retcode("Sii9777CbusLocalDevcapVideoTypeGet", retcode)

            self.assertEqual(VIDEO_TYPES[self.video_type], pVideoType.value,
                             "The video should be %s" % self.video_type)


class CbusLocalDevcapFeatureFlagTestCase(BaseBostonDriverTestCase):
    def test_golden_local_devcap_feature_flag(self):
        golden_feature_flag = 0x5F
        pFeatureFlag = Sii9777DevCapFeatureFlag_t()
        with self.device.lock:
            retcode = Sii9777CbusLocalDevcapFeatureFlagGet(self.device.drv_instance, byref(pFeatureFlag))
        self._test_api_retcode("Sii9777CbusLocalDevcapFeatureFlagGet", retcode)
        self.assertEqual(pFeatureFlag.value, golden_feature_flag,
                         "The local devcap video type value should be %s" % golden_feature_flag)

    def tearDown(self):
        with self.device.lock:
            pFeatureFlag = Sii9777DevCapFeatureFlag_t(0x5F)
            Sii9777CbusLocalDevcapFeatureFlagSet(self.device.drv_instance, byref(pFeatureFlag))

    @name("Sii9777CbusLocalDevcapFeatureFlagSet, Sii9777CbusLocalDevcapFeatureFlagSet %(feature_flag)s")
    @parametrize("feature_flag", type=str, iteration=FEATURE_FLAGS)
    def test_Sii9777CbusLocalDevcapFeatureFlagSet(self):
        with self.device.lock:
            pFeatureFlag = Sii9777DevCapFeatureFlag_t(FEATURE_FLAGS[self.feature_flag])
            retcode = Sii9777CbusLocalDevcapFeatureFlagSet(self.device.drv_instance, byref(pFeatureFlag))
            self._test_api_retcode("Sii9777CbusLocalDevcapVideoTypeSet", retcode)

        with self.device.lock:
            pFeatureFlag = Sii9777DevCapFeatureFlag_t()
            retcode = Sii9777CbusLocalDevcapFeatureFlagGet(self.device.drv_instance, byref(pFeatureFlag))
            self._test_api_retcode("Sii9777CbusLocalDevcapVideoTypeGet", retcode)

            self.assertEqual(FEATURE_FLAGS[self.feature_flag], pFeatureFlag.value,
                             "The feature flag should be %s" % self.feature_flag)


@parametrize("peer_device", type=Mhl2Interface, fetch=parametrize.FetchType.LAZY)
class CbusRemoteDevcapQueryTestCase(BaseBostonDriverTestCase):
    def test_CbusRemoteDevcapQuery(self):
        pData = (uint8_t * 16)()
        offset = uint8_t(0)
        length = uint8_t(16)

        with self.device.lock:
            retcode = Sii9777CbusRemoteDevcapQuery(self.device.drv_instance, pData, offset, length)
        self._test_api_retcode("Sii9777CbusRemoteDevcapQuery", retcode)
        actual_remote_devcap = [pData[index] for index in range(16)]

        expect_remote_devcap = self.peer_device.get_local_devcap()
        self.assertSequenceEqual(actual_remote_devcap, expect_remote_devcap,
                                 "the remote devcap should be %s" % expect_remote_devcap)


@skip("already tested in test_mhl3_msc_msg.py")
class CbusMscMsgSendReceiveTestCase(BaseBostonDriverTestCase):
    def test_Sii9777CbusMscMsgSendReceive(self):
        pass