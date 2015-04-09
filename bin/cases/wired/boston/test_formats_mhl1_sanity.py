#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from simg.test.framework import LinkedTestSuite, TestSuite
from cases.common.sample_test_formats_mhl1 import Mhl1FormatsTestCase
from .test_drv_general import InputSelectTestCase


__test_suite__ = {
    "name": "Boston Formats MHL1 Sanity Test Suite",
    "type": LinkedTestSuite,
    "subs": [
        InputSelectTestCase.test_Sii9777InputSelect,
        {
            "type": TestSuite,
            "subs": [
                Mhl1FormatsTestCase,
            ]
        }
    ]
}