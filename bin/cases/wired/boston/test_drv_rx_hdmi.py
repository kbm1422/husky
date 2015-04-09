#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import time
from ctypes import byref

from base import BaseBostonDriverTestCase, RX_PORT_MAPPER
from simg import fs
from simg.test.framework import name, parametrize, TestContextManager, LinkedTestCase
from simg.devadapter.wired.boston.Sii9777RxLib import *
from simg.util.zip import retrieve_struct


AV_LINK_MAPPER = {
    "SII9777_AV_LINK__NONE": SII9777_AV_LINK__NONE,
    "SII9777_AV_LINK__DVI": SII9777_AV_LINK__DVI,
    "SII9777_AV_LINK__HDMI1": SII9777_AV_LINK__HDMI1,
    "SII9777_AV_LINK__HDMI2": SII9777_AV_LINK__HDMI2,
    "SII9777_AV_LINK__MHL": SII9777_AV_LINK__MHL
}


@name("Sii9777Plus5vQuery")
@parametrize("rx_port", type=str, choice=RX_PORT_MAPPER.keys())
class Plus5vQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777Plus5vQuery(self):
        rx_port = Sii9777RxPort_t(RX_PORT_MAPPER[self.rx_port])
        plus_5v = bool_t()
        with self.device.lock:
            retcode = Sii9777Plus5vQuery(self.device.drv_instance, rx_port, byref(plus_5v))
        self._test_api_retcode("Sii9777Plus5vQuery", retcode)
        self.assertTrue(plus_5v, "The plus 5v should be True on port %s" % self.rx_port)


@name("Sii9777AvLinkQuery")
@parametrize("av_link", type=str, choice=AV_LINK_MAPPER.keys())
class AvLinkQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777AvLinkQuery(self):
        pAvLink = Sii9777AvLink_t()
        with self.device.lock:
            retcode = Sii9777AvLinkQuery(self.device.drv_instance, byref(pAvLink))
        self._test_api_retcode("Sii9777AvLinkQuery", retcode)
        self.assertEqual(pAvLink.value, AV_LINK_MAPPER[self.av_link], "AV link should be %s" % self.av_link)


@name("Sii9777AvMuteQuery")
class AvMuteQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777AvMuteQuery(self):
        is_av_muted = Sii9777AvMute_t()
        with self.device.lock:
            Sii9777AvMuteQuery(self.device.drv_instance, byref(is_av_muted))
        logger.debug("is_av_muted: %s", is_av_muted.value)
        self._warn("don't know how to make the av muted or un-mute")


@name("Sii9777HpdQuery, Sii9777HpdSet, Sii9777HpdGet")
@parametrize("rx_port", type=str, choice=RX_PORT_MAPPER.keys())
class HpdTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_golden_hpd_value",
        "test_Sii9777HpdSet_OFF",
        "test_Sii9777HpdSet_ON"
    )

    def setUp(self):
        self.__rx_port = Sii9777RxPort_t(RX_PORT_MAPPER[self.rx_port])
        context = TestContextManager.current_context()
        resource = context.resource
        self.webcam = resource.webcam
        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)

    def test_golden_hpd_value(self):
        actual_hpd = bool_t()
        with self.device.lock:
            retcode = Sii9777HpdQuery(self.device.drv_instance, self.__rx_port, byref(actual_hpd))
        self._test_api_retcode("Sii9777HpdQuery", retcode)
        self.assertTrue(actual_hpd.value, msg="Golden Sii9777HpdQuery value should be True")

    def test_Sii9777HpdSet_ON(self):
        try:
            expect_hpd = bool_t(True)
            with self.device.lock:
                retcode = Sii9777HpdSet(self.device.drv_instance, self.__rx_port, byref(expect_hpd))
            self._test_api_retcode("Sii9777HpdSet(ON)", retcode)

            actual_get_hpd = bool_t()
            with self.device.lock:
                retcode = Sii9777HpdGet(self.device.drv_instance, self.__rx_port, byref(actual_get_hpd))
            self._test_api_retcode("Sii9777HpdGet(ON)", retcode)
            self.assertEqual(actual_get_hpd.value, expect_hpd.value,
                             msg="Sii9777HpdGet(ON) value should be %s" % expect_hpd.value)
        finally:
            time.sleep(15)
            capture_image_name = os.path.join(self.capture_image_dir, self.name+"(ON).jpg")
            self.webcam.capture_image(capture_image_name)

    def test_Sii9777HpdSet_OFF(self):
        try:
            expect_hpd = bool_t(False)
            with self.device.lock:
                retcode = Sii9777HpdSet(self.device.drv_instance, self.__rx_port, byref(expect_hpd))
            self._test_api_retcode("Sii9777HpdSet(OFF)", retcode)

            actual_hpd = bool_t()
            with self.device.lock:
                retcode = Sii9777HpdGet(self.device.drv_instance, RX_PORT_MAPPER[self.rx_port], byref(actual_hpd))
            self._test_api_retcode("Sii9777HpdGet", retcode)
            self.assertEqual(actual_hpd.value, expect_hpd.value,
                             msg="Sii9777HpdGet(OFF) value should be %s" % expect_hpd.value)
        finally:
            time.sleep(15)
            capture_image_name = os.path.join(self.capture_image_dir, self.name+"(OFF).jpg")
            self.webcam.capture_image(capture_image_name)


