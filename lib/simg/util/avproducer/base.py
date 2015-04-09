#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


class BaseAVProducer(object):
    def __init__(self, name=None):
        self.name = name

    def close(self):
        pass