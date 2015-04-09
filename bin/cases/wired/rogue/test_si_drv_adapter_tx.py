#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import time
import unittest
from ctypes import *

from simg.test.framework import TestContextManager
from simg.devadapter.wired.rogue.api import *

from base import BaseSiiDrvAdaptTestCase


#7.5.3.1 Downstream Connection Status Interrogation
@unittest.skip("NOT FOUND API 'SiiDrvAdaptDsConnectStatusGet' IN DLL")
class SiiDrvAdaptDsConnectStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptDsConnectStatusGet(self):
        pass


#7.5.3.2 Downstream EDID Availability Interrogation
class SiiDrvAdaptTxDsEdidStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptTxDsEdidStatusGet(self):
        edid_status = SiiDrvAdaptDsEdidStatus_t()
        edid_status_mapping = {SII_DRV_ADAPT_DS_EDID__NOT_AVAILABLE: "SII_DRV_ADAPT_DS_EDID__NOT_AVAILABLE",
                               SII_DRV_ADAPT_DS_EDID__AVAILABLE: "SII_DRV_ADAPT_DS_EDID__AVAILABLE"}
        SiiDrvAdaptTxDsEdidStatusGet(self.device.sii_instance, byref(edid_status))
        self.assertIn(edid_status.value, edid_status_mapping.keys(),
                      msg="Downstream EDID status should in %s" % edid_status_mapping.values())
        logger.debug("Downstream EDID status: %s", edid_status_mapping[edid_status.value])


#7.5.3.3 Reads Downstream EDID
class SiiDrvAdaptTxDsEdidReadTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptTxDsEdidRead(self):
        edidbuf1 = (uint8_t * 128)()
        edidbuf2 = (uint8_t * 128)()
        SiiDrvAdaptTxDsEdidRead(self.device.sii_instance, 0, 0, edidbuf1, 128)
        SiiDrvAdaptTxDsEdidRead(self.device.sii_instance, 1, 0, edidbuf2, 128)
        edid = []
        for i in edidbuf1:
            edid.append("0x%x" % i)
        for i in edidbuf2:
            edid.append("0x%x" % i)
        logger.debug("Downstream EDID: %s", edid)


#7.5.3.4 TX TMDS Output Set
class SiiDrvAdaptTxTmdsOutSetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptTxTmdsOutSet_ENABLE(self):
        tmds_output = SiiDrvAdaptTmdsOut_t(SII_DRV_ADAPT_TMDS_OUT__ENABLE)
        SiiDrvAdaptTxTmdsOutSet(self.device.sii_instance, tmds_output)
        logger.debug("TxTmdsOutSet to SII_DRV_ADAPT_TMDS_OUT__ENABLE")
        with self.device.log_subject.listen("TX TMDS ON") as listener:
            s = listener.get(timeout=10)
        self.assertIsNotNone(s, msg="Should receive 'TX TMDS ON' in log in 10s")

    def test_SiiDrvAdaptTxTmdsOutSet_DISABLE(self):
        tmds_output = SiiDrvAdaptTmdsOut_t(SII_DRV_ADAPT_TMDS_OUT__DISABLE)
        SiiDrvAdaptTxTmdsOutSet(self.device.sii_instance, tmds_output)
        logger.debug("TxTmdsOutSet to SII_DRV_ADAPT_TMDS_OUT__DISABLE")
        with self.device.log_subject.listen("TX TMDS OFF") as listener:
            s = listener.get(timeout=15.0)
        self.assertIsNotNone(s, msg="Should receive 'TX TMDS OFF' in log")


#7.5.3.5 TX TMDS Swing Level Set
@unittest.skip("DLL doesn't enable si_drv_adapter_internal")
class SiiDrvAdaptTmdsSwingLevelSetTestCase(BaseSiiDrvAdaptTestCase):
    """
    0x07[7:5]:Control the TMDS swing level of the chip,
    simon: page13(ID: 50)/0x22
    """
    def test_SiiDrvAdaptTmdsSwingLevelSet(self):
        for i in range(7, 8):
            level = uint8_t(i)
            SiiDrvAdaptTmdsSwingLevelSet(self.device.sii_instance, level)
            logger.debug("TmdsSwingLevelSet to %s", level)
            time.sleep(3)

            # actual_level = uint8_t()
            # SiiDrvAdaptChipRegRead(self.device.sii_instance, 0x75, actual_level, sizeof(actual_level))
            # self.assertEquals(actual_level.value, level.value, "swing level should be %s after setting" % i)
            # #TODO: add check point


