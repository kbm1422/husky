#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import re
import time
import random

from simg import fs
from simg.test.framework import TestCase, TestContextManager, parametrize
from simg.devadapter import BaseDeviceAdapter


video_golden_timings = {
    'EIA1440x480i@59.94_RGB_8': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.73 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:59.94 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x480i@59.94_444_8': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.73 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:59.94 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x480i@59.94_422_8': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.73 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:59.94 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x480i@59.94_RGB_10': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.73 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:59.94 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x480i@59.94_444_10': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.73 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:59.94 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x480i@59.94_422_10': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.73 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:59.94 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x480i@59.94_RGB_12': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.73 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:59.94 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x480i@59.94_444_12': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.73 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:59.94 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x480i@59.94_422_12': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.73 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:59.94 Vsync:3 TMDS_Clock:27.000' ,\
   
    'EIA1440x480i@60_RGB_8': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.75 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:60.00 Vsync:3 TMDS_Clock:27.027' ,\
    'EIA1440x480i@60_444_8': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.75 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:60.00 Vsync:3 TMDS_Clock:27.027' ,\
    'EIA1440x480i@60_422_8': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.75 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:60.00 Vsync:3 TMDS_Clock:27.027' ,\
    'EIA1440x480i@60_RGB_10': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.75 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:60.00 Vsync:3 TMDS_Clock:27.027' ,\
    'EIA1440x480i@60_444_10': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.75 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:60.00 Vsync:3 TMDS_Clock:27.027' ,\
    'EIA1440x480i@60_422_10': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.75 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:60.00 Vsync:3 TMDS_Clock:27.027' ,\
    'EIA1440x480i@60_RGB_12': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.75 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:60.00 Vsync:3 TMDS_Clock:27.027' ,\
    'EIA1440x480i@60_444_12': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.75 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:60.00 Vsync:3 TMDS_Clock:27.027' ,\
    'EIA1440x480i@60_422_12': 'Video_Format:720(1440)x480i_59.94/60Hz_VIC=6 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:15.75 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:60.00 Vsync:3 TMDS_Clock:27.027' ,\
    
    'EIA2880x480i@59.94_RGB_8': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.73 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-59.94 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x480i@59.94_444_8': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.73 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-59.94 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x480i@59.94_422_8': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.73 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-59.94 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x480i@59.94_RGB_10': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:30 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.73 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-59.94 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x480i@59.94_444_10': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:30 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.73 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-59.94 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x480i@59.94_422_10': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.73 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-59.94 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x480i@59.94_RGB_12': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:36 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.73 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-59.94 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x480i@59.94_444_12': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:36 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.73 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-59.94 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x480i@59.94_422_12': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.73 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-59.94 Vsync:3 TMDS_Clock:54.000' ,\
    
    'EIA2880x480i@60_RGB_8': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.75 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-60.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA2880x480i@60_444_8': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.75 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-60.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA2880x480i@60_422_8': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.75 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-60.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA2880x480i@60_RGB_10': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:30 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.75 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-60.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA2880x480i@60_444_10': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:30 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.75 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-60.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA2880x480i@60_422_10': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.75 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-60.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA2880x480i@60_RGB_12': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:36 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.75 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-60.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA2880x480i@60_444_12': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:36 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.75 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-60.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA2880x480i@60_422_12': 'Video_Format:2880x480i_59.94/60Hz_VIC=10 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:76 Hfreq:15.75 Hsync:248 Vactive:240 Vtotal:263 Vfront:4 Vfreq:-60.00 Vsync:3 TMDS_Clock:54.054' ,\
    
    'EIA640x480p@60_RGB_8': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.50 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:60.00 Vsync:2 TMDS_Clock:25.200' ,\
    'EIA640x480p@60_444_8': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:4:4 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.50 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:60.00 Vsync:2 TMDS_Clock:25.200' ,\
    'EIA640x480p@60_422_8': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:2:2 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.50 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:60.00 Vsync:2 TMDS_Clock:25.200' ,\
    'EIA640x480p@60_RGB_10': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:30 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.50 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:60.00 Vsync:2 TMDS_Clock:25.200' ,\
    'EIA640x480p@60_444_10': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:30 RGB_YCC:4:4:4 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.50 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:60.00 Vsync:2 TMDS_Clock:25.200' ,\
    'EIA640x480p@60_422_10': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:2:2 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.50 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:60.00 Vsync:2 TMDS_Clock:25.200' ,\
    'EIA640x480p@60_RGB_12': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:36 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.50 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:60.00 Vsync:2 TMDS_Clock:25.200' ,\
    'EIA640x480p@60_444_12': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:36 RGB_YCC:4:4:4 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.50 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:60.00 Vsync:2 TMDS_Clock:25.200' ,\
    'EIA640x480p@60_422_12': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:2:2 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.50 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:60.00 Vsync:2 TMDS_Clock:25.200' ,\
    
    'EIA720x480p@59.94_RGB_8': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:31.47 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:27.000' ,\
    'EIA720x480p@59.94_444_8': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.47 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:27.000' ,\
    'EIA720x480p@59.94_422_8': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.47 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:27.000' ,\
    'EIA720x480p@59.94_RGB_10': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:30 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:31.47 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:27.000' ,\
    'EIA720x480p@59.94_444_10': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:30 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.47 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:27.000' ,\
    'EIA720x480p@59.94_422_10': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.47 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:27.000' ,\
    'EIA720x480p@59.94_RGB_12': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:36 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:31.47 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:27.000' ,\
    'EIA720x480p@59.94_444_12': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:36 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.47 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:27.000' ,\
    'EIA720x480p@59.94_422_12': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.47 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:27.000' ,\
    
    'EIA720x480p@60_RGB_8': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:31.50 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:27.027' ,\
    'EIA720x480p@60_444_8': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.50 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:27.027' ,\
    'EIA720x480p@60_422_8': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.50 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:27.027' ,\
    'EIA720x480p@60_RGB_10': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:30 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:31.50 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:27.027' ,\
    'EIA720x480p@60_444_10': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:30 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.50 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:27.027' ,\
    'EIA720x480p@60_422_10': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.50 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:27.027' ,\
    'EIA720x480p@60_RGB_12': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:36 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:31.50 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:27.027' ,\
    'EIA720x480p@60_444_12': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:36 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.50 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:27.027' ,\
    'EIA720x480p@60_422_12': 'Video_Format:720x480p_59.94/60Hz_VIC=2 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:31.50 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:27.027' ,\
    
    'EIA1920x1080p@25_RGB_8': 'Video_Format:1920x1080p_25Hz_VIC=33 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@25_444_8': 'Video_Format:1920x1080p_25Hz_VIC=33 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@25_422_8': 'Video_Format:1920x1080p_25Hz_VIC=33 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@25_RGB_10': 'Video_Format:1920x1080p_25Hz_VIC=33 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@25_444_10': 'Video_Format:1920x1080p_25Hz_VIC=33 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@25_422_10': 'Video_Format:1920x1080p_25Hz_VIC=33 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@25_RGB_12': 'Video_Format:1920x1080p_25Hz_VIC=33 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@25_444_12': 'Video_Format:1920x1080p_25Hz_VIC=33 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@25_422_12': 'Video_Format:1920x1080p_25Hz_VIC=33 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    
    'EIA1920x1080p@30_RGB_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_444_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_422_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_RGB_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_444_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_422_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_RGB_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_444_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_422_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    
    'EIA1920x1080p@50_RGB_8': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_444_8': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_422_8': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_RGB_10': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_444_10': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_422_10': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_RGB_12': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_444_12': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_422_12': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    
    'EIA1920x1080p@60_RGB_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_444_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_422_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_RGB_10': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_444_10': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_422_10': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_RGB_12': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_444_12': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_422_12': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    
    'EIA640x480p@59.94_RGB_8': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_444_8': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:4:4 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_422_8': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:2:2 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_RGB_10': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:30 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_444_10': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:30 RGB_YCC:4:4:4 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_422_10': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:2:2 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_RGB_12': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:36 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_444_12': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:36 RGB_YCC:4:4:4 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_422_12': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:2:2 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    
    'EIA2880x480p@59.94_RGB_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_444_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_422_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_RGB_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:30 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_444_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:30 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_422_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_RGB_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:36 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_444_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:36 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_422_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    
    'EIA2880x480p@60_RGB_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_444_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_422_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_RGB_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:30 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_444_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:30 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_422_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_RGB_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:36 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_444_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:36 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_422_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    
    'EIA2880x576p@50_RGB_8': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:RGB Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_444_8': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_422_8': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_RGB_10': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:30 RGB_YCC:RGB Hactive:2880 Htotal:3456 Hfront:47 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_444_10': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:30 RGB_YCC:4:4:4 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_422_10': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_RGB_12': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:36 RGB_YCC:RGB Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_444_12': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:36 RGB_YCC:4:4:4 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_422_12': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    
    'EIA1920x1080p@29.97_RGB_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_444_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_422_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_RGB_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_444_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_422_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_RGB_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_444_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_422_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    
    #'4K2K 3840x2160p24_RGB_8': 'Video_Format:3840x2160p_@Hz_VIC=93 Color_Depth:24 RGB_YCC:RGB Hactive:3840 Htotal:5500 Hfront:1276 Hfreq:53.95 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:23.98 Vsync:10 TMDS_Clock:296.703' ,\
    #'4K2K 3840x2160p24_444_8': 'Video_Format:3840x2160p_@Hz_VIC=93 Color_Depth:24 RGB_YCC:4:4:4 Hactive:3840 Htotal:5500 Hfront:1276 Hfreq:53.95 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:23.98 Vsync:10 TMDS_Clock:296.703' ,\
    #'4K2K 3840x2160p24_422_8': 'Video_Format:3840x2160p_@Hz_VIC=93 Color_Depth:24 RGB_YCC:4:2:2 Hactive:3840 Htotal:5500 Hfront:1276 Hfreq:53.95 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:23.98 Vsync:10 TMDS_Clock:296.703' ,\
    #'4K2K 3840x2160p25_RGB_8': 'Video_Format:3840x2160p_@Hz_VIC=94 Color_Depth:24 RGB_YCC:RGB Hactive:3840 Htotal:5280 Hfront:1056 Hfreq:56.25 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:25.00 Vsync:10 TMDS_Clock:297.000' ,\
    #'4K2K 3840x2160p25_444_8': 'Video_Format:3840x2160p_@Hz_VIC=94 Color_Depth:24 RGB_YCC:4:4:4 Hactive:3840 Htotal:5280 Hfront:1056 Hfreq:56.25 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:25.00 Vsync:10 TMDS_Clock:297.000' ,\
    #'4K2K 3840x2160p25_422_8': 'Video_Format:3840x2160p_@Hz_VIC=94 Color_Depth:24 RGB_YCC:4:2:2 Hactive:3840 Htotal:5280 Hfront:1056 Hfreq:56.25 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:25.00 Vsync:10 TMDS_Clock:297.000' ,\
    #'4K2K 3840x2160p30_RGB_8': 'Video_Format:3840x2160p_@Hz_VIC=95 Color_Depth:24 RGB_YCC:RGB Hactive:3840 Htotal:4400 Hfront:176 Hfreq:67.43 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:29.97 Vsync:10 TMDS_Clock:297.000' ,\
    #'4K2K 3840x2160p30_444_8': 'Video_Format:3840x2160p_@Hz_VIC=95 Color_Depth:24 RGB_YCC:4:4:4 Hactive:3840 Htotal:4400 Hfront:176 Hfreq:67.43 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:29.97 Vsync:10 TMDS_Clock:297.000' ,\
    #'4K2K 3840x2160p30_422_8': 'Video_Format:3840x2160p_@Hz_VIC=95 Color_Depth:24 RGB_YCC:4:2:2 Hactive:3840 Htotal:4400 Hfront:176 Hfreq:67.43 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:29.97 Vsync:10 TMDS_Clock:296.703' ,\
                                          # ' No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:4:2:2 Hactive:3840 Htotal:4400 Hfront:176 Hfreq:67.43 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:29.97 Vsync:10 TMDS Clock:296.703
    '4K2K 3840x2160p24_RGB_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:RGB Hactive:3840 Htotal:5500 Hfront:1276 Hfreq:53.95 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:23.98 Vsync:10 TMDS_Clock:296.703' ,\
    '4K2K 3840x2160p24_444_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:4:4:4 Hactive:3840 Htotal:5500 Hfront:1276 Hfreq:53.95 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:23.98 Vsync:10 TMDS_Clock:296.703' ,\
    '4K2K 3840x2160p24_422_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:4:2:2 Hactive:3840 Htotal:5500 Hfront:1276 Hfreq:53.95 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:23.98 Vsync:10 TMDS_Clock:296.703' ,\
    '4K2K 3840x2160p25_RGB_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:RGB Hactive:3840 Htotal:5280 Hfront:1056 Hfreq:56.25 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:25.00 Vsync:10 TMDS_Clock:297.000' ,\
    '4K2K 3840x2160p25_444_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:4:4:4 Hactive:3840 Htotal:5280 Hfront:1056 Hfreq:56.25 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:25.00 Vsync:10 TMDS_Clock:297.000' ,\
    '4K2K 3840x2160p25_422_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:4:2:2 Hactive:3840 Htotal:5280 Hfront:1056 Hfreq:56.25 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:25.00 Vsync:10 TMDS_Clock:297.000' ,\
    '4K2K 3840x2160p30_RGB_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:RGB Hactive:3840 Htotal:4400 Hfront:176 Hfreq:67.43 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:29.97 Vsync:10 TMDS_Clock:297.000' ,\
    '4K2K 3840x2160p30_444_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:4:4:4 Hactive:3840 Htotal:4400 Hfront:176 Hfreq:67.43 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:29.97 Vsync:10 TMDS_Clock:297.000' ,\
    '4K2K 3840x2160p30_422_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:4:2:2 Hactive:3840 Htotal:4400 Hfront:176 Hfreq:67.43 Hsync:88 Vactive:2160 Vtotal:2250 Vfront:8 Vfreq:29.97 Vsync:10 TMDS_Clock:296.703' ,\
    
    'EIA1440x480i@120_RGB_8': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_444_8': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_422_8': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_RGB_10': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_444_10': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_422_10': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_RGB_12': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_444_12': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_422_12': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    
    'EIA1440x480i@240_RGB_8': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.672' ,\
    'EIA1440x480i@240_444_8': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:63.706' ,\
    'EIA1440x480i@240_422_8': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:63.706' ,\
    'EIA1440x480i@240_RGB_10': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.379' ,\
    'EIA1440x480i@240_444_10': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.865' ,\
    'EIA1440x480i@240_422_10': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.099' ,\
    'EIA1440x480i@240_RGB_12': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:63.680' ,\
    'EIA1440x480i@240_444_12': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.280' ,\
    'EIA1440x480i@240_422_12': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.099' ,\
    
    'EIA1440x480p@59.94_RGB_8': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.47 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:54.000' ,\
    'EIA1440x480p@59.94_444_8': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.47 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:54.000' ,\
    'EIA1440x480p@59.94_422_8': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.47 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:54.000' ,\
    'EIA1440x480p@59.94_RGB_10': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.47 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:54.000' ,\
    'EIA1440x480p@59.94_444_10': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.47 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:54.000' ,\
    'EIA1440x480p@59.94_422_10': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.47 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:54.000' ,\
    'EIA1440x480p@59.94_RGB_12': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.47 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:54.000' ,\
    'EIA1440x480p@59.94_444_12': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.47 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:54.000' ,\
    'EIA1440x480p@59.94_422_12': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.47 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:54.000' ,\
    
    'EIA1440x480p@60_RGB_8': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.50 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA1440x480p@60_444_8': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.50 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA1440x480p@60_422_8': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.50 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA1440x480p@60_RGB_10': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.50 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA1440x480p@60_444_10': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.50 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA1440x480p@60_422_10': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.50 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA1440x480p@60_RGB_12': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.50 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA1440x480p@60_444_12': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.50 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA1440x480p@60_422_12': 'Video_Format:1440x480p_59.94/60Hz_VIC=14 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:32 Hfreq:31.50 Hsync:124 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:54.054' ,\
    
    'EIA1440x576i@50_RGB_8': 'Video_Format:720(1440)x576i_50Hz_VIC=21 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:15.62 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:50.00 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x576i@50_444_8': 'Video_Format:720(1440)x576i_50Hz_VIC=21 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:15.62 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:50.00 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x576i@50_422_8': 'Video_Format:720(1440)x576i_50Hz_VIC=21 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:15.62 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:50.00 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x576i@50_RGB_10': 'Video_Format:720(1440)x576i_50Hz_VIC=21 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:15.62 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:50.00 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x576i@50_444_10': 'Video_Format:720(1440)x576i_50Hz_VIC=21 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:15.62 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:50.00 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x576i@50_422_10': 'Video_Format:720(1440)x576i_50Hz_VIC=21 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:15.62 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:50.00 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x576i@50_RGB_12': 'Video_Format:720(1440)x576i_50Hz_VIC=21 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:15.62 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:50.00 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x576i@50_444_12': 'Video_Format:720(1440)x576i_50Hz_VIC=21 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:15.62 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:50.00 Vsync:3 TMDS_Clock:27.000' ,\
    'EIA1440x576i@50_422_12': 'Video_Format:720(1440)x576i_50Hz_VIC=21 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:15.62 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:50.00 Vsync:3 TMDS_Clock:27.000' ,\
    
    'EIA2880x576i@50_RGB_8': 'Video_Format:2880x576i_50Hz_VIC=25 Color_Depth:24 RGB_YCC:RGB Hactive:2880 Htotal:3456 Hfront:48 Hfreq:15.62 Hsync:252 Vactive:288 Vtotal:313 Vfront:2 Vfreq:-50.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x576i@50_444_8': 'Video_Format:2880x576i_50Hz_VIC=25 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:15.62 Hsync:252 Vactive:288 Vtotal:313 Vfront:2 Vfreq:-50.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x576i@50_422_8': 'Video_Format:2880x576i_50Hz_VIC=25 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:15.62 Hsync:252 Vactive:288 Vtotal:313 Vfront:2 Vfreq:-50.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x576i@50_RGB_10': 'Video_Format:2880x576i_50Hz_VIC=25 Color_Depth:30 RGB_YCC:RGB Hactive:2880 Htotal:3456 Hfront:47 Hfreq:15.62 Hsync:252 Vactive:288 Vtotal:313 Vfront:2 Vfreq:-50.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x576i@50_444_10': 'Video_Format:2880x576i_50Hz_VIC=25 Color_Depth:30 RGB_YCC:4:4:4 Hactive:2880 Htotal:3456 Hfront:47 Hfreq:15.62 Hsync:252 Vactive:288 Vtotal:313 Vfront:2 Vfreq:-50.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x576i@50_422_10': 'Video_Format:2880x576i_50Hz_VIC=25 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:15.62 Hsync:252 Vactive:288 Vtotal:313 Vfront:2 Vfreq:-50.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x576i@50_RGB_12': 'Video_Format:2880x576i_50Hz_VIC=25 Color_Depth:36 RGB_YCC:RGB Hactive:2880 Htotal:3456 Hfront:48 Hfreq:15.62 Hsync:252 Vactive:288 Vtotal:313 Vfront:2 Vfreq:-50.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x576i@50_444_12': 'Video_Format:2880x576i_50Hz_VIC=25 Color_Depth:36 RGB_YCC:4:4:4 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:15.62 Hsync:252 Vactive:288 Vtotal:313 Vfront:2 Vfreq:-50.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA2880x576i@50_422_12': 'Video_Format:2880x576i_50Hz_VIC=25 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:15.62 Hsync:252 Vactive:288 Vtotal:313 Vfront:2 Vfreq:-50.00 Vsync:3 TMDS_Clock:54.000' ,\
    
    'EIA720x576p@50_RGB_8': 'Video_Format:720x576p_50Hz_VIC=17 Color_Depth:24 RGB_YCC:RGB Hactive:720 Htotal:864 Hfront:12 Hfreq:31.25 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:27.000' ,\
    'EIA720x576p@50_444_8': 'Video_Format:720x576p_50Hz_VIC=17 Color_Depth:24 RGB_YCC:4:4:4 Hactive:720 Htotal:864 Hfront:12 Hfreq:31.25 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:27.000' ,\
    'EIA720x576p@50_422_8': 'Video_Format:720x576p_50Hz_VIC=17 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:864 Hfront:12 Hfreq:31.25 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:27.000' ,\
    'EIA720x576p@50_RGB_10': 'Video_Format:720x576p_50Hz_VIC=17 Color_Depth:30 RGB_YCC:RGB Hactive:720 Htotal:864 Hfront:11 Hfreq:31.25 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:27.000' ,\
    'EIA720x576p@50_444_10': 'Video_Format:720x576p_50Hz_VIC=17 Color_Depth:30 RGB_YCC:4:4:4 Hactive:720 Htotal:864 Hfront:11 Hfreq:31.25 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:27.000' ,\
    'EIA720x576p@50_422_10': 'Video_Format:720x576p_50Hz_VIC=17 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:864 Hfront:12 Hfreq:31.25 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:27.000' ,\
    'EIA720x576p@50_RGB_12': 'Video_Format:720x576p_50Hz_VIC=17 Color_Depth:36 RGB_YCC:RGB Hactive:720 Htotal:864 Hfront:12 Hfreq:31.25 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:27.000' ,\
    'EIA720x576p@50_444_12': 'Video_Format:720x576p_50Hz_VIC=17 Color_Depth:36 RGB_YCC:4:4:4 Hactive:720 Htotal:864 Hfront:12 Hfreq:31.25 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:27.000' ,\
    'EIA720x576p@50_422_12': 'Video_Format:720x576p_50Hz_VIC=17 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:864 Hfront:12 Hfreq:31.25 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:27.000' ,\
    
    'EIA1440x576p@50_RGB_8': 'Video_Format:1440x576p_50Hz_VIC=29 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:128 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA1440x576p@50_444_8': 'Video_Format:1440x576p_50Hz_VIC=29 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:128 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA1440x576p@50_422_8': 'Video_Format:1440x576p_50Hz_VIC=29 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:128 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA1440x576p@50_RGB_10': 'Video_Format:1440x576p_50Hz_VIC=29 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:128 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA1440x576p@50_444_10': 'Video_Format:1440x576p_50Hz_VIC=29 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:128 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA1440x576p@50_422_10': 'Video_Format:1440x576p_50Hz_VIC=29 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:128 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA1440x576p@50_RGB_12': 'Video_Format:1440x576p_50Hz_VIC=29 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:128 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA1440x576p@50_444_12': 'Video_Format:1440x576p_50Hz_VIC=29 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:128 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA1440x576p@50_422_12': 'Video_Format:1440x576p_50Hz_VIC=29 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:128 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:54.000' ,\
 
    'EIA1280x720p@23.98_RGB_8': 'Video_Format:1280x720p_@Hz_VIC=65 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:17.98 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:23.98 Vsync:5 TMDS_Clock:59.341' ,\
    'EIA1280x720p@23.98_422_8': 'Video_Format:1280x720p_@Hz_VIC=65 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:17.98 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:23.98 Vsync:5 TMDS_Clock:59.341' ,\
    'EIA1280x720p@23.98_444_8': 'Video_Format:1280x720p_@Hz_VIC=65 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:17.98 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:23.98 Vsync:5 TMDS_Clock:59.341' ,\
    'EIA1280x720p@24_RGB_8': 'Video_Format:1280x720p_23.97/24Hz_VIC=60 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:18.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:24.00 Vsync:5 TMDS_Clock:59.400' ,\
    'EIA1280x720p@24_422_8': 'Video_Format:1280x720p_23.97/24Hz_VIC=60 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:18.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:24.00 Vsync:5 TMDS_Clock:59.400' ,\
    'EIA1280x720p@24_444_8': 'Video_Format:1280x720p_23.97/24Hz_VIC=60 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:18.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:24.00 Vsync:5 TMDS_Clock:59.400' ,\
    'EIA1280x720p@25_RGB_8': 'Video_Format:1280x720p_25Hz_VIC=61 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:3960 Hfront:2420 Hfreq:18.75 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@25_422_8': 'Video_Format:1280x720p_25Hz_VIC=61 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:3960 Hfront:2420 Hfreq:18.75 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@25_444_8': 'Video_Format:1280x720p_25Hz_VIC=61 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:3960 Hfront:2420 Hfreq:18.75 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:25.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@29.97_RGB_8': 'Video_Format:1280x720p_@Hz_VIC=67 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:22.48 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@29.97_422_8': 'Video_Format:1280x720p_@Hz_VIC=67 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:22.48 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@29.97_444_8': 'Video_Format:1280x720p_@Hz_VIC=67 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:22.48 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@30_RGB_8': 'Video_Format:1280x720p_29.97/30Hz_VIC=62 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:22.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@30_422_8': 'Video_Format:1280x720p_29.97/30Hz_VIC=62 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:22.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@30_444_8': 'Video_Format:1280x720p_29.97/30Hz_VIC=62 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:3300 Hfront:1760 Hfreq:22.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\

    'EIA1280x720p@50_RGB_8': 'Video_Format:1280x720p_50Hz_VIC=19 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:1980 Hfront:440 Hfreq:37.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@50_444_8': 'Video_Format:1280x720p_50Hz_VIC=19 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:37.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@50_422_8': 'Video_Format:1280x720p_50Hz_VIC=19 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:37.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@50_RGB_10': 'Video_Format:1280x720p_50Hz_VIC=19 Color_Depth:30 RGB_YCC:RGB Hactive:1280 Htotal:1980 Hfront:440 Hfreq:37.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@50_444_10': 'Video_Format:1280x720p_50Hz_VIC=19 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:37.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@50_422_10': 'Video_Format:1280x720p_50Hz_VIC=19 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:37.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@50_RGB_12': 'Video_Format:1280x720p_50Hz_VIC=19 Color_Depth:36 RGB_YCC:RGB Hactive:1280 Htotal:1980 Hfront:440 Hfreq:37.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@50_444_12': 'Video_Format:1280x720p_50Hz_VIC=19 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:37.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@50_422_12': 'Video_Format:1280x720p_50Hz_VIC=19 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:37.50 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:74.250' ,\
   
    'EIA1280x720p@59.94_RGB_8': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:1650 Hfront:110 Hfreq:44.95 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@59.94_444_8': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:44.95 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@59.94_422_8': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:44.95 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@59.94_RGB_10': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:30 RGB_YCC:RGB Hactive:1280 Htotal:1650 Hfront:110 Hfreq:44.95 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@59.94_444_10': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:44.95 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@59.94_422_10': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:44.95 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@59.94_RGB_12': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:36 RGB_YCC:RGB Hactive:1280 Htotal:1650 Hfront:110 Hfreq:44.95 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@59.94_444_12': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:44.95 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1280x720p@59.94_422_12': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:44.95 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:59.94 Vsync:5 TMDS_Clock:74.176' ,\
    
    'EIA1280x720p@60_RGB_8': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:1650 Hfront:110 Hfreq:45.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@60_444_8': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:45.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@60_422_8': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:45.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@60_RGB_10': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:30 RGB_YCC:RGB Hactive:1280 Htotal:1650 Hfront:110 Hfreq:45.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@60_444_10': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:45.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@60_422_10': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:45.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@60_RGB_12': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:36 RGB_YCC:RGB Hactive:1280 Htotal:1650 Hfront:110 Hfreq:45.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@60_444_12': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:45.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1280x720p@60_422_12': 'Video_Format:1280x720p_59.94/60Hz_VIC=4 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:45.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:60.00 Vsync:5 TMDS_Clock:74.250' ,\
    
    'EIA1920x1080i@50_RGB_8': 'Video_Format:1920x1080i_50Hz_VIC=20 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@50_444_8': 'Video_Format:1920x1080i_50Hz_VIC=20 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@50_422_8': 'Video_Format:1920x1080i_50Hz_VIC=20 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@50_RGB_10': 'Video_Format:1920x1080i_50Hz_VIC=20 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@50_444_10': 'Video_Format:1920x1080i_50Hz_VIC=20 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@50_422_10': 'Video_Format:1920x1080i_50Hz_VIC=20 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@50_RGB_12': 'Video_Format:1920x1080i_50Hz_VIC=20 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@50_444_12': 'Video_Format:1920x1080i_50Hz_VIC=20 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-50.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@50_422_12': 'Video_Format:1920x1080i_50Hz_VIC=20 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:28.12 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-50.00 Vsync:5 TMDS_Clock:74.250' ,\
    
    'EIA1920x1080i@59.94_RGB_8': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080i@59.94_444_8': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080i@59.94_422_8': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080i@59.94_RGB_10': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080i@59.94_444_10': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080i@59.94_422_10': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080i@59.94_RGB_12': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080i@59.94_444_12': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-59.94 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080i@59.94_422_12': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-59.94 Vsync:5 TMDS_Clock:74.176' ,\
   
    'EIA1920x1080i@60_RGB_8': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@60_444_8': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@60_422_8': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@60_RGB_10': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@60_444_10': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@60_422_10': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@60_RGB_12': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@60_444_12': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-60.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080i@60_422_12': 'Video_Format:1920x1080i_59.94/60Hz_VIC=5 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-60.00 Vsync:5 TMDS_Clock:74.250' ,\
 
    'EIA1920x1080p@23.98_RGB_8': 'Video_Format:1920x1080p_@Hz_VIC=72 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.98_422_8': 'Video_Format:1920x1080p_@Hz_VIC=72 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.98_444_8': 'Video_Format:1920x1080p_@Hz_VIC=72 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@59.94_RGB_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.43 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:59.94 Vsync:5 TMDS_Clock:148.351' ,\
    'EIA1920x1080p@59.94_422_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.43 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:59.94 Vsync:5 TMDS_Clock:148.351' ,\
    'EIA1920x1080p@59.94_444_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.43 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:59.94 Vsync:5 TMDS_Clock:148.351' ,\
    'EIA1920x1080p@60_RGB_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_422_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_444_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\

    'EIA1920x1080p@23.97_RGB_8': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.97_444_8': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.97_422_8': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.97_RGB_10': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.97_444_10': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.97_422_10': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.97_RGB_12': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.97_444_12': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@23.97_422_12': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:26.97 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:23.98 Vsync:5 TMDS_Clock:74.176' ,\
   
    'EIA1920x1080p@24_RGB_8': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2750 Hfront:638 Hfreq:27.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:24.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@24_444_8': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:27.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:24.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@24_422_8': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:27.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:24.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@24_RGB_10': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2750 Hfront:638 Hfreq:27.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:24.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@24_444_10': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:27.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:24.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@24_422_10': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:27.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:24.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@24_RGB_12': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2750 Hfront:638 Hfreq:27.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:24.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@24_444_12': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:27.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:24.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@24_422_12': 'Video_Format:1920x1080p_23.97/24Hz_VIC=32 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2750 Hfront:638 Hfreq:27.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:24.00 Vsync:5 TMDS_Clock:74.250' ,\
    
    'EIA1920x1080p@30_RGB_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_444_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_422_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_RGB_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_444_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_422_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_RGB_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_444_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    'EIA1920x1080p@30_422_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.75 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:30.00 Vsync:5 TMDS_Clock:74.250' ,\
    
    'EIA1920x1080p@50_RGB_8': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_444_8': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_422_8': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_RGB_10': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_444_10': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_422_10': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_RGB_12': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_444_12': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@50_422_12': 'Video_Format:1920x1080p_50Hz_VIC=31 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:50.00 Vsync:5 TMDS_Clock:148.500' ,\
    
    'EIA1920x1080p@60_RGB_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_444_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_422_8': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_RGB_10': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_444_10': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_422_10': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_RGB_12': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_444_12': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080p@60_422_12': 'Video_Format:1920x1080p_59.9/60Hz_VIC=16 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:60.00 Vsync:5 TMDS_Clock:148.500' ,\
   
    'EIA640x480p@59.94_RGB_8': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_444_8': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:4:4 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_422_8': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:2:2 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_RGB_10': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:30 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_444_10': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:30 RGB_YCC:4:4:4 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_422_10': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:2:2 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_RGB_12': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:36 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_444_12': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:36 RGB_YCC:4:4:4 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'EIA640x480p@59.94_422_12': 'Video_Format:640x480p_59.94/60Hz_VIC=1 Color_Depth:24 RGB_YCC:4:2:2 Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    
    'EIA2880x480p@59.94_RGB_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_444_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_422_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_RGB_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:30 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:63 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_444_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:30 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:63 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_422_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_RGB_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:36 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_444_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:36 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    'EIA2880x480p@59.94_422_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.47 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:59.94 Vsync:6 TMDS_Clock:108.000' ,\
    
    'EIA2880x480p@60_RGB_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_444_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_422_8': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_RGB_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:30 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_444_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:30 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:63 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_422_10': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_RGB_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:36 RGB_YCC:RGB Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_444_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:36 RGB_YCC:4:4:4 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    'EIA2880x480p@60_422_12': 'Video_Format:2880x480p_59.94/60Hz_VIC=35 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3432 Hfront:64 Hfreq:31.50 Hsync:248 Vactive:480 Vtotal:525 Vfront:9 Vfreq:60.00 Vsync:6 TMDS_Clock:108.108' ,\
    
    'EIA2880x576p@50_RGB_8': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:RGB Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_444_8': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:4:4:4 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_422_8': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_RGB_10': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:30 RGB_YCC:RGB Hactive:2880 Htotal:3456 Hfront:47 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_444_10': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:30 RGB_YCC:4:4:4 Hactive:2880 Htotal:3456 Hfront:47 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_422_10': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_RGB_12': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:36 RGB_YCC:RGB Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_444_12': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:36 RGB_YCC:4:4:4 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    'EIA2880x576p@50_422_12': 'Video_Format:2880x576p_50Hz_VIC=37 Color_Depth:24 RGB_YCC:4:2:2 Hactive:2880 Htotal:3456 Hfront:48 Hfreq:31.25 Hsync:256 Vactive:576 Vtotal:625 Vfront:5 Vfreq:50.00 Vsync:5 TMDS_Clock:108.000' ,\
    
    'EIA1920x1080p@29.97_RGB_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_444_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_422_8': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_RGB_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_444_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_422_10': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_RGB_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_444_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    'EIA1920x1080p@29.97_422_12': 'Video_Format:1920x1080p_29.97/30Hz_VIC=34 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:33.72 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:29.97 Vsync:5 TMDS_Clock:74.176' ,\
    
    'EIA1440x480i@120_RGB_8': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_444_8': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_422_8': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_RGB_10': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_444_10': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_422_10': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_RGB_12': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_444_12': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    'EIA1440x480i@120_422_12': 'Video_Format:720(1440)x480i_119.88/120Hz_VIC=50 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:31.50 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:120.00 Vsync:3 TMDS_Clock:54.054' ,\
    
    'EIA1440x480i@240_RGB_8': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.672' ,\
    'EIA1440x480i@240_444_8': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.099' ,\
    'EIA1440x480i@240_422_8': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.099' ,\
    'EIA1440x480i@240_RGB_10': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:63.664' ,\
    'EIA1440x480i@240_444_10': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:37 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.379' ,\
    'EIA1440x480i@240_422_10': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:63.706' ,\
    'EIA1440x480i@240_RGB_12': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:64.280' ,\
    'EIA1440x480i@240_444_12': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:63.680' ,\
    'EIA1440x480i@240_422_12': 'Video_Format:720(1440)x480i_239.76/240Hz_VIC=58 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1716 Hfront:38 Hfreq:63.00 Hsync:124 Vactive:240 Vtotal:263 Vfront:4 Vfreq:240.00 Vsync:3 TMDS_Clock:65.056' ,\
    
    'EIA720x480p@120_RGB_8': 'Video_Format:720x480p_119.88/120Hz_VIC=48 Color_Depth:24 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:63.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:120.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA720x480p@120_444_8': 'Video_Format:720x480p_119.88/120Hz_VIC=48 Color_Depth:24 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:63.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:120.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA720x480p@120_422_8': 'Video_Format:720x480p_119.88/120Hz_VIC=48 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:63.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:120.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA720x480p@120_RGB_10': 'Video_Format:720x480p_119.88/120Hz_VIC=48 Color_Depth:30 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:63.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:120.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA720x480p@120_444_10': 'Video_Format:720x480p_119.88/120Hz_VIC=48 Color_Depth:30 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:63.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:120.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA720x480p@120_422_10': 'Video_Format:720x480p_119.88/120Hz_VIC=48 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:63.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:120.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA720x480p@120_RGB_12': 'Video_Format:720x480p_119.88/120Hz_VIC=48 Color_Depth:36 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:63.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:120.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA720x480p@120_444_12': 'Video_Format:720x480p_119.88/120Hz_VIC=48 Color_Depth:36 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:63.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:120.00 Vsync:6 TMDS_Clock:54.054' ,\
    'EIA720x480p@120_422_12': 'Video_Format:720x480p_119.88/120Hz_VIC=48 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:63.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:120.00 Vsync:6 TMDS_Clock:54.054' ,\
    
    'EIA720x480p@240_RGB_8': 'Video_Format:720x480p_239.76/240Hz_VIC=56 Color_Depth:24 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:126.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:240.00 Vsync:6 TMDS_Clock:63.706' ,\
    'EIA720x480p@240_444_8': 'Video_Format:720x480p_239.76/240Hz_VIC=56 Color_Depth:24 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:126.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:240.00 Vsync:6 TMDS_Clock:64.672' ,\
    'EIA720x480p@240_422_8': 'Video_Format:720x480p_239.76/240Hz_VIC=56 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:126.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:240.00 Vsync:6 TMDS_Clock:64.672' ,\
    'EIA720x480p@240_RGB_10': 'Video_Format:720x480p_239.76/240Hz_VIC=56 Color_Depth:30 RGB_YCC:RGB Hactive:721 Htotal:858 Hfront:16 Hfreq:126.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:240.00 Vsync:6 TMDS_Clock:64.379' ,\
    'EIA720x480p@240_444_10': 'Video_Format:720x480p_239.76/240Hz_VIC=56 Color_Depth:30 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:126.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:240.00 Vsync:6 TMDS_Clock:64.379' ,\
    'EIA720x480p@240_422_10': 'Video_Format:720x480p_239.76/240Hz_VIC=56 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:126.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:240.00 Vsync:6 TMDS_Clock:64.672' ,\
    'EIA720x480p@240_RGB_12': 'Video_Format:720x480p_239.76/240Hz_VIC=56 Color_Depth:36 RGB_YCC:RGB Hactive:720 Htotal:858 Hfront:16 Hfreq:126.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:240.00 Vsync:6 TMDS_Clock:64.280' ,\
    'EIA720x480p@240_444_12': 'Video_Format:720x480p_239.76/240Hz_VIC=56 Color_Depth:36 RGB_YCC:4:4:4 Hactive:720 Htotal:858 Hfront:16 Hfreq:126.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:240.00 Vsync:6 TMDS_Clock:64.280' ,\
    'EIA720x480p@240_422_12': 'Video_Format:720x480p_239.76/240Hz_VIC=56 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:858 Hfront:16 Hfreq:126.00 Hsync:62 Vactive:480 Vtotal:525 Vfront:9 Vfreq:240.00 Vsync:6 TMDS_Clock:64.672' ,\
    
    'EIA1440x576i@100_RGB_8': 'Video_Format:720(1440)x576i_100Hz_VIC=44 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:100.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA1440x576i@100_444_8': 'Video_Format:720(1440)x576i_100Hz_VIC=44 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:100.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA1440x576i@100_422_8': 'Video_Format:720(1440)x576i_100Hz_VIC=44 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:100.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA1440x576i@100_RGB_10': 'Video_Format:720(1440)x576i_100Hz_VIC=44 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:100.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA1440x576i@100_444_10': 'Video_Format:720(1440)x576i_100Hz_VIC=44 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:100.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA1440x576i@100_422_10': 'Video_Format:720(1440)x576i_100Hz_VIC=44 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:100.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA1440x576i@100_RGB_12': 'Video_Format:720(1440)x576i_100Hz_VIC=44 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:100.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA1440x576i@100_444_12': 'Video_Format:720(1440)x576i_100Hz_VIC=44 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:100.00 Vsync:3 TMDS_Clock:54.000' ,\
    'EIA1440x576i@100_422_12': 'Video_Format:720(1440)x576i_100Hz_VIC=44 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:31.25 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:100.00 Vsync:3 TMDS_Clock:54.000' ,\
    
    'EIA1440x576i@200_RGB_8': 'Video_Format:720(1440)x576i_200Hz_VIC=54 Color_Depth:24 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:62.50 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:200.00 Vsync:3 TMDS_Clock:77.478' ,\
    'EIA1440x576i@200_444_8': 'Video_Format:720(1440)x576i_200Hz_VIC=54 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:62.50 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:200.00 Vsync:3 TMDS_Clock:77.478' ,\
    'EIA1440x576i@200_422_8': 'Video_Format:720(1440)x576i_200Hz_VIC=54 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:62.50 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:200.00 Vsync:3 TMDS_Clock:77.478' ,\
    'EIA1440x576i@200_RGB_10': 'Video_Format:720(1440)x576i_200Hz_VIC=54 Color_Depth:30 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:62.50 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:200.00 Vsync:3 TMDS_Clock:76.931' ,\
    'EIA1440x576i@200_444_10': 'Video_Format:720(1440)x576i_200Hz_VIC=54 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:62.50 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:200.00 Vsync:3 TMDS_Clock:76.931' ,\
    'EIA1440x576i@200_422_10': 'Video_Format:720(1440)x576i_200Hz_VIC=54 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:62.50 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:200.00 Vsync:3 TMDS_Clock:77.478' ,\
    'EIA1440x576i@200_RGB_12': 'Video_Format:720(1440)x576i_200Hz_VIC=54 Color_Depth:36 RGB_YCC:RGB Hactive:1440 Htotal:1728 Hfront:24 Hfreq:62.50 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:200.00 Vsync:3 TMDS_Clock:76.131' ,\
    'EIA1440x576i@200_444_12': 'Video_Format:720(1440)x576i_200Hz_VIC=54 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:62.50 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:200.00 Vsync:3 TMDS_Clock:76.131' ,\
    'EIA1440x576i@200_422_12': 'Video_Format:720(1440)x576i_200Hz_VIC=54 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1440 Htotal:1728 Hfront:24 Hfreq:62.50 Hsync:126 Vactive:288 Vtotal:313 Vfront:2 Vfreq:200.00 Vsync:3 TMDS_Clock:77.478' ,\
    
    'EIA720x576p@100_RGB_8': 'Video_Format:720x576p_100Hz_VIC=42 Color_Depth:24 RGB_YCC:RGB Hactive:720 Htotal:864 Hfront:12 Hfreq:62.50 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA720x576p@100_444_8': 'Video_Format:720x576p_100Hz_VIC=42 Color_Depth:24 RGB_YCC:4:4:4 Hactive:720 Htotal:864 Hfront:12 Hfreq:62.50 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA720x576p@100_422_8': 'Video_Format:720x576p_100Hz_VIC=42 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:864 Hfront:12 Hfreq:62.50 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA720x576p@100_RGB_10': 'Video_Format:720x576p_100Hz_VIC=42 Color_Depth:30 RGB_YCC:RGB Hactive:720 Htotal:864 Hfront:12 Hfreq:62.50 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA720x576p@100_444_10': 'Video_Format:720x576p_100Hz_VIC=42 Color_Depth:30 RGB_YCC:4:4:4 Hactive:721 Htotal:864 Hfront:12 Hfreq:62.50 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA720x576p@100_422_10': 'Video_Format:720x576p_100Hz_VIC=42 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:864 Hfront:12 Hfreq:62.50 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA720x576p@100_RGB_12': 'Video_Format:720x576p_100Hz_VIC=42 Color_Depth:36 RGB_YCC:RGB Hactive:720 Htotal:864 Hfront:12 Hfreq:62.50 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA720x576p@100_444_12': 'Video_Format:720x576p_100Hz_VIC=42 Color_Depth:36 RGB_YCC:4:4:4 Hactive:720 Htotal:864 Hfront:12 Hfreq:62.50 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:54.000' ,\
    'EIA720x576p@100_422_12': 'Video_Format:720x576p_100Hz_VIC=42 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:864 Hfront:12 Hfreq:62.50 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:54.000' ,\
    
    'EIA720x576p@200_RGB_8': 'Video_Format:720x576p_200Hz_VIC=52 Color_Depth:24 RGB_YCC:RGB Hactive:720 Htotal:864 Hfront:12 Hfreq:125.00 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:200.00 Vsync:5 TMDS_Clock:76.645' ,\
    'EIA720x576p@200_444_8': 'Video_Format:720x576p_200Hz_VIC=52 Color_Depth:24 RGB_YCC:4:4:4 Hactive:720 Htotal:864 Hfront:12 Hfreq:125.00 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:200.00 Vsync:5 TMDS_Clock:77.806' ,\
    'EIA720x576p@200_422_8': 'Video_Format:720x576p_200Hz_VIC=52 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:864 Hfront:12 Hfreq:125.00 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:200.00 Vsync:5 TMDS_Clock:76.645' ,\
    'EIA720x576p@200_RGB_10': 'Video_Format:720x576p_200Hz_VIC=52 Color_Depth:30 RGB_YCC:RGB Hactive:721 Htotal:864 Hfront:12 Hfreq:125.00 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:200.00 Vsync:5 TMDS_Clock:77.351' ,\
    'EIA720x576p@200_444_10': 'Video_Format:720x576p_200Hz_VIC=52 Color_Depth:30 RGB_YCC:4:4:4 Hactive:721 Htotal:864 Hfront:12 Hfreq:125.00 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:200.00 Vsync:5 TMDS_Clock:77.351' ,\
    'EIA720x576p@200_422_10': 'Video_Format:720x576p_200Hz_VIC=52 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:864 Hfront:12 Hfreq:125.00 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:200.00 Vsync:5 TMDS_Clock:77.806' ,\
    'EIA720x576p@200_RGB_12': 'Video_Format:720x576p_200Hz_VIC=52 Color_Depth:36 RGB_YCC:RGB Hactive:720 Htotal:864 Hfront:12 Hfreq:125.00 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:200.00 Vsync:5 TMDS_Clock:77.902' ,\
    'EIA720x576p@200_444_12': 'Video_Format:720x576p_200Hz_VIC=52 Color_Depth:36 RGB_YCC:4:4:4 Hactive:720 Htotal:864 Hfront:12 Hfreq:125.00 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:200.00 Vsync:5 TMDS_Clock:77.902' ,\
    'EIA720x576p@200_422_12': 'Video_Format:720x576p_200Hz_VIC=52 Color_Depth:24 RGB_YCC:4:2:2 Hactive:720 Htotal:864 Hfront:12 Hfreq:125.00 Hsync:64 Vactive:576 Vtotal:625 Vfront:5 Vfreq:200.00 Vsync:5 TMDS_Clock:77.806' ,\
    
    'EIA1280x720p@100_RGB_8': 'Video_Format:1280x720p_100Hz_VIC=41 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:1980 Hfront:440 Hfreq:75.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@100_444_8': 'Video_Format:1280x720p_100Hz_VIC=41 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:75.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@100_422_8': 'Video_Format:1280x720p_100Hz_VIC=41 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:75.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@100_RGB_10': 'Video_Format:1280x720p_100Hz_VIC=41 Color_Depth:30 RGB_YCC:RGB Hactive:1281 Htotal:1980 Hfront:440 Hfreq:75.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@100_444_10': 'Video_Format:1280x720p_100Hz_VIC=41 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:75.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@100_422_10': 'Video_Format:1280x720p_100Hz_VIC=41 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:75.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@100_RGB_12': 'Video_Format:1280x720p_100Hz_VIC=41 Color_Depth:36 RGB_YCC:RGB Hactive:1280 Htotal:1980 Hfront:440 Hfreq:75.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@100_444_12': 'Video_Format:1280x720p_100Hz_VIC=41 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:75.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@100_422_12': 'Video_Format:1280x720p_100Hz_VIC=41 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1980 Hfront:440 Hfreq:75.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:100.00 Vsync:5 TMDS_Clock:148.500' ,\
    
    'EIA1280x720p@120_RGB_8': 'Video_Format:1280x720p_119.88/120Hz_VIC=47 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:1650 Hfront:110 Hfreq:90.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@120_444_8': 'Video_Format:1280x720p_119.88/120Hz_VIC=47 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:90.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@120_422_8': 'Video_Format:1280x720p_119.88/120Hz_VIC=47 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:90.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@120_RGB_10': 'Video_Format:1280x720p_119.88/120Hz_VIC=47 Color_Depth:30 RGB_YCC:RGB Hactive:1281 Htotal:1650 Hfront:110 Hfreq:90.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@120_444_10': 'Video_Format:1280x720p_119.88/120Hz_VIC=47 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1281 Htotal:1650 Hfront:110 Hfreq:90.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@120_422_10': 'Video_Format:1280x720p_119.88/120Hz_VIC=47 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:90.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@120_RGB_12': 'Video_Format:1280x720p_119.88/120Hz_VIC=47 Color_Depth:36 RGB_YCC:RGB Hactive:1280 Htotal:1650 Hfront:110 Hfreq:90.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@120_444_12': 'Video_Format:1280x720p_119.88/120Hz_VIC=47 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:90.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1280x720p@120_422_12': 'Video_Format:1280x720p_119.88/120Hz_VIC=47 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1280 Htotal:1650 Hfront:110 Hfreq:90.00 Hsync:40 Vactive:720 Vtotal:750 Vfront:5 Vfreq:120.00 Vsync:5 TMDS_Clock:148.500' ,\
    
    'EIA1920x1080i@100_RGB_8': 'Video_Format:1920x1080i_100Hz_VIC=40 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@100_444_8': 'Video_Format:1920x1080i_100Hz_VIC=40 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@100_422_8': 'Video_Format:1920x1080i_100Hz_VIC=40 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@100_RGB_10': 'Video_Format:1920x1080i_100Hz_VIC=40 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@100_444_10': 'Video_Format:1920x1080i_100Hz_VIC=40 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@100_422_10': 'Video_Format:1920x1080i_100Hz_VIC=40 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@100_RGB_12': 'Video_Format:1920x1080i_100Hz_VIC=40 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@100_444_12': 'Video_Format:1920x1080i_100Hz_VIC=40 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-100.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@100_422_12': 'Video_Format:1920x1080i_100Hz_VIC=40 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:56.25 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-100.00 Vsync:5 TMDS_Clock:148.500' ,\
    
    'EIA1920x1080i@120_RGB_8': 'Video_Format:1920x1080i_119.88/120Hz_VIC=46 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@120_444_8': 'Video_Format:1920x1080i_119.88/120Hz_VIC=46 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@120_422_8': 'Video_Format:1920x1080i_119.88/120Hz_VIC=46 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@120_RGB_10': 'Video_Format:1920x1080i_119.88/120Hz_VIC=46 Color_Depth:30 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@120_444_10': 'Video_Format:1920x1080i_119.88/120Hz_VIC=46 Color_Depth:30 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@120_422_10': 'Video_Format:1920x1080i_119.88/120Hz_VIC=46 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@120_RGB_12': 'Video_Format:1920x1080i_119.88/120Hz_VIC=46 Color_Depth:36 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@120_444_12': 'Video_Format:1920x1080i_119.88/120Hz_VIC=46 Color_Depth:36 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-120.00 Vsync:5 TMDS_Clock:148.500' ,\
    'EIA1920x1080i@120_422_12': 'Video_Format:1920x1080i_119.88/120Hz_VIC=46 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:67.50 Hsync:44 Vactive:540 Vtotal:563 Vfront:2 Vfreq:-120.00 Vsync:5 TMDS_Clock:148.500' ,\
    
    'EIA1920x1080p@100_RGB_8': 'Video_Format:1920x1080p_100Hz_VIC=64 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2640 Hfront:528 Hfreq:112.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:100.00 Vsync:5 TMDS_Clock:297.000',\
    'EIA1920x1080p@100_444_8': 'Video_Format:1920x1080p_100Hz_VIC=64 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:112.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:100.00 Vsync:5 TMDS_Clock:297.000',\
    'EIA1920x1080p@100_422_8': 'Video_Format:1920x1080p_100Hz_VIC=64 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2640 Hfront:528 Hfreq:112.50 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:100.00 Vsync:5 TMDS_Clock:297.000',\
    
    'EIA1920x1080p@120_RGB_8': 'Video_Format:1920x1080p_119.88/120Hz_VIC=63 Color_Depth:24 RGB_YCC:RGB Hactive:1920 Htotal:2200 Hfront:88 Hfreq:135.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:120.00 Vsync:5 TMDS_Clock:297.000',\
    'EIA1920x1080p@120_444_8': 'Video_Format:1920x1080p_119.88/120Hz_VIC=63 Color_Depth:24 RGB_YCC:4:4:4 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:135.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:120.00 Vsync:5 TMDS_Clock:297.000',\
    'EIA1920x1080p@120_422_8': 'Video_Format:1920x1080p_119.88/120Hz_VIC=63 Color_Depth:24 RGB_YCC:4:2:2 Hactive:1920 Htotal:2200 Hfront:88 Hfreq:135.00 Hsync:44 Vactive:1080 Vtotal:1125 Vfront:4 Vfreq:120.00 Vsync:5 TMDS_Clock:297.000',\
 
    'VESA640x480@60_RGB_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:RGB Hactive:640 Htotal:800 Hfront:16 Hfreq:31.47 Hsync:96 Vactive:480 Vtotal:525 Vfront:10 Vfreq:59.94 Vsync:2 TMDS_Clock:25.175' ,\
    'VESA800x600@60_RGB_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:RGB Hactive:800 Htotal:1056 Hfront:40 Hfreq:37.88 Hsync:128 Vactive:600 Vtotal:628 Vfront:1 Vfreq:60.32 Vsync:4 TMDS_Clock:40.000' ,\
    'VESA1024x768@60_RGB_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:RGB Hactive:1024 Htotal:1344 Hfront:24 Hfreq:48.36 Hsync:136 Vactive:768 Vtotal:806 Vfront:3 Vfreq:60.00 Vsync:6 TMDS_Clock:65.000' ,\
    'VESA1280x1024@60_RGB_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:RGB Hactive:1280 Htotal:1688 Hfront:48 Hfreq:63.98 Hsync:112 Vactive:1024 Vtotal:1066 Vfront:1 Vfreq:60.02 Vsync:3 TMDS_Clock:108.000' ,\
    'VESA1600x1200@60_RGB_8': 'Video_Format:No_VideoHz_VIC=0 Color_Depth:24 RGB_YCC:RGB Hactive:1600 Htotal:2160 Hfront:64 Hfreq:75.00 Hsync:192 Vactive:1200 Vtotal:1250 Vfront:1 Vfreq:60.00 Vsync:3 TMDS_Clock:162.000' ,\

    '3D 480i60 FramePack_RGB_8': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) frame packing' ,\
    '3D 480i60 FramePack_444_8': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) frame packing' ,\
    '3D 480i60 FramePack_422_8': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) frame packing' ,\
    
    '3D 480p60 FramePack_RGB_8': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) frame packing' ,\
    '3D 480p60 FramePack_444_8': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) frame packing' ,\
    '3D 480p60 FramePack_422_8': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) frame packing' ,\
    
    '3D 576i50 FramePack_RGB_8': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) frame packing' ,\
    '3D 576i50 FramePack_444_8': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) frame packing' ,\
    '3D 576i50 FramePack_422_8': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) frame packing' ,\
    
    '3D 576p50 FramePack_RGB_8': 'VIC=17 (720x576p 50Hz, 4:3,16:15) frame packing' ,\
    '3D 576p50 FramePack_444_8': 'VIC=17 (720x576p 50Hz, 4:3,16:15) frame packing' ,\
    '3D 576p50 FramePack_422_8': 'VIC=17 (720x576p 50Hz, 4:3,16:15) frame packing' ,\
    
    '3D 720p24 FramePack_RGB_8': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) frame packing' ,\
    '3D 720p24 FramePack_444_8': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) frame packing' ,\
    '3D 720p24 FramePack_422_8': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) frame packing' ,\
    
    '3D 720p30 FramePack_RGB_8': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) frame packing' ,\
    '3D 720p30 FramePack_444_8': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) frame packing' ,\
    '3D 720p30 FramePack_422_8': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) frame packing' ,\
    
    '3D 720p50 FramePack_RGB_8': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) frame packing' ,\
    '3D 720p50 FramePack_444_8': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) frame packing' ,\
    '3D 720p50 FramePack_422_8': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) frame packing' ,\
    '3D 720p60 FramePack_RGB_8': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) frame packing' ,\
    '3D 720p60 FramePack_444_8': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) frame packing' ,\
    '3D 720p60 FramePack_422_8': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) frame packing' ,\
    '3D 1080i50 FramePack_RGB_8': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080i50 FramePack_444_8': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080i50 FramePack_422_8': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080i60 FramePack_RGB_8': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) frame packing' ,\
    '3D 1080i60 FramePack_444_8': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) frame packing' ,\
    '3D 1080i60 FramePack_422_8': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) frame packing' ,\
    '3D 1080p24 FramePack_RGB_8': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p24 FramePack_444_8': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p24 FramePack_422_8': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p30 FramePack_RGB_8': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p30 FramePack_444_8': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p30 FramePack_422_8': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p50 FramePack_RGB_8': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p50 FramePack_444_8': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p50 FramePack_422_8': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p60 FramePack_RGB_8': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) frame packing' ,\
    '3D 1080p60 FramePack_444_8': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) frame packing' ,\
    '3D 1080p60 FramePack_422_8': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) frame packing' ,\
    '3D 480i60 TopandBot_RGB_8': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Top-and-Bottom' ,\
    '3D 480i60 TopandBot_444_8': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Top-and-Bottom' ,\
    '3D 480i60 TopandBot_422_8': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Top-and-Bottom' ,\
    '3D 480p60 TopandBot_RGB_8': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Top-and-Bottom' ,\
    '3D 480p60 TopandBot_444_8': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Top-and-Bottom' ,\
    '3D 480p60 TopandBot_422_8': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Top-and-Bottom' ,\
    '3D 576i50 TopandBot_RGB_8': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Top-and-Bottom' ,\
    '3D 576i50 TopandBot_444_8': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Top-and-Bottom' ,\
    '3D 576i50 TopandBot_422_8': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Top-and-Bottom' ,\
    '3D 576p50 TopandBot_RGB_8': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Top-and-Bottom' ,\
    '3D 576p50 TopandBot_444_8': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Top-and-Bottom' ,\
    '3D 576p50 TopandBot_422_8': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Top-and-Bottom' ,\
    '3D 720p24 TopandBot_RGB_8': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Top-and-Bottom' ,\
    '3D 720p24 TopandBot_444_8': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Top-and-Bottom' ,\
    '3D 720p24 TopandBot_422_8': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Top-and-Bottom' ,\
    '3D 720p30 TopandBot_RGB_8': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Top-and-Bottom' ,\
    '3D 720p30 TopandBot_444_8': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Top-and-Bottom' ,\
    '3D 720p30 TopandBot_422_8': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Top-and-Bottom' ,\
    '3D 720p50 TopandBot_RGB_8': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 720p50 TopandBot_444_8': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 720p50 TopandBot_422_8': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 720p60 TopandBot_RGB_8': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Top-and-Bottom' ,\
    '3D 720p60 TopandBot_444_8': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Top-and-Bottom' ,\
    '3D 720p60 TopandBot_422_8': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Top-and-Bottom' ,\
    '3D 1080i50 TopandBot_RGB_8': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080i50 TopandBot_444_8': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080i50 TopandBot_422_8': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080i60 TopandBot_RGB_8': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Top-and-Bottom' ,\
    '3D 1080i60 TopandBot_444_8': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Top-and-Bottom' ,\
    '3D 1080i60 TopandBot_422_8': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Top-and-Bottom' ,\
    '3D 1080p24 TopandBot_RGB_8': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p24 TopandBot_444_8': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p24 TopandBot_422_8': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p30 TopandBot_RGB_8': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p30 TopandBot_444_8': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p30 TopandBot_422_8': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p50 TopandBot_RGB_8': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p50 TopandBot_444_8': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p50 TopandBot_422_8': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p60 TopandBot_RGB_8': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p60 TopandBot_444_8': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Top-and-Bottom' ,\
    '3D 1080p60 TopandBot_422_8': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Top-and-Bottom' ,\
    '3D 480i60 Side_half_RGB_8_HHOO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_444_8_HHOO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_422_8_HHOO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_RGB_8_HHOO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_444_8_HHOO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_422_8_HHOO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_RGB_8_HHOO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_444_8_HHOO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_422_8_HHOO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_RGB_8_HHOO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_444_8_HHOO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_422_8_HHOO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_RGB_8_HHOO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_444_8_HHOO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_422_8_HHOO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_RGB_8_HHOO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_444_8_HHOO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_422_8_HHOO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_RGB_8_HHOO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_444_8_HHOO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_422_8_HHOO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_RGB_8_HHOO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_444_8_HHOO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_422_8_HHOO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_RGB_8_HHOO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_444_8_HHOO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_422_8_HHOO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_RGB_8_HHOO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_444_8_HHOO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_422_8_HHOO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_RGB_8_HHOO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_444_8_HHOO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_422_8_HHOO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_RGB_8_HHOO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_444_8_HHOO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_422_8_HHOO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_RGB_8_HHOO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_444_8_HHOO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_422_8_HHOO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_RGB_8_HHOO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_444_8_HHOO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_422_8_HHOO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_RGB_8_HHOE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 480i60 Side_half_444_8_HHOE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 480i60 Side_half_422_8_HHOE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 480p60 Side_half_RGB_8_HHOE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 480p60 Side_half_444_8_HHOE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 480p60 Side_half_422_8_HHOE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 576i50 Side_half_RGB_8_HHOE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 576i50 Side_half_444_8_HHOE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 576i50 Side_half_422_8_HHOE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 576p50 Side_half_RGB_8_HHOE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 576p50 Side_half_444_8_HHOE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 576p50 Side_half_422_8_HHOE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p24 Side_half_RGB_8_HHOE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p24 Side_half_444_8_HHOE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p24 Side_half_422_8_HHOE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p30 Side_half_RGB_8_HHOE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p30 Side_half_444_8_HHOE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p30 Side_half_422_8_HHOE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p50 Side_half_RGB_8_HHOE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p50 Side_half_444_8_HHOE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p50 Side_half_422_8_HHOE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p60 Side_half_RGB_8_HHOE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p60 Side_half_444_8_HHOE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 720p60 Side_half_422_8_HHOE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_RGB_8_HHOE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_444_8_HHOE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_422_8_HHOE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_RGB_8_HHOE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_444_8_HHOE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_422_8_HHOE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_RGB_8_HHOE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_444_8_HHOE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_422_8_HHOE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_RGB_8_HHOE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_444_8_HHOE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_422_8_HHOE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_RGB_8_HHOE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_444_8_HHOE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_422_8_HHOE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_RGB_8_HHOE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_444_8_HHOE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_422_8_HHOE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing odd/left picture, even/right picture' ,\
    '3D 480i60 Side_half_RGB_8_HHEO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_444_8_HHEO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_422_8_HHEO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_RGB_8_HHEO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_444_8_HHEO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_422_8_HHEO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_RGB_8_HHEO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_444_8_HHEO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_422_8_HHEO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_RGB_8_HHEO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_444_8_HHEO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_422_8_HHEO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_RGB_8_HHEO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_444_8_HHEO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_422_8_HHEO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_RGB_8_HHEO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_444_8_HHEO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_422_8_HHEO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_RGB_8_HHEO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_444_8_HHEO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_422_8_HHEO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_RGB_8_HHEO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_444_8_HHEO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_422_8_HHEO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_RGB_8_HHEO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_444_8_HHEO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_422_8_HHEO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_RGB_8_HHEO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_444_8_HHEO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_422_8_HHEO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_RGB_8_HHEO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_444_8_HHEO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_422_8_HHEO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_RGB_8_HHEO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_444_8_HHEO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_422_8_HHEO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_RGB_8_HHEO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_444_8_HHEO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_422_8_HHEO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_RGB_8_HHEO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_444_8_HHEO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_422_8_HHEO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_RGB_8_HHEE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 480i60 Side_half_444_8_HHEE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 480i60 Side_half_422_8_HHEE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 480p60 Side_half_RGB_8_HHEE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 480p60 Side_half_444_8_HHEE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 480p60 Side_half_422_8_HHEE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 576i50 Side_half_RGB_8_HHEE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 576i50 Side_half_444_8_HHEE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 576i50 Side_half_422_8_HHEE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 576p50 Side_half_RGB_8_HHEE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 576p50 Side_half_444_8_HHEE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 576p50 Side_half_422_8_HHEE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p24 Side_half_RGB_8_HHEE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p24 Side_half_444_8_HHEE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p24 Side_half_422_8_HHEE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p30 Side_half_RGB_8_HHEE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p30 Side_half_444_8_HHEE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p30 Side_half_422_8_HHEE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p50 Side_half_RGB_8_HHEE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p50 Side_half_444_8_HHEE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p50 Side_half_422_8_HHEE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p60 Side_half_RGB_8_HHEE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p60 Side_half_444_8_HHEE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 720p60 Side_half_422_8_HHEE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_RGB_8_HHEE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_444_8_HHEE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_422_8_HHEE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_RGB_8_HHEE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_444_8_HHEE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_422_8_HHEE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_RGB_8_HHEE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_444_8_HHEE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_422_8_HHEE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_RGB_8_HHEE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_444_8_HHEE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_422_8_HHEE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_RGB_8_HHEE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_444_8_HHEE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_422_8_HHEE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_RGB_8_HHEE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_444_8_HHEE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_422_8_HHEE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)horizontal sub-frame packing even/left picture, even/right picture' ,\
    '3D 480i60 Side_half_RGB_8_HQOO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_444_8_HQOO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_422_8_HQOO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_RGB_8_HQOO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_444_8_HQOO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_422_8_HQOO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_RGB_8_HQOO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_444_8_HQOO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_422_8_HQOO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_RGB_8_HQOO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_444_8_HQOO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_422_8_HQOO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_RGB_8_HQOO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_444_8_HQOO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_422_8_HQOO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_RGB_8_HQOO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_444_8_HQOO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_422_8_HQOO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_RGB_8_HQOO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_444_8_HQOO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_422_8_HQOO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_RGB_8_HQOO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_444_8_HQOO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_422_8_HQOO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_RGB_8_HQOO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_444_8_HQOO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_422_8_HQOO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_RGB_8_HQOO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_444_8_HQOO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_422_8_HQOO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_RGB_8_HQOO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_444_8_HQOO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_422_8_HQOO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_RGB_8_HQOO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_444_8_HQOO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_422_8_HQOO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_RGB_8_HQOO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_444_8_HQOO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_422_8_HQOO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_RGB_8_HQOO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_444_8_HQOO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_422_8_HQOO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_RGB_8_HQOE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 480i60 Side_half_444_8_HQOE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 480i60 Side_half_422_8_HQOE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 480p60 Side_half_RGB_8_HQOE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 480p60 Side_half_444_8_HQOE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 480p60 Side_half_422_8_HQOE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 576i50 Side_half_RGB_8_HQOE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 576i50 Side_half_444_8_HQOE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 576i50 Side_half_422_8_HQOE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 576p50 Side_half_RGB_8_HQOE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 576p50 Side_half_444_8_HQOE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 576p50 Side_half_422_8_HQOE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p24 Side_half_RGB_8_HQOE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p24 Side_half_444_8_HQOE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p24 Side_half_422_8_HQOE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p30 Side_half_RGB_8_HQOE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p30 Side_half_444_8_HQOE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p30 Side_half_422_8_HQOE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p50 Side_half_RGB_8_HQOE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p50 Side_half_444_8_HQOE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p50 Side_half_422_8_HQOE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p60 Side_half_RGB_8_HQOE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p60 Side_half_444_8_HQOE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 720p60 Side_half_422_8_HQOE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_RGB_8_HQOE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_444_8_HQOE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_422_8_HQOE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_RGB_8_HQOE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_444_8_HQOE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_422_8_HQOE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_RGB_8_HQOE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_444_8_HQOE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_422_8_HQOE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_RGB_8_HQOE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_444_8_HQOE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_422_8_HQOE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_RGB_8_HQOE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_444_8_HQOE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_422_8_HQOE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_RGB_8_HQOE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_444_8_HQOE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_422_8_HQOE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix odd/left picture, even/right picture' ,\
    '3D 480i60 Side_half_RGB_8_HQEO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_444_8_HQEO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_422_8_HQEO': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_RGB_8_HQEO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_444_8_HQEO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 480p60 Side_half_422_8_HQEO': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_RGB_8_HQEO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_444_8_HQEO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 576i50 Side_half_422_8_HQEO': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_RGB_8_HQEO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_444_8_HQEO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 576p50 Side_half_422_8_HQEO': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_RGB_8_HQEO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_444_8_HQEO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p24 Side_half_422_8_HQEO': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_RGB_8_HQEO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_444_8_HQEO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p30 Side_half_422_8_HQEO': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_RGB_8_HQEO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_444_8_HQEO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p50 Side_half_422_8_HQEO': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_RGB_8_HQEO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_444_8_HQEO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 720p60 Side_half_422_8_HQEO': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_RGB_8_HQEO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_444_8_HQEO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080i50 Side_half_422_8_HQEO': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_RGB_8_HQEO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_444_8_HQEO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080i60 Side_half_422_8_HQEO': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_RGB_8_HQEO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_444_8_HQEO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p24 Side_half_422_8_HQEO': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_RGB_8_HQEO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_444_8_HQEO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p30 Side_half_422_8_HQEO': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_RGB_8_HQEO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_444_8_HQEO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p50 Side_half_422_8_HQEO': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_RGB_8_HQEO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_444_8_HQEO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 1080p60 Side_half_422_8_HQEO': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, odd/right picture' ,\
    '3D 480i60 Side_half_RGB_8_HQEE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 480i60 Side_half_444_8_HQEE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 480i60 Side_half_422_8_HQEE': 'VIC=6 (720(1440)x480i 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 480p60 Side_half_RGB_8_HQEE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 480p60 Side_half_444_8_HQEE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 480p60 Side_half_422_8_HQEE': 'VIC=2 (720x480p 59.94/60Hz,4:3,8:9) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 576i50 Side_half_RGB_8_HQEE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 576i50 Side_half_444_8_HQEE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 576i50 Side_half_422_8_HQEE': 'VIC=21 (720(1440)x576i 50Hz, 4:3, 16:15) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 576p50 Side_half_RGB_8_HQEE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 576p50 Side_half_444_8_HQEE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 576p50 Side_half_422_8_HQEE': 'VIC=17 (720x576p 50Hz, 4:3,16:15) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p24 Side_half_RGB_8_HQEE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p24 Side_half_444_8_HQEE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p24 Side_half_422_8_HQEE': 'VIC=60 (1280x720p 23.97/24Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p30 Side_half_RGB_8_HQEE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p30 Side_half_444_8_HQEE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p30 Side_half_422_8_HQEE': 'VIC=62 (1280x720p 29.97/30Hz, 16:9 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p50 Side_half_RGB_8_HQEE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p50 Side_half_444_8_HQEE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p50 Side_half_422_8_HQEE': 'VIC=19 (1280x720p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p60 Side_half_RGB_8_HQEE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p60 Side_half_444_8_HQEE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 720p60 Side_half_422_8_HQEE': 'VIC=4 (1280x720p 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_RGB_8_HQEE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_444_8_HQEE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080i50 Side_half_422_8_HQEE': 'VIC=20 (1920x1080i 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_RGB_8_HQEE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_444_8_HQEE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080i60 Side_half_422_8_HQEE': 'VIC=5 (1920x1080i 59.94/60Hz,16:9,1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_RGB_8_HQEE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_444_8_HQEE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p24 Side_half_422_8_HQEE': 'VIC=32 (1920x1080p 23.97/24Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_RGB_8_HQEE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_444_8_HQEE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p30 Side_half_422_8_HQEE': 'VIC=34 (1920x1080p 29.97/30Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_RGB_8_HQEE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_444_8_HQEE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p50 Side_half_422_8_HQEE': 'VIC=31 (1920x1080p 50Hz, 16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_RGB_8_HQEE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_444_8_HQEE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    '3D 1080p60 Side_half_422_8_HQEE': 'VIC=16 (1920x1080p 59.9/60Hz,16:9, 1:1) Side-by-Side (Half)quincunx matrix even/left picture, even/right picture' ,\
    
    '3D 1080p25 FramePack_RGB_8': 'VIC=33 (1920x1080p 25Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p25 FramePack_422_8': 'VIC=33 (1920x1080p 25Hz, 16:9, 1:1) frame packing' ,\
    '3D 1080p25 FramePack_444_8': 'VIC=33 (1920x1080p 25Hz, 16:9, 1:1) frame packing' ,\
}

