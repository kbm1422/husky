#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

import os
import re
import time
from datetime import datetime
from simg import fs
from simg.test.framework import TestContextManager, parametrize

from base import BaseJaxTestCase


class VendorMessageTestCase(BaseJaxTestCase):
    def __init__(self):
        super(VendorMessageTestCase, self).__init__()

    def setUp(self):
        resource = TestContextManager.current_context().resource
        self.txunit, self.rxunit = resource.acquire_pair()
        self.tx_gen3_1 = self.txunit.device.gen3_1
        self.tx_gen3_2 = self.txunit.device.gen3_2
        self.rx_gen3_1 = self.rxunit.device.gen3_1
        self.rx_gen3_2 = self.rxunit.device.gen3_2
        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)
        self.capture_image_name = os.path.join(self.capture_image_dir, self.name + ".jpg")
        self.make_connected(self.txunit.device, self.rxunit.device)

    def tearDown(self):
        self.rxunit.webcam.capture_image(self.capture_image_name)

    def test_vendor_msg_filter_get_set(self):
        tg1_set_ret = self.tx_gen3_1.sendcmd("vendor_msg_set_filter 11:11:11")
        rg1_set_ret = self.rx_gen3_1.sendcmd("vendor_msg_set_filter 22:22:22")

        self.assertEqual(tg1_set_ret, "OK",
                         "The vendor message set filter on TX GEN3 MAIN should be applied successfully")
        self.assertEqual(rg1_set_ret, "OK",
                         "The vendor message set filter on RX GEN3 MAIN should be applied successfully")

        tg1_get_ret = self.tx_gen3_1.sendcmd("vendor_msg_get_filter")
        rg1_get_ret = self.rx_gen3_1.sendcmd("vendor_msg_get_filter")

        self.assertEqual(tg1_get_ret, "11:11:11",
                         "The vendor message set filter on TX GEN3 MAIN should be set up successfully")
        self.assertEqual(rg1_get_ret, "22:22:22",
                         "The vendor message set filter on RX GEN3 MAIN should be set up successfully")

    def __send_vendor_msg(self):
        rx_gen3_1_filter = self.rx_gen3_1.sendcmd("vendor_msg_get_filter")
        send_msg_ret = self.tx_gen3_1.sendcmd(
            "vendor_msg_send " + rx_gen3_1_filter + " " + self.rx_gen3_1.setMacAddress + " 2 bb:bb")

    def test_vendor_msg_send(self):
        self.__send_vendor_msg()
        self.assertEqual(send_msg_ret, "OK", "The message should be sent from TX to RX successfully")

    def test_vendor_msg_get(self):
        self.__send_vendor_msg()
        rx_vendor_msg_ret = self.rx_gen3_1.sendcmd("vendor_msg_recv")
        self.assertEqual(rx_vendor_msg_ret, "bb:bb", "The received RX vendor message should be same as sent from TX")

    def test_vendor_msg_broadcast(self):
        tx1_set_filter = self.tx_gen3_1.sendcmd("vendor_msg_set_filter FF:FF:FF")
        tx2_set_filter = self.tx_gen3_2.sendcmd("vendor_msg_set_filter 11:11:11")
        tx1_set_filter = self.rx_gen3_1.sendcmd("vendor_msg_set_filter 22:22:22")

        assert tx1_set_filter == "OK", "TX MAIN filter is not setup successfully"
        assert tx2_set_filter == "OK", "TX SUB filter is not setup successfully"
        assert rx1_set_filter == "OK", "RX MAIN filter is not setup successfully"

        while True:
            tx1_msg_receive = None
            rx1_send_cmd = self.rx_gen3_1.sendcmd("vendor_msg_send 22:22:22 FF:FF:FF:FF:FF:FF 2 bb:bb")
            assert rx1_send_cmd == "OK", "The RX1 send command is not applied successfully"
            tx1_msg_receive = self.tx_gen3_1.sendcmd("vendor_msg_recv")
            i = 0
            if tx1_msg_receive == "bb:bb":
                self._pass("The vendor message is received by TX MAIN successfully")
                break
            elif i == 10:
                self._fail("The vendor message is received by TX MAIN successfully")
                break
            i += 1

        while True:
            tx1_msg_receive = None
            tx2_send_cmd = self.tx_gen3_2.sendcmd("vendor_msg_send 22:22:22 FF:FF:FF:FF:FF:FF 2 bb:bb")
            assert tx2_send_cmd == "OK", "The TX2 send command is not applied successfully"
            tx1_msg_receive = self.tx_gen3_1.sendcmd("vendor_msg_recv")
            self.assertEqual(tx1_msg_receive2, "bb:bb", "The vendor message is received by TX main successfully")
            i = 0
            if tx1_msg_receive == "bb:bb":
                self._pass("The vendor message is received by TX MAIN successfully")
                break
            elif i == 10:
                self._fail("The vendor message is received by TX MAIN successfully")
                break
            i += 1