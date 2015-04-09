#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import time

from simg import fs
from simg.test.framework import TestCase, TestContextManager, parametrize


class PlayVideoTestCase(TestCase):
    def setUp(self):
        context = TestContextManager.current_context()
        resource = context.resource
        self.webcam = resource.webcam

        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)

    @parametrize("totaltime", type=float, default=600)
    @parametrize("interval", type=float, default=60)
    def test_playvideo(self):
        time1 = 0
        time2 = time.time() + self.totaltime
        while time2-time1 >= 0:
            time.sleep(self.interval)
            self.capture_image_name = os.path.join(self.capture_image_dir, self.name + str(time1) + ".jpg")
            self.webcam.capture_image(self.capture_image_name)
            time1 = time.time()
