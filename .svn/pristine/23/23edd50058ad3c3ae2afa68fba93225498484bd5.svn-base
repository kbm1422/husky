#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import time

from simg.test.framework import TestCase, parametrize
from simg.util.webcam import WebCamFactory
from simg.util.sl8800 import SL8800


@parametrize("interface")
@parametrize("item")
@parametrize("dut")
class HDCPTestCase(TestCase):
    def test_receiver(self):
        logger.info("Now start receiver test item " + self.item)
        receiver = SL8800(interface=self.interface, dut=self.dut)
        res = receiver.test(self.item)
        time.sleep(20)
        self.assertEquals(res, 0, "Test item " + self.item + " return code should be \"0\" ")
        #Capture picture
        picture_path = os.path.dirname(os.path.dirname(self.logdir))
        picture_name = os.path.join(picture_path, self.item + ".jpeg")
        webcam = WebCamFactory.new_webcam(devnum="0")
        webcam.capture_image(picture_name)
        time.sleep(5)

    def test_transmitter(self):
        logger.info("Now start transmitter test item " + self.item)
        transmitter = SL8800(interface=self.interface, dut=self.dut)
        res = transmitter.test(self.item)
        time.sleep(20)
        self.assertEquals(res, 0, "Test item " + self.item + " return code should be \"0\" ")
        if self.item in ["1A-01", "1A-03", "1A-04", "1A-05", "1A-06", "1A-07", "1B-01", "1B-08"]:
            #Capture picture
            picture_path = os.path.dirname(os.path.dirname(self.logdir))
            picture_name = os.path.join(picture_path, self.item + ".jpeg")
            webcam = WebCamFactory.new_webcam(devnum="0")
            webcam.capture_image(picture_name)
            time.sleep(5)               

    def test_repeater(self):
        logger.info("Now start repeater test item " + self.item)
        repeater = SL8800(interface=self.interface, dut=self.dut)
        res = repeater.test(self.item)
        time.sleep(20)
        self.assertEquals(res, 0, "Test item " + self.item + " return code should be \"0\" ")
        if self.item in ["3A-01", "3B-01", "3C-01-1", "3C-01-2","3C-01-3", "3C-01-4", "3C-04", "3C-05", "3C-06", "3C-07", "3C-11",
                         "3C-23", "3C-24", "3C-25-T0", "3C-25-T1", "3C-25-T2"]:
            #Capture picture
            picture_path = os.path.dirname(os.path.dirname(self.logdir))
            picture_name = os.path.join(picture_path, self.item + ".jpeg")
            webcam = WebCamFactory.new_webcam(devnum="0")
            webcam.capture_image(picture_name)
            time.sleep(5)
            
        
if __name__ == '__main__':
    a = HDCPTestCase()
    a.test_receiver()