audio_golden_timings = {
    '2ch_32 KHz_24-bit': 'AUD check sum:verified AUD channel count:2ch AUD HB:84 01 0a 4a |',
    '2ch_44.1 KHz_24-bit': 'AUD check sum:verified AUD channel count:2ch AUD HB:84 01 0a 4a |',
    '2ch_48 KHz_24-bit': 'AUD check sum:verified AUD channel count:2ch AUD HB:84 01 0a 4a |',
    '2ch_88.2 KHz_24-bit': 'AUD check sum:verified AUD channel count:2ch AUD HB:84 01 0a 4a |',
    '2ch_96 KHz_24-bit': 'AUD check sum:verified AUD channel count:2ch AUD HB:84 01 0a 4a |',
    '2ch_176.4 KHz_24-bit': 'AUD check sum:verified AUD channel count:2ch AUD HB:84 01 0a 4a |',
    '2ch_192 KHz_24-bit': 'AUD check sum:verified AUD channel count:2ch AUD HB:84 01 0a 4a |',
    '4ch_32 KHz_24-bit': 'AUD check sum:verified AUD channel count:4ch AUD HB:84 01 0a 4a |',
    '4ch_44.1 KHz_24-bit': 'AUD check sum:verified AUD channel count:4ch AUD HB:84 01 0a 4a |',
    '4ch_48 KHz_24-bit': 'AUD check sum:verified AUD channel count:4ch AUD HB:84 01 0a 4a |',
    '4ch_88.2 KHz_24-bit': 'AUD check sum:verified AUD channel count:4ch AUD HB:84 01 0a 4a |',
    '4ch_96 KHz_24-bit': 'AUD check sum:verified AUD channel count:4ch AUD HB:84 01 0a 4a |',
    '4ch_176.4 KHz_24-bit': 'AUD check sum:verified AUD channel count:4ch AUD HB:84 01 0a 4a |',
    '4ch_192 KHz_24-bit': 'AUD check sum:verified AUD channel count:4ch AUD HB:84 01 0a 4a |',
    '6ch_32 KHz_24-bit': 'AUD check sum:verified AUD channel count:6ch AUD HB:84 01 0a 4a |',
    '6ch_44.1 KHz_24-bit': 'AUD check sum:verified AUD channel count:6ch AUD HB:84 01 0a 4a |',
    '6ch_48 KHz_24-bit': 'AUD check sum:verified AUD channel count:6ch AUD HB:84 01 0a 4a |',
    '6ch_88.2 KHz_24-bit': 'AUD check sum:verified AUD channel count:6ch AUD HB:84 01 0a 4a |',
    '6ch_96 KHz_24-bit': 'AUD check sum:verified AUD channel count:6ch AUD HB:84 01 0a 4a |',
    '6ch_176.4 KHz_24-bit': 'AUD check sum:verified AUD channel count:6ch AUD HB:84 01 0a 4a |',
    '6ch_192 KHz_24-bit': 'AUD check sum:verified AUD channel count:6ch AUD HB:84 01 0a 4a |',
    '8ch_32 KHz_24-bit': 'AUD check sum:verified AUD channel count:8ch AUD HB:84 01 0a 4a |',
    '8ch_44.1 KHz_24-bit': 'AUD check sum:verified AUD channel count:8ch AUD HB:84 01 0a 4a |',
    '8ch_48 KHz_24-bit': 'AUD check sum:verified AUD channel count:8ch AUD HB:84 01 0a 4a |',
    '8ch_88.2 KHz_24-bit': 'AUD check sum:verified AUD channel count:8ch AUD HB:84 01 0a 4a |',
    '8ch_96 KHz_24-bit': 'AUD check sum:verified AUD channel count:8ch AUD HB:84 01 0a 4a |',
    '8ch_176.4 KHz_24-bit': 'AUD check sum:verified AUD channel count:8ch AUD HB:84 01 0a 4a |',
    '8ch_192 KHz_24-bit': 'AUD check sum:verified AUD channel count:8ch AUD HB:84 01 0a 4a |',
}


