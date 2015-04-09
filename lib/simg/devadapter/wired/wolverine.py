#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from simg.devadapter import DeviceEndType
from base import BaseBlackBoxDeviceAdapter


class WolverineDeviceAdapter(BaseBlackBoxDeviceAdapter):
    def __init__(self, blackbox_number, blackbox_comport, **kwargs):
        super(WolverineDeviceAdapter, self).__init__(blackbox_number, blackbox_comport, 19200, **kwargs)

    @property
    def end_type(self):
        return DeviceEndType.SOURCE

    def send_msc_message(self, message):
        logger.debug("send msc message: %s", message)
        self.write_byte(0xC8, 0x13, 0x68)
        self.write_byte(0xC8, 0x14, message.type)
        self.write_byte(0xC8, 0x15, message.code)
        self.write_byte(0xC8, 0X12, 0x02)

    def recv_msc_message(self):
        raise NotImplementedError

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )

    adpt = WolverineDeviceAdapter(0, "COM15")
    adpt.open()
    try:
        v = adpt.read_byte(0xC8, 0x13)
        print hex(v)
    finally:
        adpt.close()
