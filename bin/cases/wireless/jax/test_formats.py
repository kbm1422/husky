#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import re
import time
from datetime import datetime
from simg import fs
from simg.util.soundrecorder import capture_soundrecorder_image
from simg.test.framework import TestContextManager, parametrize
from base import BaseJaxTestCase


@parametrize("format")
class FormatsTestCase(BaseJaxTestCase):
    def setUp(self):
        resource = TestContextManager.current_context().resource
        self.txunit, self.rxunit = resource.acquire_pair()
        self.tx_gen3_1 = self.txunit.device.gen3_1
        self.tx_gen3_2 = self.txunit.device.gen3_2
        self.rx_gen3_1 = self.rxunit.device.gen3_1
        self.rx_gen3_2 = self.rxunit.device.gen3_2
        self.qd = self.txunit.avproducer

        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)
        self.capture_image_name = os.path.join(self.capture_image_dir, self.name+".jpg")

        if re.match("DVI_", self.format, re.IGNORECASE):
            self.iface = "DVI"
            self.format = re.sub("DVI_", "", self.format)
        elif re.match("HDMI_", self.format, re.IGNORECASE):
            self.iface = "HDMI"
            self.format = re.sub("HDMI_", "", self.format)
        else:
            self.iface = "HDMI"

        # if self.rx_gen3_2.nvramget(0x66) != 0x0:
        #     self.rx_gen3_2.nvramset(0x66, 0x0)
        #     self.rxunit.reset()
        #     time.sleep(10)
        self.make_connected(self.txunit.device, self.rxunit.device)

    @parametrize("IMAGE_2D", default="Acer1")
    def test_video_format(self):
        fmt, color_space, color_depth = self.format.split('_')
        logger.debug("which image for vformat test? %s", self.IMAGE_2D)
        try:
            with self.rx_gen3_1.log_subject.listen("baseband video UNMUTE") as rx_listener1:
                load = self.qd.load(self.iface, self.IMAGE_2D, "/card0/Library/formats/" + fmt, color_space, color_depth)
                self.assertEqual(load, 1, msg="QD should load image successfully")
                self._test_non4k_logkeyword_recvtime_devstate(rx_listener1)
            time.sleep(10.0)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)

    def _test_non4k_logkeyword_recvtime_devstate(self, rx_listener1):
        qd_send_time = datetime.now()
        rx_event1 = rx_listener1.get(timeout=20)
        self.assertIsNotNone(rx_event1,
                             msg="main should get log keyword 'baseband video UNMUTE' in 20s")

        rx_recv_time1 = datetime.strptime(rx_event1.partition('>')[0].replace("(E) ", ""), "%m/%d/%Y %H:%M:%S:%f")
        rx_spend_time1 = (rx_recv_time1 - qd_send_time).total_seconds()
        self.assertLessEqual(rx_spend_time1, 10,
                             msg="Main change format spend time %ss should less equal than 10s" % rx_spend_time1,
                             iswarning=True)

        # actual_state = self.rx_gen3_2.getDevState()
        # self.assertEquals(actual_state, "associated", "sub state should be associated")

    @parametrize("aud_vfmt", default="1080p60_RGB_8")
    def test_audio_format(self):
        match = re.search("(.*)Ch_(.*)_(.*)Fs_(.*)KHz", self.format, re.I)
        audio_channel_number = match.group(1)  # Number of channels (eg: 2, 6, 8)
        audio_format = match.group(2)  # Format (eg: LPCM, SPDIF, Dolby etc)
        audio_fs = match.group(3)  # 256Fx, 128Fs, 384Fs, 512Fs
        audio_frequency = match.group(4)  # Sampling frequency (eg: 32, 44.1, 48, 88.2, 96, 176.4, 192)
        logger.debug("Get the vformat %s", self.aud_vfmt)
        video_format, video_color_space, video_color_depth = self.aud_vfmt.split('_')

        if audio_channel_number == "2":
            audio_type = "AudioLR"
        elif audio_channel_number == "6" or audio_channel_number == "8":
            audio_type = "Audio_Xf"
        else:
            raise ValueError("Unsupported channel number: %s" % audio_channel_number)

        try:
            with self.rx_gen3_1.log_subject.listen("baseband video UNMUTE") as rx_listener1:
                load = self.qd.load_audio(self.iface,
                                          audio_type,
                                          "/card0/Library/formats/"+video_format,
                                          video_color_space,
                                          video_color_depth,
                                          audio_frequency,
                                          audio_channel_number)
                self.assertEqual(load, 1, msg="QD should load audio successfully")
                self._test_non4k_logkeyword_recvtime_devstate(rx_listener1)
            time.sleep(10.0)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)
            capture_soundrecorder_image(os.path.join(self.capture_image_dir, "%s_sn.jpg" % self.name + ".jpg"))

    def test_3d_format(self):
        fmt, structure, color_space, color_depth, image = self.format.split('_')
        logger.debug("Which image for 3D format test ? %s", image)
        try:
            with self.rx_gen3_1.log_subject.listen("baseband video UNMUTE") as rx_listener1:
                load = self.qd.load_3d(image, "/card0/Library/formats/"+fmt, structure, color_space, color_depth)
                self.assertEqual(load, 1, msg="QD should load 3D successfully")
                self._test_non4k_logkeyword_recvtime_devstate(rx_listener1)
            time.sleep(10.0)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)
            self.qd.back_2d()



