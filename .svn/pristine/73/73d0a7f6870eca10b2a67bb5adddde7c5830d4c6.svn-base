#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import time
from simg.devadapter import DeviceEndType
from simg.devadapter.wired.base import BaseSerialDeviceAdapter, Mhl2Interface, MscMessage


class StromDeviceAdapter(BaseSerialDeviceAdapter, Mhl2Interface):
    def __init__(self, comport, **kwargs):
        super(StromDeviceAdapter, self).__init__(comport, 19200, **kwargs)

    @property
    def end_type(self):
        return DeviceEndType.SINK

    def send_msc_message(self, message):
        logger.debug("send msc message: %s", message)
        self.write_byte(0xC0, 0xB9, 0x68)
        self.write_byte(0xC0, 0xBA, message.type)
        self.write_byte(0xC0, 0xBB, message.code)
        self.write_byte(0xC0, 0XB8, 0x02)

    def recv_msc_message(self):
        type = self.read_byte(0xC0, 0xBF)
        code = self.read_byte(0xC0, 0xC0)
        if code < 0:
            code += 256
        message = MscMessage(type, code)
        logger.debug("recv msc message: %s", message)
        return message

    def get_local_devcap(self):
        devcap = []
        devcap.extend(self.read_block(0xC0, 0x00, 8))
        devcap.extend(self.read_block(0xC0, 0x08, 8))
        logger.debug("get %s local devcap: %s", self, devcap)
        return devcap

    def get_remote_devcap(self):
        devcap = []
        for i in range(16):
            self.write_byte(0xC0, 0xB9, i)
            self.write_byte(0xC0, 0xB8, 4)
            time.sleep(0.1)
            self.read_byte(0xC0, 0x92),
            byte = self.read_byte(0xC0, 0xBC)
            if byte < 0:
                byte &= 0xFF
            devcap.append(byte)
        return devcap


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )

    adpt = StromDeviceAdapter("COM36")
    adpt.open()
    try:
        print adpt.get_local_devcap()
    finally:
        adpt.close()