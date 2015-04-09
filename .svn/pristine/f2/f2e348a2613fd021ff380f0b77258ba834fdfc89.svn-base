#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
from simg.test.framework import TestContextManager
from base import BaseJaxTestCase


class ResetTestCase(BaseJaxTestCase):
    def setUp(self):
        resource = TestContextManager.current_context().resource
        self.txunit, self.rxunit = resource.acquire_pair()

        self.capture_image_dir = os.path.join(self.logdir, "images")
        self.capture_image_name = os.path.join(self.capture_image_dir, "%s_%s.jpg" % (self.name, self.cycleindex))
        self._make_connected(self.txunit.device, self.rxunit.device)

    def test_source_reset(self):
        try:
            self.txunit.device.reset()
            self._test_connection(self.rxunit.device)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)

    def test_sink_reset(self):
        try:
            self.rxunit.device.reset()
            self._test_connection(self.rxunit.device)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)

    def test_both_reset(self):
        try:
            self.txunit.device.reset()
            self.rxunit.device.reset()
            self._test_connection(self.rxunit.device)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)

    def test_source_nvramreset(self):
        try:
            self.txunit.device.nvramreset()
            self.txunit.device.reset()
            self._test_connection(self.rxunit.device)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)

    def test_sink_nvramreset(self):
        try:
            self.rxunit.device.nvramreset()
            self.rxunit.device.reset()
            self._test_connection(self.rxunit.device)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)