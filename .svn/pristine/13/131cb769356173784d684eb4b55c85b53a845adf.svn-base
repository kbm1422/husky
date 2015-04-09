#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
B&A wihd scan test suite
Including test cases: scan_from_idle, scan_from_scan, scan_stop, intervscan_from_idle, intervscan_from_scan
Note: before test, make sure B&A has connected with Linux PC through USB cable, driver has been installed and wihd
firmware has been loaded
"""

import logging

logger = logging.getLogger(__name__)

from simg.test.framework import TestContextManager

from base import BaseTestCase
import time
import threading


class ScanTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager().getCurrentContext()
        self.txunit, self.rxunit = context.resource.acquire_pair()

    def test_scan_from_idle(self):
        # Test scan from idle state repeatedly
        # Steps:
        # 1. Disconnect to make sure B&A in idle, try max 3 times, if not in idle, exit test
        # 2. Start scan under idle mode
        # 3. Check point1 -- check scan node value is correct, check driver state is correct, and uevent is correct
        # 4. Check point2 -- check unit scan duration
        #5. After all scan cycle complete, join the wvan and connect
        #6. Check point3 -- check connect successfully
        #7. Get result:
        #   scan failed, result failed
        #   join failed or connect failed after all scan cycle, print comments in test result
        #   if fail or warning, copy dmesg tail and syslog

        # Make sure the precondition is in "IDLE" state
        self.try_disassociated(self.txunit)

        # Start to scan
        self.make_scan(0, 0, 10)


    def test_scan_from_scan(self):
        # Test scan from scan state repeatedly
        # Steps:
        # 1. Disconnect to make sure B&A in idle, try max 3 times, if not in idle, exit test
        # 2. Start scan under idle mode
        # 3. Check point1 -- check scan node value
        #4. Check point2 -- check driver state
        #5. Before scan complete, start new scan
        #6. After waiting scan duration
        #7. Check point3 -- check wvan_scan_start event, if no or more than 2, report scan failure
        #8. Check point4 -- check wvan_scan_complete event, if no or less than 2, report scan failure
        #9. Check point5 -- check wvan_scan_stop event, if no report scan failure
        #10. Check point6 -- check wvan_scan_complete data, if no data in the end, report scan failure
        #11. Get result:
        #   scan failed, result failed
        #   join failed or connect failed after all scan cycle, print comments in test result
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunit)
        self.make_concurrent_scan(self.txunit)

    def test_scan_stop(self):
        # Test scan stop during scanning
        # Steps:
        # 1. Disconnect to make sure B&A in idle, try max 3 times, if not in idle, exit test
        # 2. Start scan under idle mode with duration
        #3. Before scan complete, stop the scan
        #4. Check point1 -- check the active scan process can complete, including node value, driver state and uevent
        #5. Check point2 -- check the scan can stop, including node value, driver state and uevent
        #6. Wait 1/3 duration time
        #7. Check point3 -- check no scan process active
        #8. After run all cycle scan stop test, join and connect wvan
        #9. Check point4 -- check it can join and connect successfully, including node value, driver state and uevent
        #10. Get result:
        #   scan failed, result failed
        #   stop failed, result failed
        #   join failed or connect failed after all scan cycle, print comments in test result
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunit)
        self.make_scan(10, 1, 10)
        self.make_stop_scan(self.txunit)

    def test_intervscan_from_idle(self):
        # Test interval scan from idle state repeatedly
        # Steps:
        # 1. Disconnect to make sure B&A in idle, try max 3 times, if not in idle, exit test
        #2. Start interval scan under idle mode (duration = 30, interval = 10)
        #3. Check point1 -- check scan node value is correct, check driver state is correct, and uevent is correct for every unit scan
        #4. Check point2 -- check scan duration for every unit scan
        #5. After all scan cycle complete, join the wvan and connect
        #6. Check point3 -- check connect successfully
        #7. Get result:
        #   scan failed, result failed
        #   join failed or connect failed after all scan cycle, print comments in test result
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunit)
        self.make_interval_scan()

    def test_intervscan_from_scan(self):
        # Test interval scan from scan state repeatedly
        # Steps:
        #1. Disconnect to make sure B&A in idle, try max 3 times, if not in idle, exit test
        #2. Start interval scan under idle mode
        #3. Check point1 -- check scan node value
        #4. Check point2 -- check driver state
        #5. Before interval scan complete, start new interval scan
        #6. After waiting scan duration
        #7. Check point3 -- check wvan_scan_start event, if no or more than 2, report scan failure
        #8. Check point4 -- check wvan_scan_complete event, if no or less than 3, report scan failure
        #9. Check point5 -- check wvan_scan_stop event, if no report scan failure
        #10. Check point6 -- check wvan_scan_complete data, if no data in the end, report scan failure
        #11. Get result:
        #   scan failed, result failed
        #   join failed or connect failed after all scan cycle, print comments in test result
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunit)
        t1 = threading.Thread(target=self.make_interval_scan(30, 10))
        t1.start()
        time.sleep(3)
        t2 = threading.Thread(target=self.make_interval_scan(30, 10))
        t2.start()
        t1.join()
        t2.join()