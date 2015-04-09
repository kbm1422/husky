#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
from simg import fs
from simg.test.framework import TestContextManager
from base import BaseJaxTestCase


class WhitelistTestCase(BaseJaxTestCase):
    def setUp(self):
        resource = TestContextManager.current_context().resource
        self.txunit, self.rxunit = resource.acquire_pair()
        #self.txunit0 = resource.apply_txunit(0)
        #self.txunit1 = resource.apply_txunit(1)
        #self.rxunit0 = resource.apply_rxunit(0)
        # self.rxunit1 = resource.apply_rxunit(1)
        #resource.allocate_units()


        self.capture_image_dir = os.path.join(self.logdir, "images")
        self.capture_image_name = os.path.join(self.capture_image_dir, "%s_%s.jpg" % (self.name, self.cycleindex))
        self.make_connected(self.txunit.device, self.rxunit.device)
        fs.mkpath(self.capture_image_dir)

    def test_set_tx_whitelist(self):

        '''
        test steps:
        1. get TX main and sub mac_address
        2. get RX main and sub white list
        3. set white list as TX mac_address on RX
        4. both reset TX and RX
        5. CHECK POINT1 (after reset, TX should connect with RX)
        '''

        try:
            tx1addr = self.txunit.device.gen3_1.getMacAddress()
            tx2addr = self.txunit.device.gen3_2.getMacAddress()
            logging.debug('TX main Mac address is: ' + tx1addr)
            logging.debug('TX sub Mac address is: ' + tx2addr)
            self.rxunit.device.gen3_1.sendcmd('get_whitelist')
            self.rxunit.device.gen3_1.sendcmd('set_whitelist_entry 0 ' + tx1addr)
            self.rxunit.device.gen3_2.sendcmd('get_whitelist')
            self.rxunit.device.gen3_2.sendcmd('set_whitelist_entry 0 ' + tx2addr)
            self.txunit.device.reset()
            #self.txunit.device.nvramreset()
            self.rxunit.device.reset()
            self._test_connection(self.rxunit.device)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)

    def test_set_not_tx_whitelist(self):

        '''
        test steps:
        1. get RX main and sub white list
        2. set white list as non_TX mac_address on RX
        3. both reset TX and RX
        4. CHECK POINT1 (after reset, TX should not connect with RX)
        5. clear white list on RX
        6. both reset TX and RX
        7. CHECK POINT2 (after reset, TX should connect with RX)
        '''

        try:
            self.rxunit.device.gen3_1.sendcmd('get_whitelist')
            self.rxunit.device.gen3_2.sendcmd('get_whitelist')
            self.rxunit.device.gen3_1.sendcmd('set_whitelist_entry 0 ' + "aa:aa:aa:11:11:11")
            self.rxunit.device.gen3_2.sendcmd('set_whitelist_entry 0 ' + "11:11:11:aa:aa:aa")
            self.txunit.device.reset()
            self.rxunit.device.reset()
            self._test_noconnection(self.rxunit.device)
            self.rxunit.device.gen3_1.sendcmd('set_whitelist_entry 0 ' + "ff:ff:ff:ff:ff:ff")
            self.rxunit.device.gen3_2.sendcmd('set_whitelist_entry 0 ' + "ff:ff:ff:ff:ff:ff")
            self.txunit.device.reset()
            self.rxunit.device.reset()
            self._test_connection(self.rxunit.device)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)