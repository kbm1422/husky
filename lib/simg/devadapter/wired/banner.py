#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from simg.devadapter.wired.base import Mhl3Interface, BaseAndroidDeviceAdapter


class BannerDeviceAdapter(BaseAndroidDeviceAdapter, Mhl3Interface):
    DEVPATH = "/sys/class/sii8630/8630"