#7.5.3.6 SiiDrvAdaptTxMuteSet
class SiiDrvAdaptTxMuteSetTestCase(BaseSiiDrvAdaptTestCase):
    __mute_status_mapper = {SII_DRV_ADAPTER_MUTE__OFF: "SII_DRV_ADAPTER_MUTE__OFF",
                            SII_DRV_ADAPTER_MUTE__AV_MUTE_OFF: "SII_DRV_ADAPTER_MUTE__AV_MUTE_OFF",
                            SII_DRV_ADAPTER_MUTE__AV_MUTE_ON: "SII_DRV_ADAPTER_MUTE__AV_MUTE_ON",
                            SII_DRV_ADAPTER_MUTE__VIDEO: "SII_DRV_ADAPTER_MUTE__VIDEO",
                            SII_DRV_ADAPTER_MUTE__AUDIO: "SII_DRV_ADAPTER_MUTE__AUDIO",
                            SII_DRV_ADAPTER_MUTE__AUDIO_VIDEO: "SII_DRV_ADAPTER_MUTE__AUDIO_VIDEO"}

    def setUp(self):
        mute_state = SiiDrvAdaptMute_t()
        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, byref(mute_state))
        if self._testMethodName == "test_SiiDrvAdaptTxMuteSet__AV_MUTE_OFF":
            if mute_state.value == SII_DRV_ADAPTER_MUTE__AV_MUTE_OFF:
                self.test_SiiDrvAdaptTxMuteSet__AV_MUTE_ON()
        elif self._testMethodName == "test_SiiDrvAdaptTxMuteSet__AV_MUTE_ON":
            if mute_state.value == SII_DRV_ADAPTER_MUTE__AV_MUTE_ON:
                self.test_SiiDrvAdaptTxMuteSet__AV_MUTE_OFF()
        else:
            raise ValueError("Unsupported test method: %s" % self._testMethodName)

    def tearDown(self):
        mute_state = SiiDrvAdaptMute_t()
        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, byref(mute_state))
        if mute_state.value == SII_DRV_ADAPTER_MUTE__AV_MUTE_ON:
            self.test_SiiDrvAdaptTxMuteSet__AV_MUTE_OFF()

    def test_SiiDrvAdaptTxMuteSet__AV_MUTE_OFF(self):
        expected = SII_DRV_ADAPTER_MUTE__AV_MUTE_OFF
        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__RX_AV_MUTE_STATUS_CHNG) as listener:
            mute = SiiDrvAdaptMute_t(expected)
            SiiDrvAdaptTxMuteSet(self.device.sii_instance, mute)
            event = listener.get(timeout=10)
            self.assertIsNotNone(event, msg="should get SII_DRV_ADAPT_EVENT__RX_AV_MUTE_STATUS_CHNG in 10s")

        mute_state = SiiDrvAdaptMute_t()
        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, byref(mute_state))
        self.assertEquals(mute_state.value, expected,
                          msg="RxAvMuteStatus should be %s" % self.__mute_status_mapper[expected])

    def test_SiiDrvAdaptTxMuteSet__AV_MUTE_ON(self):
        expected = SII_DRV_ADAPTER_MUTE__AV_MUTE_ON

        with self.device.evt_subject.listen(SII_DRV_ADAPT_EVENT__RX_AV_MUTE_STATUS_CHNG) as listener:
            mute = SiiDrvAdaptMute_t(SII_DRV_ADAPTER_MUTE__AV_MUTE_ON)
            SiiDrvAdaptTxMuteSet(self.device.sii_instance, mute)
            event = listener.get(timeout=10)
            self.assertIsNotNone(event, msg="should get SII_DRV_ADAPT_EVENT__RX_AV_MUTE_STATUS_CHNG in 10s")

        mute_state = SiiDrvAdaptMute_t()
        SiiDrvAdaptRxAvMuteStatusGet(self.device.sii_instance, byref(mute_state))
        self.assertEquals(mute_state.value, expected,
                          msg="RxAvMuteStatus should be %s" % self.__mute_status_mapper[expected])


