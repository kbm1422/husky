#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
#B&A wihd connect test suite
#Including test case: connect directly, connect through mac address, connected to disconnect, connected to disassociated
#Note: before test, make sure B&A has connected with Linux PC through USB cable, driver has been installed and wihd
firmware has been loaded
"""

import logging

logger = logging.getLogger(__name__)

import time

from simg.test.framework import TestContextManager

from base import BaseTestCase


class ConnectTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager().getCurrentContext()
        self.txunits = context.resource.txunits
        self.rxunits = context.resource.rxunits

    def test_connect_disassoc(self):
        # Test scan->join->connect->disassociate repeatedly
        # Steps:
        # 1. Make sure B&A in disassociate state before test
        # 2. Set mac address, set scan duration, start scan, max to 3 times, check point1 -- check scan successful or not
        # 3. Join wvan, max to 3 times, check point2 -- check join successful or not
        # 4. Connect by echo 1 > connect, max to 3 times, check point3 -- check connect successful or not, check connect value, driver state and uevent
        # 5. Disassociate, check point4 -- check disassociate successful or not, check driver state and uevent
        #6. Get result:
        #   set mac failed or scan failed or join failed, result warning
        #   scan more time, or join more time, or connect more time, result warning
        #   connect failed or disassociate failed, result failed
        #   connect passed and disassociate passed, result passed
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunits[0])
        self.make_connected(self.txunits[0].self.rxunits[0], 10)
        self.make_disassociated(self.txunits[0])

    def test_connect_disconnect(self):
        # Test scan->join->connect->disconnect repeatedly
        # Steps:
        # 1. Make sure B&A in disassociate state before test
        # 2. Set mac address, set scan duration, start scan, max to 3 times, check point1 -- check scan successful or not
        # 3. Join wvan, max to 3 times, check point2 -- check join successful or not
        # 4. Connect by echo 1 > connect, max to 3 times, check point3 -- check connect successful or not, check connect value, driver state and uevent
        #5. Disconnect, check point4 -- check disconnect and disassociate successful or not, check driver state and uevent
        #6. Get result:
        #   set mac failed or scan failed or join failed, result warning
        #   scan more time, or join more time, or connect more time, result warning
        #   connect failed or disconnect failed, result failed
        #   connect passed and disconnect passed, result passed
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunits[0])
        self.make_connected(self.txunits[0].self.rxunits[0], 10)
        self.make_disconnected(self.txunits[0], self.rxunits[0])

    def test_connect_mac_disassoc(self):
        # Test scan->join->connect_mac->disassociate repeatedly
        # Steps:
        # 1. Make sure B&A in disassociate state before test
        # 2. Set mac address, set scan duration, start scan, max to 3 times, check point1 -- check scan successful or not
        # 3. Join wvan, max to 3 times, check point2 -- check join successful or not
        #4. Connect by echo mac_addr > connect, max to 3 times, check point3 -- check connect successful or not, check connect value, driver state and uevent
        #5. Disassociate, check point4 -- check disassociate successful or not, check driver state and uevent
        #6. Get result:
        #   set mac failed or scan failed or join failed, result warning
        #   scan more time, or join more time, or connect more time, result warning
        #   connect failed or disassociate failed, result failed
        #   connect passed and disassociate passed, result passed
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunits[0])
        self.make_connected(self.txunits[0].self.rxunits[0], 10, mode=2)
        self.make_disassociated(self.txunits[0])

    def test_connect_mac_disconnect_disassoc(self):
        # Test scan->join->connect->disconnect->disassoc repeatedly
        # Steps:
        # 1. Make sure B&A in disassociate state before test
        # 2. Set mac address, set scan duration, start scan, max to 3 times, check point1 -- check scan successful or not
        #3. Join wvan, max to 3 times, check point2 -- check join successful or not
        #4. Connect by echo 1 > connect, max to 3 times, check point3 -- check connect successful or not, check connect value, driver state and uevent
        #5. Disconnect, check point4 -- check disconnect and disassociate successful or not for A0, check disconnect successful or not for A1, check driver state and uevent
        #6. Get result:
        #   set mac failed or scan failed or join failed, result warning
        #   scan more time, or join more time, or connect more time, result warning
        #   connect failed, disconnect failed or disassoc failed, result failed
        #   connect passed, disconnect passed and disassoc passed, result passed
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunits[0])
        self.make_connected(self.txunits[0].self.rxunits[0], 10, mode=2)
        self.make_disconnected(self.txunits[0], self.rxunits[0])
        self.make_disassociated(self.txunits[0])

    def test_connect_mac_disconnect_A1(self):
        # Test scan->join->connect->disconnect repeatedly (this case just for A1, A0 cannot support)
        # Steps:
        # 1. Check B&A version, if chip version is A0 exit test, otherwise continue
        #2. Make sure it is in associated state before test, if not exit test
        #3. Connect by echo mac_addr > connect, max to 3 times, check point1 -- check connect successful or not, check connect value, driver state and uevent
        #4. Disconnect, check point2 -- check disconnect successful or not for A1, check driver state and uevent
        #5. Get result:
        #   connect failed, disconnect failed, result failed
        #   connect passed, disconnect passed, result passed
        #   if fail or warning, copy dmesg tail and syslog
        pass

    def test_connect_disconnect_under_idle(self):
        # Test connect under idle state->scan->join->recover connect->disconnect->disconnect under idle state repeatedly
        # Steps:
        #1. Make sure B&A in idle state before test
        #2. Scan wvan to get remote device mac address
        #3. Connect under idle state -- check point1, check there is no error respond
        #4. Scan->join and recover connect under associated state -- check point2, check scan/join/connect can success, check connect value, driver state and uevent
        #5. Disconnect under av_enabled state -- check point3, check disconnect can success, check driver state and uevent
        #6. Disconnect under idle state -- check point4, check there is no error respond
        #7. Get result:
        #   set mac failed or scan failed or join failed, result warning
        #   scan more time, or join more time, or connect more time, result warning
        #   connect failed or disconnect failed, result failed
        #   connect passed and disconnect passed, result passed
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunits[0])
        self.make_connected(self.txunits[0].self.rxunits[0], 10)
        self.make_disconnected(self.txunits[0], self.rxunits[0])
        self.make_disassociated(self.txunits[0])

    def test_connect_after_sink_sleep(self):
        self.try_disassociated(self.txunits[0])
        self.make_connected(self.txunits[0].self.rxunits[0], 10)
        self.make_disassociated(self.txunits[0])
        # After tx is in disconnected for 120 seconds, the rx will be in sleep state, per discuss with Yale
        time.sleep(120)
        self.make_connected(self.txunits[0].self.rxunits[0], 10)
        self.make_disconnected(self.txunits[0], self.rxunits[0])

    def test_switch_wvan(self):
        # Test connect under idle state->scan->join->connect one sink ->disconnect-> scan again-> join another sink-> connect another sink
        #Steps:
        #1. Make sure B&A in disassociate state before test
        #2. Make sure B&A in wihd state before test
        #3. set mac address --> check point 1 ,mac address set successfully
        #4. Scan->join check point2, scan/join/connect one sink  can success, check scan/join /connect value, driver state and uevent
        #5. Disassociate under av_enabled state -- check point3, check disconnect can success, check driver state and uevent
        #6. Scan->joi again ,check point4, scan/join/connect another sink  can success, check scan/join /connect value, driver state and uevent
        #7. Get result:
        #   set mac failed or scan failed or join failed or connect failed or disassociate failed ,result failed
        #   scan more time, or join more time, or connect more time, result warning
        #   if fail or warning, copy dmesg tail and syslog
        #   res[mac,scan,scan wvan,join,associate pass,connect, connect value,disassociate,scan,scan wvan,join,associate
        #   pass,connect,connect value,disassociate,]
        self.try_disassociated(self.txunits[0])
        self.make_connected(self.txunits[0].self.rxunits[0], 10)
        self.make_disassociated(self.txunits[0])
        self.make_connected(self.txunits[0].self.rxunits[1], 10)
        self.make_disconnected(self.txunits[0], self.rxunits[0])
