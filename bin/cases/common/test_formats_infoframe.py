#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import re
import time
import random

from simg import fs
from simg.util.soundrecorder import capture_soundrecorder_image
from simg.test.framework import TestCase, TestContextManager, parametrize
from simg.devadapter import BaseDeviceAdapter
#from simg.util.avproducer.getinfoframe import VideoInfo


video_golden_timing= {\
'EIA640x480p@60_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA1440x480i@60_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA2880x480i@60_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA720x480p@60_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA1440x480p@60_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA2880x480p@60_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA1440x576i@50_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA2880x576i@50_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA720x576p@50_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA1440x576p@50_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA2880x576p@50_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:SMPTE 170M[1] ITU601 [5] HB:82 02 0d e4   ' ,\
'EIA1280x720p@60_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:ITU709 [6] HB:82 02 0d e4   ' ,\
'EIA1920x1080i@60_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:ITU709 [6] HB:82 02 0d e4   ' ,\
'EIA1920x1080p@60_RGB_8' : '[AUD] check_sum:verified channel_count:2ch HB:84 01 0a 4a  [SPD] check_sum:verified vendor_name:[VENDOR..] HB:83 01 19 64  [AVI] check_sum:verified colorimetry:ITU709 [6] HB:82 02 0d e4   ' ,\
     }

@parametrize("format")
@parametrize("listen_keyword")
@parametrize("device", type=BaseDeviceAdapter, fetch=parametrize.FetchType.LAZY)
class FormatsTestCase(TestCase):
    def setUp(self):
        context = TestContextManager.current_context()
        resource = context.resource
        self.astro = resource.avproducer
        self.qd980 = resource.avconsumer
        self.webcam = resource.webcam

        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)
        self.capture_image_name = os.path.join(self.capture_image_dir, self.name+".jpg")

    def tearDown(self):
        pass
    
    @parametrize("listen_timeout", type=float, default=3.0)    
    def test_x_infoframe(self):
        try:
            if re.search("Side_half_",self.format,re.I):
                part1,part2 = self.format.split('Side_half_')
                program = part1+ "Side_half"
                color_space, color_depth, threed_type = part2.split('_')
            else:    
                program, color_space, color_depth = self.format.split('_')
            color_depth += "-bit"
            with self.device.log_subject.listen(self.listen_keyword) as listener:
                if re.search("Side_half_",self.format,re.I):
                    self.astro.load_video(program, 'Color Bar SMPTE', color_space, color_depth,video_3d_extension=threed_type)
                else:    
                    self.astro.load_video(program, 'Color Bar SMPTE', color_space, color_depth)
                event = listener.get(timeout=self.listen_timeout)
                self.assertIsNotNone(event,
                                     msg="should get log keyword '%s' in %ss" % (self.listen_keyword, self.listen_timeout))
            #time.sleep(15.0)
        finally:
            #self.webcam.capture_image(self.capture_image_name)
            pass

        time.sleep(15.0)

        timing_info = self.qd980.get_x_info(mem_size="big")
        self.assertEquals(timing_info, video_golden_timing[self.format], "AUD/AVI/SPD/VSIF/MPEG infoframe should be the same with golden value")
      


def trans_info(items):
    print items
    for i in range(3,14):
        if i == 6 or i == 11 or i == 13:
            items[i] = float(items[i].split(":")[1])
        else:
            items[i] = int(items[i].split(":")[1])
    return items        