@parametrize("device", type=BaseDeviceAdapter, fetch=parametrize.FetchType.LAZY)
@parametrize("listen_keyword")
@parametrize("listen_timeout", type=float, default=3.0)
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

    @parametrize("video_format", type=str, choice=video_golden_timings)
    def test_video_format(self):
        try:
            if re.search("Side_half_", self.video_format,re.I):
                part1, part2 = self.video_format.split('Side_half_')
                program = part1+ "Side_half"
                color_space, color_depth, threed_type = part2.split('_')
            else:    
                program, color_space, color_depth = self.video_format.split('_')
            color_depth += "-bit"
            with self.device.log_subject.listen(self.listen_keyword) as listener:
                if re.search("Side_half_", self.video_format,re.I):
                    self.astro.load_video(program, 'Color Bar SMPTE', color_space, color_depth, video_3d_extension=threed_type)
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
        if re.search("3D", program, re.I) or re.search("4k", program, re.I) or re.search("1080p", program, re.I):
            if re.search("3D", program, re.I):
                #timing_info = qd.get_3d_info(mem_size="big")
                timing_info = self.qd980.get_3d_info(mem_size="big")
            else:    
                #timing_info = qd.get_2d_info(mem_size="big")
                timing_info = self.qd980.get_2d_info(mem_size="big")
        else:
            #timing_info = qd.get_2d_info(mem_size="small")
            timing_info = self.qd980.get_2d_info(mem_size="small")
         
        if re.search("3D", program, re.I):
            self.assertEquals(timing_info, video_golden_timings[self.video_format], "Video timing should be the same with golden value")
        else:    
            actual_timing = trans_info(timing_info.split())
            golden_timing = trans_info(video_golden_timings[self.video_format].split())
            self.assertEquals(actual_timing[0], golden_timing[0], "Actual "+actual_timing[0])
            self.assertEquals(actual_timing[1], golden_timing[1], "Actual "+actual_timing[1])
            self.assertEquals(actual_timing[2], golden_timing[2], "Actual "+actual_timing[2])
            for i in range(3, 14):
                golden = video_golden_timings[self.video_format].split()[i]
                message = "Actual %s, Golden %s" % (timing_info.split()[i], golden)
                if i == 6 or i == 11:
                    #handle float value 
                    if actual_timing[i] == golden_timing[i]:
                        self._pass(message)
                    elif (actual_timing[i] < golden_timing[i] + 1) and (actual_timing[i] > golden_timing[i] - 1):
                        self._warn(message)
                    else:
                        self._fail(message)
                elif i == 13:
                    # TMDS clock
                    if actual_timing[i] == golden_timing[i]:
                        self._pass(message)
                    elif (actual_timing[i] < golden_timing[i] + 5) and (actual_timing[i] > golden_timing[i] - 5):
                        self._warn(message)
                    else:
                        self._fail(message)
                else:
                    #handle int value
                    if actual_timing[i] == golden_timing[i]:
                        self._pass(message)
                    elif (actual_timing[i] == golden_timing[i] + 1) or (actual_timing[i] == golden_timing[i] - 1):
                        self._warn(message)
                    else:
                        self._fail(message)


    @parametrize("audio_format", type=str, choice=audio_golden_timings)
    def test_audio_format(self):
        try:
            video_program = ""
            color_depth = ""
            color_space = ""
            if self.source_type == "mhl3" or self.source_type == "hdmi1x":
                video_program = random.choice(["EIA720x480p@60","EIA720x576p@50","EIA1280x720p@50","EIA1280x720p@60", "EIA1920x1080p@30","EIA1920x1080p@60", "EIA1920x1080i@60", "4K2K 3840x2160p30"])
                color_space = random.choice(["RGB", "444", "422"])
                if video_program == "4K2K 3840x2160p30":
                    #color_space = random.choice(["RGB","444","422","420"]) Currently QD980 analyzer V1.4 not supports 4k_420 very well
                    color_depth = "8-bit"
                else:
                    #color_depth = random.choice(["8-bit","10-bit","12-bit"])
                    #Titian doesn't support deep color
                    color_depth = "8-bit"
            elif self.source_type == "mhl2":
                #video_program = random.choice(["EIA720x480p@60","EIA720x576p@50", "EIA1280x720p@50","EIA1280x720p@60", "EIA1920x1080p@30","EIA1920x1080i@60","EIA1920x1080p@60"])
                video_program = random.choice(["EIA720x480p@60","EIA720x576p@50", "EIA1280x720p@50","EIA1280x720p@60", "EIA1920x1080p@30","EIA1920x1080i@60"])
                color_space = random.choice(["RGB","444","422"])
                color_depth = "8-bit"
            elif self.source_type == "mhl1":
                video_program = random.choice(["EIA720x480p@60","EIA720x576p@50", "EIA1280x720p@50","EIA1280x720p@60", "EIA1920x1080p@30"])
                color_space = random.choice(["RGB","444","422"])
                color_depth = "8-bit"
            else:
                print ("MHL type is wrong! ")
            
            audio_channel_number, audio_frequency, audio_size = self.audio_format.split('_')
            print video_program
            with self.device.log_subject.listen(self.listen_keyword) as listener:
                self.astro.load(video_program, 'Color Bar 100/100-H', color_space, color_depth, audio_channel_number, audio_frequency, audio_size)
                event = listener.get(timeout=self.listen_timeout)
                self.assertIsNotNone(event,
                                     msg="should get log keyword '%s' in %ss" % (self.listen_keyword, self.listen_timeout))
        finally:
            time.sleep(15.0)
            #self.webcam.capture_image(self.capture_image_name)
            #capture_soundrecorder_image(os.path.join(self.capture_image_dir, "%s_sn.jpg" % self.name))
            timing_info = self.qd980.get_audio_info(mem_size="big")
            #timing_info = qd.get_audio_info(mem_size="big")
            self.assertEquals(timing_info, audio_golden_timings[self.format], "Audio Info frame should be the same with golden value")


def trans_info(items):
    print items
    for i in range(3,14):
        if i == 6 or i == 11 or i == 13:
            items[i] = float(items[i].split(":")[1])
        else:
            items[i] = int(items[i].split(":")[1])
    return items        