#7.5.3.7 TX HDCP Aksv Get
class SiiDrvAdaptTxHdcpAksvGetTestCase(BaseSiiDrvAdaptTestCase):
    __tx_askv = ['0x52', '0xbc', '0x38', '0x7c', '0x2b']

    def test_SiiDrvAdaptTxHdcpAksvGet(self):
        aksv_buffer = (uint8_t * 5)()
        ksv_load = SiiDrvAdaptTxHdcpAksvGet(self.device.sii_instance, aksv_buffer)
        ksv_load_mapper = {
            SII_DRV_ADAPTER_KSV_LOAD__OK: "SII_DRV_ADAPTER_KSV_LOAD__OK",
            SII_DRV_ADAPTER_KSV_LOAD__NOT_AVAILABLE: "SII_DRV_ADAPTER_KSV_LOAD__NOT_AVAILABLE",
            SII_DRV_ADAPTER_KSV_LOAD__BUFFER_ERROR: "SII_DRV_ADAPTER_KSV_LOAD__BUFFER_ERROR"}

        self.assertIn(ksv_load, ksv_load_mapper.keys(),
                      msg="AKSV load error code should in %s" % ksv_load_mapper.values())
        logger.debug("AKSV load error code: %s" % ksv_load_mapper[ksv_load])
        askv = []
        for i in aksv_buffer:
            askv.append("0x%x" % i)
        logger.debug("TX HDCP Aksv: %s", askv)
        #self.assertSequenceEqual(askv, self.__tx_askv, "TX HDCP Aksv should be %s" % self.__tx_askv, seq_type=list)


