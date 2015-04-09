#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from simg.test.framework import TestCase, TestContextManager, parametrize
from simg.devadapter.wired.rogue import RogueDrvAdapter


@parametrize("device", type=RogueDrvAdapter, fetch=parametrize.FetchType.LAZY)
class BaseSiiDrvAdaptTestCase(TestCase):
    pass