@name("Sii9777HpdReplicateEnableSet, Sii9777HpdReplicateEnableGet")
class HpdReplicateEnableTestCase(LinkedTestCase, BaseBostonDriverTestCase):
    methodNames = (
        "test_golden_hpd_replicate_enable",
        "test_Sii9777HpdReplicateEnableSet_ON",
        "test_Sii9777HpdReplicateEnableSet_OFF"
    )

    def test_golden_hpd_replicate_enable(self):
        pbOn = bool_t()
        with self.device.lock:
            Sii9777HpdReplicateEnableGet(self.device.drv_instance, byref(pbOn))
        self.assertFalse(pbOn, "HPD replicate enable golden value should be False")

    def test_Sii9777HpdReplicateEnableSet_ON(self):
        pbOn = bool_t(True)
        with self.device.lock:
            retcode = Sii9777HpdReplicateEnableSet(self.device.drv_instance, byref(pbOn))
        self._test_api_retcode("Sii9777HpdReplicateEnableSet", retcode)

        pbOn = bool_t()
        with self.device.lock:
            retcode = Sii9777HpdReplicateEnableGet(self.device.drv_instance, byref(pbOn))
        self._test_api_retcode("Sii9777HpdReplicateEnableGet", retcode)
        self.assertTrue(pbOn, "Set HPD replicate enable to True should be successfully.")
        time.sleep(5)

    def test_Sii9777HpdReplicateEnableSet_OFF(self):
        pbOn = bool_t(False)
        with self.device.lock:
            Sii9777HpdReplicateEnableSet(self.device.drv_instance, byref(pbOn))
        time.sleep(5)


@name("Sii9777VideoTimingQuery")
class VideoTimingQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777VideoTimingQuery(self):
        video_timing = Sii9777VideoTiming_t()
        with self.device.lock:
            retcode = Sii9777VideoTimingQuery(self.device.drv_instance, byref(video_timing))
        self._test_api_retcode("Sii9777VideoTimingQuery", retcode)

        fields = retrieve_struct(video_timing)
        logger.debug("VideoTiming: %s", fields)
        self.assertTrue(True, msg="Current video timing is %s" % fields)


@name("Sii9777VideoFormatQuery")
class VideoFormatQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777VideoFormatQuery(self):
        video_format = Sii9777VideoFmt_t()
        with self.device.lock:
            retcode = Sii9777VideoFormatQuery(self.device.drv_instance, byref(video_format))
        self._test_api_retcode("Sii9777VideoFormatQuery", retcode)

        fields = retrieve_struct(video_format)
        logger.debug("VideoFormat: %s", fields)
        self.assertTrue(True, msg="Current video format is %s" % fields)


@name("Sii9777AudioFormatQuery")
class AudioFormatQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777AudioFormatQuery(self):
        audio_format = Sii9777AudioFmt_t()
        with self.device.lock:
            retcode = Sii9777AudioFormatQuery(self.device.drv_instance, byref(audio_format))
        self._test_api_retcode("Sii9777AudioFormatQuery", retcode)

        fields = retrieve_struct(audio_format)
        logger.debug("AudioFormat: %s", fields)
        self.assertTrue(True, msg="Current audio format is %s" % fields)


@name("Sii9777IsrcQuery")
class IsrcQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777IsrcQuery(self):
        isrc = Sii9777Isrc_t()
        with self.device.lock:
            retcode = Sii9777IsrcQuery(self.device.drv_instance, byref(isrc))
        self._test_api_retcode("Sii9777IsrcQuery", retcode)

        fields = retrieve_struct(isrc)
        logger.debug("Isrc: %s", fields)
        self.assertTrue(True, msg="Current isrc is %s" % fields)


@name("Sii9777AcpQuery")
class AcpQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777AcpQuery(self):
        """
        ACP: Audio Content Protection
        Outputs Audio Content Protection information to a Sii9777Acp_t data structure.
        The structure is based on the ACP packet as defined in <insert cross-reference>.
        SII9777_EVENT_FLAGS__ACP_CHNG notification is generated when incoming ACP information changes.
        """
        acp = Sii9777Acp_t()
        with self.device.lock:
            retcode = Sii9777AcpQuery(self.device.drv_instance, byref(acp))
        self._test_api_retcode("Sii9777AcpQuery", retcode)
        fields = retrieve_struct(acp)
        self.assertTrue(True, msg="Current ACP is %s" % fields)


@name("Sii9777SpdQuery")
class SpdQueryTestCase(BaseBostonDriverTestCase):
    def test_Sii9777SpdQuery(self):
        """
        SPD: Source Product Description
        The structure is based on SPD packet.
        SII9777_EVENT_FLAGS__SPD_CHNG notification is generated when incoming SPD information changes.
        """
        spd = Sii9777Spd_t()
        with self.device.lock:
            retcode = Sii9777SpdQuery(self.device.drv_instance, byref(spd))
        self._test_api_retcode("Sii9777SpdQuery", retcode)
        fields = retrieve_struct(spd)
        logger.debug("SPD: %s", fields)
        self.assertTrue(True, msg="Current SPD is %s" % fields)


__test_suite__ = {
    "name": "Boston Driver RX HDMI Test Suite",
}