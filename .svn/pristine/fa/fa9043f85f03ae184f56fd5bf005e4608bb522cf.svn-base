#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import re
import time

from simg import fs
from simg.util.soundrecorder import capture_soundrecorder_image
from simg.test.framework import TestCase, TestContextManager, parametrize
from simg.devadapter import BaseDeviceAdapter

@parametrize("format")
@parametrize("listen_keyword")
@parametrize("device", type=BaseDeviceAdapter, fetch=parametrize.FetchType.LAZY)
class FormatsTestCase(TestCase):
    def setUp(self):
        context = TestContextManager.current_context()
        resource = context.resource
        self.qd = resource.avproducer
        self.webcam = resource.webcam

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

    def tearDown(self):
        pass

    @parametrize("IMAGE_2D", default="Acer1")
    @parametrize("listen_timeout", type=float, default=3.0)
    def test_video_format(self):
        fmt, color_space, color_depth = self.format.split('_')
        logger.debug("which image for vformat test? %s", self.IMAGE_2D)
        with self.device.log_subject.listen(self.listen_keyword) as listener:
            load = self.qd.load(self.iface, self.IMAGE_2D, "/card0/Library/formats/" + fmt, color_space, color_depth)
            self.assertEqual(load, 1, msg="QD should load image successfully")
            event = listener.get(timeout=self.listen_timeout)
            self.assertIsNotNone(event,
                                 msg="should get log keyword '%s' in %ss" % (self.listen_keyword, self.listen_timeout))
        time.sleep(15.0)
        self.webcam.capture_image(self.capture_image_name)

    @parametrize("aud_vfmt", default="1080p60_RGB_8")
    @parametrize("listen_timeout", type=float, default=3.0)
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

        with self.device.log_subject.listen(self.listen_keyword) as listener:
            load = self.qd.load_audio(self.iface,
                                      audio_type,
                                      "/card0/Library/formats/"+video_format,
                                      video_color_space,
                                      video_color_depth,
                                      audio_frequency,
                                      audio_channel_number)
            self.assertEqual(load, 1, msg="QD should load audio successfully")
            event = listener.get(timeout=self.listen_timeout)
            self.assertIsNotNone(event,
                                 msg="should get log keyword '%s' in %ss" % (self.listen_keyword, self.listen_timeout))

        time.sleep(15.0)
        self.webcam.capture_image(self.capture_image_name)
        capture_soundrecorder_image(os.path.join(self.capture_image_dir, "%s_sn.jpg" % self.name + ".jpg"))

    def test_3d_format(self):
        fmt, structure, color_space, color_depth, image = self.format.split('_')
        logger.debug("Which image for 3D format test ? %s", image)
        with self.device.log_subject.listen(self.listen_keyword) as listener:
            load = self.qd.load_3d(image, "/card0/Library/formats/"+fmt, structure, color_space, color_depth)
            self.assertEqual(load, 1, msg="QD should load 3D successfully")
            timeout = 20 if re.search("SBSF", image) else 10
            event = listener.get(timeout=timeout)
            self.assertIsNotNone(event, msg="should get log keyword '%s' in %ss" % (self.listen_keyword, timeout))

        time.sleep(15.0)
        self.webcam.capture_image(self.capture_image_name)
        self.qd.back_2d()


@parametrize("format")
class VideoCardFormatsTestCase(TestCase):
    def setUp(self):
        context = TestContextManager.current_context()
        resource = context.resource
        self.GTX = resource.avproducer

    @parametrize("format", default="1920_1080_32_30")
    def test_videocard_format(self):
        from simg.net.ssh import SSHClient
        logger.debug("which image for kformat test? %s", self.format)
        gtx = SSHClient(hostname=self.GTX.host, username="cyg_server", password="sqa")
        gtx.run("mkdir "+self.format, cwd="sqa_at/resolution")
        time.sleep(2)
        res = gtx.run(cmd="rmdir "+self.format[:-6], cwd="sqa_at/resolution")
        self.assertEqual(list(res)[0], 0, msg="4k format test")