#7.5.3.8 TX HDCP Protection Set
class SiiDrvAdaptTxHdcpProtectionSetTestCase(BaseSiiDrvAdaptTestCase):
    """
    Enable/disable downstream HDCP.
    Note:
    This function is only used for debugging purpose and only with debugging version of adapter firmware.
    HDCP is enabled by default.
    """
    __hdcp_status_mapper = {
        SII_DRV_ADAPTER_HDCP_TX_STATUS__OFF: "SII_DRV_ADAPTER_HDCP_TX_STATUS__OFF",
        SII_DRV_ADAPTER_HDCP_TX_STATUS__SUCCESS: "SII_DRV_ADAPTER_HDCP_TX_STATUS__SUCCESS",
        SII_DRV_ADAPTER_HDCP_TX_STATUS__AUTHENTICATING: "SII_DRV_ADAPTER_HDCP_TX_STATUS__AUTHENTICATING",
        SII_DRV_ADAPTER_HDCP_TX_STATUS__FAILED: "SII_DRV_ADAPTER_HDCP_TX_STATUS__FAILED",
        SII_DRV_ADAPTER_HDCP_TX_STATUS__RCVID_CHG: "SII_DRV_ADAPTER_HDCP_TX_STATUS__RCVID_CHG"}

    def setUp(self):
        hdcp_status = SiiDrvAdaptHdcpTxStatus_t()
        SiiDrvAdaptTxHdcpDsStatusGet(self.device.sii_instance, byref(hdcp_status))
        if self._testMethodName == "test_SiiDrvAdaptTxHdcpProtectionSet_ON":
            if hdcp_status.value == SII_DRV_ADAPTER_HDCP_TX_STATUS__SUCCESS:
                self.test_SiiDrvAdaptTxHdcpProtectionSet_OFF()
        elif self._testMethodName == "test_SiiDrvAdaptTxHdcpProtectionSet_OFF":
            if hdcp_status.value == SII_DRV_ADAPTER_HDCP_PROTECT__OFF:
                self.test_SiiDrvAdaptTxHdcpProtectionSet_ON()
        else:
            raise ValueError("Unsupported test method: %s" % self._testMethodName)

    def tearDown(self):
        SiiDrvAdaptTxHdcpProtectionSet(self.device.sii_instance, SII_DRV_ADAPTER_HDCP_PROTECT__OFF)

    def test_SiiDrvAdaptTxHdcpProtectionSet_ON(self):
        with self.device.log_subject.listen("TX HDCP ON") as log_listener:
            protect_type = SII_DRV_ADAPTER_HDCP_PROTECT__ON
            SiiDrvAdaptTxHdcpProtectionSet(self.device.sii_instance, protect_type)
            log = log_listener.get(timeout=5.0)
            self.assertIsNotNone(log, "'TX HDCP ON' should be found in 5.0s from log file.")

        hdcp_status = SiiDrvAdaptHdcpTxStatus_t()
        SiiDrvAdaptTxHdcpDsStatusGet(self.device.sii_instance, byref(hdcp_status))
        self.assertEquals(hdcp_status.value, SII_DRV_ADAPTER_HDCP_TX_STATUS__SUCCESS,
                          msg="TX HDCP status should be %s" % self.__hdcp_status_mapper[SII_DRV_ADAPTER_HDCP_TX_STATUS__SUCCESS])

    def test_SiiDrvAdaptTxHdcpProtectionSet_OFF(self):
        with self.device.log_subject.listen("TX HDCP OFF") as log_listener:
            protect_type = SII_DRV_ADAPTER_HDCP_PROTECT__OFF
            SiiDrvAdaptTxHdcpProtectionSet(self.device.sii_instance, protect_type)
            log = log_listener.get(timeout=5.0)
            self.assertIsNotNone(log, "'TX HDCP OFF' should be found in 5.0s from log file.")

        hdcp_status = SiiDrvAdaptHdcpTxStatus_t()
        SiiDrvAdaptTxHdcpDsStatusGet(self.device.sii_instance, byref(hdcp_status))
        self.assertEquals(hdcp_status.value, SII_DRV_ADAPTER_HDCP_PROTECT__OFF,
                          msg="TX HDCP status should be %s" % self.__hdcp_status_mapper[SII_DRV_ADAPTER_HDCP_PROTECT__OFF])


#7.5.3.9 Downstream HDCP Status Get
@unittest.skip("SiiDrvAdaptTxHdcpDsStatusGet has already been tested in SiiDrvAdaptTxHdcpProtectionSetTestCase")
class SiiDrvAdaptTxHdcpDsStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptTxHdcpDsStatusGet(self):
        pass


#7.5.3.10 Downstream HDCP Last Failure Reason Get
#TODO: How to make HDCP failed
class SiiDrvAdaptDsHdcpLastFailureReasonGetTestCase(BaseSiiDrvAdaptTestCase):
    """
    Enable/disable downstream HDCP.
    Note:
    This function is only used for debugging purpose and only with debugging version of adapter firmware.
    HDCP is enabled by default.
    """
    def test_SiiDrvAdaptDsHdcpLastFailureReasonGet(self):

        hdcp_fail_reason = SiiDrvAdaptHdcpTxFailureReason_t()
        SiiDrvAdaptDsHdcpLastFailureReasonGet(self.device.sii_instance, byref(hdcp_fail_reason))
        logger.debug("DsHdcpLastFailureReason: %s", hdcp_fail_reason)


