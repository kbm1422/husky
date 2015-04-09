#!/usr/bin/python
# -*- coding: utf-8 -*-


import logging
logger = logging.getLogger(__name__)


from simg.test.framework import TestCase


class BaseTestCase(TestCase):
    def runTest(self):
        raise NotImplementedError

    def _test_set_product_id(self, unit, product_id):
        logger.debug("_test_set_product_id: unit=%s, product_id=%s", unit, product_id)
        unit.device.sendcmd("custparamset 3 %s" % product_id)
        unit.device.nvramreset()
        pid = unit.device.getProductId()
        if product_id == 9977:
            self.assertEquals("reserved id", pid, "unit '%s' set product id to '%s' should be successfully" % (unit, product_id))
        else:
            pid = int(pid, 16)
            self.assertEquals(pid, product_id, "unit '%s' set product id to '%s' should be successfully" % (unit, product_id))

    # def _test_connecttime(self, logfile, fromtime):
    #     logparser = SWAM3LogParser(logfile)
    #     connectedTimestamps = logparser.getConnectTimestamps(fromtime, timeout=30)
    #     self.assertTrue(connectedTimestamps, "After reset, should find 'baseband video UNMUTE' within 30s")
    #
    #     lastConnectedTimestamp = connectedTimestamps[-1]
    #     disconnectTimestamps = logparser.getDisconnectTimestamps(lastConnectedTimestamp, 5)
    #     self.assertFalse(disconnectTimestamps, "Should have no 'Disconnect' after the last 'baseband video UNMUTE'")
    #
    #     connectTimeCost = connectedTimestamps[-1] - fromtime
    #     self.add_concern("connect cost time", connectTimeCost)
    #     self.assertLessEqual(connectTimeCost, 20, "Connect time cost should less equal than 20s", iswarning=True)
