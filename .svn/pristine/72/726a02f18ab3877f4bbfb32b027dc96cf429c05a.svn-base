#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
B&A wihd join test suite
Including test cases: join_from_idle, join_from_periodscan
Note: before test, make sure B&A has connected with Linux PC through USB cable, driver has been installed and wihd
firmware has been loaded
"""

import logging

logger = logging.getLogger(__name__)

from simg.test.framework import TestContextManager

from base import BaseTestCase


class JoinTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager().getCurrentContext()
        self.txunits = context.resource.txunits
        self.rxunits = context.resource.rxunits

    def test_join_from_idle(self):
        #Test join from idle state repeatedly
        #Steps:
        #1. Disconnect to make sure B&A in idle, try max 3 times, if not in idle, exit test
        #2. Scan under idle mode to get wvan data
        #3. Join the wvan under idle mode
        #4. Check point1 -- check associate can successfully, join node value is correct, check driver state is correct,
        # and uevent is correct
        #5. Exit the wvan
        #6. Check point2 -- check disassociate can successfully, join node value is correct, check driver state is correct, and uevent is correct
        #7. Repeat step 3 to 5
        #8. After all join cycle complete, connect
        #9. Check point3 -- check connect successfully
        #10. Get result:
        #   join failed, result failed
        #   exit failed, result failed
        #   connect failed after all scan cycle, print comments in test result
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunits[0])
        self.make_associated(self.txunits[0], self.rxunits[0])
        self.try_disassociated(self.txunits[0])

    def test_join_from_peroidscan(self):
        #Test join from period scan state repeatedly
        #Steps:
        #1. Disconnect to make sure B&A in idle, try max 3 times, if not in idle, exit test
        #2. Scan under idle mode to get wvan data
        #3. Start period scan again
        #4. Join the wvan under scan state before scan complete
        #5. Check point1 -- check associate can successfully, join node value is correct, check driver state is correct, and uevent is correct
        #6. Exit the wvan
        #7. Check point2 -- check disassociate can successfully, join node value is correct, check driver state is correct, and uevent is correct
        #8. Repeat step 3 to 5
        #9. After all join cycle complete, connect
        #10. Check point3 -- check connect successfully
        #11. Get result:
        #   join failed, result failed
        #   exit failed, result failed
        #   connect failed after all scan cycle, print comments in test result
        #   if fail or warning, copy dmesg tail and syslog
        self.try_disassociated(self.txunits[0])
        self.make_associated_from_intervalscan(self.txunits[0], self.rxunits[0], 30, 10)
        self.try_disassociated(self.txunits[0])