#7.5.3.11 Sink HDCP Ver Get
class SiiDrvAdaptTxHdcpDsVerGetTestCase(BaseSiiDrvAdaptTestCase):
    """
    Downstream HDCP support interrogation
    """
    hdcp_ver_mapper = {SII_DRV_ADAPTER_HDCP_VER__NOT_SUPPORTED: "SII_DRV_ADAPTER_HDCP_VER__NOT_SUPPORTED",
                       SII_DRV_ADAPTER_HDCP_VER__1x: "SII_DRV_ADAPTER_HDCP_VER__1x",
                       SII_DRV_ADAPTER_HDCP_VER__22: "SII_DRV_ADAPTER_HDCP_VER__22"}

    def test_SiiDrvAdaptTxHdcpDsVerGet(self):
        hdcp_ver = SiiDrvAdaptHdcpVer_t()
        SiiDrvAdaptTxHdcpDsVerGet(self.device.sii_instance, byref(hdcp_ver))

        logger.debug("TX HDCP version is: %s", self.hdcp_ver_mapper[hdcp_ver.value])
        self.assertIn(hdcp_ver.value, self.hdcp_ver_mapper.keys(),
                      msg="TX HDCP version should in %s" % self.hdcp_ver_mapper.values())


#7.5.3.12 TX HDCP Receiver Id Get
class SiiDrvAdaptTxHdcpRcvIdGetTestCase(BaseSiiDrvAdaptTestCase):
    """
    Downstream HDCP 1.X/2.X AKSV/RcvID interrogation.
    """

    def test_SiiDrvAdaptTxHdcpRcvIdGet(self):
        #tx_rcvid = ['0xaf', '0x54', '0x39', '0x8d', '0xd']
        rcv_id_buffer = (uint8_t * 5)()
        SiiDrvAdaptTxHdcpRcvIdGet(self.device.sii_instance, rcv_id_buffer)
        rcvid = []
        for i in rcv_id_buffer:
            rcvid.append("0x%x" % i)
        logger.debug("TX HDCP Receiver Id: %s", rcvid)
        #self.assertSequenceEqual(rcvid, tx_rcvid, "TX HDCP Aksv should be %s" % tx_rcvid, seq_type=list)


#7.5.3.13 TX HDCP Downstream Repeater Bit Get
class SiiDrvAdaptTxHdcpDsRepeaterBitGetTestCase(BaseSiiDrvAdaptTestCase):
    """
    Downstream HDCP downstream repeater bit interrogation.
    Note:
    This function is only expected to be called when transmitter is used in AVR repeater case.
    """
    def setUp(self):
        devices = TestContextManager.current_context().resource.devices
        if not (devices.transmitter and devices.repeater and self.device.id == 0x9678):
            self.skipTest("This function is only expected to be called when transmitter is used in AVR repeater case.")

    def test_SiiDrvAdaptTxHdcpDsRepeaterBitGet(self):
        ds_repeater = bool_t()
        SiiDrvAdaptTxHdcpDsRepeaterBitGet(self.device.sii_instance, byref(ds_repeater))
        if ds_repeater.value is True:
            logger.debug("SiiDrvAdaptTxHdcpDsRepeaterBitGet: Downstream device is a repeater.")
        else:
            logger.debug("SiiDrvAdaptTxHdcpDsRepeaterBitGet: false Downstream device is not a repeater.")


#7.5.3.14 HDCP Receiver Id List Get
@unittest.skip("NOT FOUND API 'SiiDrvAdaptHdcpRcvIdListGet' IN DLL")
class SiiDrvAdaptHdcpRcvIdListGetTestCase(BaseSiiDrvAdaptTestCase):
    def test_SiiDrvAdaptHdcpRcvIdListGet(self):
        pass


