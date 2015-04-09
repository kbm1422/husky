#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from simg.test.framework import parametrize
from test_drv_rx_mhl_common import *

# FIXME: will cause conflict when mul-threads TestRunner
parametrize("expect_cd_sense", default="SII9777_CD_SENSE__MHL_CABLE")(RxCdSenseQueryTestCase)
parametrize("expect_mhl_version", default="SII9777_MHL_VERSION__MHL12")(MHLVersionQueryTestCase)
parametrize("expect_cbus_mode", default="SII9777_CBUS_MODE__OCBUS")(CbusModeQueryTestCase)


__test_suite__ = {
    "name": "Boston Driver RX MHL2 Test Suite"
}