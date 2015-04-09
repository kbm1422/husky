#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from simg.devadapter.wired.base import Mhl3Interface, BaseAndroidDeviceAdapter


class TitanDeviceAdapter(BaseAndroidDeviceAdapter, Mhl3Interface):
    DEVPATH = "/sys/class/mhl/sii-8620"

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(thread)-5d [%(levelname)-8s] - %(message)s',
    )

    titan = TitanDeviceAdapter()
    titan.open()
    try:
        titan.recv_msc_message()
        titan.send_rap(0xFF)
        print titan.recv_msc_message()
    finally:
        titan.close()