#7.5.3.15 TX HDCP Topology Get
class SiiDrvAdaptTxHdcpDsTopologyGetTestCase(BaseSiiDrvAdaptTestCase):
    """
    Downstream HDCP 2.X RxInfo and HDCP 1.X BStatus interrogation.
    Note:
    This function is only expected to be called when transmitter is used in AVR repeater case.
    """
    def setUp(self):
        devices = TestContextManager.current_context().resource.devices
        if not (devices.transmitter and devices.repeater and self.device.id == 0x9678):
            self.skipTest("This function is only expected to be called when transmitter is used in AVR repeater case.")

    def test_SiiDrvAdaptTxHdcpDsTopologyGet(self):
        hdcp_topology = SiiDrvAdaptHdcpTopology_t()
        SiiDrvAdaptTxHdcpDsTopologyGet(self.device.sii_instance, byref(hdcp_topology))
        logger.debug("SiiDrvAdaptTxHdcpDsTopologyGet: bHdcp1DeviceDs %s", hdcp_topology.bHdcp1DeviceDs)
        logger.debug("SiiDrvAdaptTxHdcpDsTopologyGet: bHdcp20DeviceDs %s", hdcp_topology.bHdcp20DeviceDs)
        logger.debug("SiiDrvAdaptTxHdcpDsTopologyGet: bMaxCascadeExceeded %s", hdcp_topology.bMaxCascadeExceeded)
        logger.debug("SiiDrvAdaptTxHdcpDsTopologyGet: bMaxDevsExceeded %s", hdcp_topology.bMaxDevsExceeded)
        logger.debug("SiiDrvAdaptTxHdcpDsTopologyGet: deviceCount %s", hdcp_topology.deviceCount)
        logger.debug("SiiDrvAdaptTxHdcpDsTopologyGet: depth %s", hdcp_topology.depth)
        logger.debug("SiiDrvAdaptTxHdcpDsTopologyGet: seqNumV %s", hdcp_topology.seqNumV)


#7.5.3.16 TX HDCP StreamManageMessage Set
class SiiDrvAdaptTxHdcpStreamManageMsgSetTestCase(BaseSiiDrvAdaptTestCase):
    """
    Downstream HDCP 2.X Stream Manage message set.
    Propagate the HDCP 2.X Stream_Manage message to the downstream repeater.
    Note:
    This function is only expected to be called when transmitter is used in AVR repeater case,
    and attached downstream device is also a repeater.
    """
    def setUp(self):
        devices = TestContextManager.current_context().resource.devices
        if not (devices.transmitter and devices.repeater and devices.receiver and self.device.id == 0x9678):
            self.skipTest("This function is only expected to be called when transmitter is used in AVR repeater case.")

    def test_SiiDrvAdaptTxHdcpStreamManageMsgSet(self):
        message = SiiDrvAdaptHdcpStreamManageInfo_t()
        message.k = 1
        message.seqNumM = 0
        message.streamIdType[0] = 0     # content type 0
        SiiDrvAdaptTxHdcpStreamManageMsgSet(self.device.sii_instance, message)

        message.streamIdType[0] = 0x0100    # content type 1
        SiiDrvAdaptTxHdcpStreamManageMsgSet(self.device.sii_instance, message)


#7.5.3.17 TX RxSense Status Get
class SiiDrvAdaptTxRxSenseStatusGetTestCase(BaseSiiDrvAdaptTestCase):
    """
    Checks if a downstream Rx sense is detected.
    """
    def setUp(self):
        if self.device.id != 0x9678:
            self.skipTest("SiiDrvAdaptTxRxSenseStatusGetTestCase only can be tested on 0x9678")

    def test_SiiDrvAdaptTxRxSenseStatusGet(self):
        rx_sense_status = SiiDrvAdaptTxRxSenseType_t()
        SiiDrvAdaptTxRxSenseStatusGet(self.device.sii_instance, byref(rx_sense_status))
        logger.debug("Downstream Rx sense is detected: %s", rx_sense_status)


class SiiDrvAdaptTxLinkTypeGetTestCase(BaseSiiDrvAdaptTestCase):
    __link_type_mapping = {SII_DRV_LINK_DISCONNECTED: "SII_DRV_LINK_DISCONNECTED",
                           SII_DRV_LINK_HDMI: "SII_DRV_LINK_HDMI",
                           SII_DRV_LINK_MHL12: "SII_DRV_LINK_MHL12",
                           SII_DRV_LINK_MHL3: "SII_DRV_LINK_MHL3"}

    def test_SiiDrvAdaptTxLinkTypeGet(self):
        link_type = SiiDrvAdaptLinkType_t()
        SiiDrvAdaptTxLinkTypeGet(self.device.sii_instance, byref(link_type))
        logger.debug("TX link type is: %s", self.__link_type_mapping[link_type.value])
        self.assertEquals(link_type.value, self.device.ds_linktype,
                          msg="TX link type should be %s" % self.__link_type_mapping[self.device.ds_linktype])
