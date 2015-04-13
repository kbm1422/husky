#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from simg.devadapter import DeviceEndType
from simg.devadapter.wired.base import BaseSerialDeviceAdapter, Mhl2Interface, MscMessage


class JubileeDeviceAdapter(BaseSerialDeviceAdapter, Mhl2Interface):
    def __init__(self, comport, **kwargs):
        super(JubileeDeviceAdapter, self).__init__(comport, 19200, **kwargs)

    @property
    def end_type(self):
        return DeviceEndType.SINK

    def send_msc_message(self, message):
        logger.debug("send msc message: %s", message)
        self.write_byte(0xC8, 0x13, 0x68)
        self.write_byte(0xC8, 0x14, message.type)
        self.write_byte(0xC8, 0x15, message.code)
        self.write_byte(0xC8, 0x12, 0x02)

    def recv_msc_message(self):
        type = self.read_byte(0xC8, 0x18)
        code = self.read_byte(0xC8, 0x19)
        if code < 0:
            code += 256
        message = MscMessage(type, code)
        logger.debug("recv msc message: %s", message)
        return message

    def get_local_devcap(self):
        devcap = []
        devcap.extend(self.read_block(0xC8, 0x80, 8))
        devcap.extend(self.read_block(0xC8, 0x88, 8))
        logger.debug("get %s local devcap: %s", self, devcap)
        return devcap

    def get_remote_devcap(self):
        raise NotImplementedError
