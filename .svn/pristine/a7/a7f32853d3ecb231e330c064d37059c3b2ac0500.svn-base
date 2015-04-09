#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import time

from simg.test.framework import TestContextManager
from base import BaseTestCase

"""
soft_pairing_info
0: idle mode        blinking once per 3.0sec
1: pairing mode     blinking once per 0.6sec
2: paired mode      LED on
3: idle pair mode   blinking once per 1.0sec

set_conn_stats 4
short press

set_conn_stats 5
long press
"""


def tearDownModule():
    logger.debug("do teardown for 'softpairing' module.")
    resource = TestContextManager().getCurrentContext().resource
    for unit in resource.getAcquiredUnits():
        unit.device.sendcmd("custparamset 3 1")
        unit.device.nvramreset()


class SoftPairingBaseTestCase(BaseTestCase):
    reserved_id = 9977

    class Mode(object):
        IDLE = 0
        PAIRING = 1
        PAIRED = 2
        IDLEPAIR = 3

    mode_mapping = {
        "0": "idle mode",
        "1": "pairing mode",
        "2": "paired mode",
        "3": "idle pair mode",
    }

    def runTest(self):
        raise NotImplementedError

    def make_reserved(self, unit):
        logger.debug("make unit '%s' reserved", unit)
        resp = unit.device.sendcmd("custparamget 3")
        if "reserved id" not in resp:
            self._test_set_product_id(unit, self.reserved_id)

    def make_no_reserved(self, unit):
        logger.debug("make unit '%s' no reserved", unit)
        resp = unit.device.sendcmd("custparamget 3")
        if "reserved id" in resp:
            self._test_set_product_id(unit, 1)

    def make_idle(self, unit):
        logger.debug("make unit '%s' idle", unit)
        mode = unit.device.getSoftPairingStatus()
        if mode != self.Mode.IDLE:
            unit.device.nvramreset()

    def make_pairing(self, unit):
        logger.debug("make unit '%s' pairing", unit)
        mode = unit.device.getSoftPairingStatus()
        if mode != self.Mode.PAIRING:
            unit.device.sendcmd("set_conn_stats 4")

    def _test_in_expected_mode(self, unit, expected_mode, msg=None):
        logger.debug("_test_in_expected_mode: unit=%s, expected_mode=%s, msg=%s", unit, expected_mode, msg)
        s_expected_mode = self.mode_mapping[str(expected_mode)]
        mode = unit.device.getSoftPairingStatus()
        msg = msg or "%s should in %s" % (unit, s_expected_mode)
        self.assertEquals(mode, expected_mode, msg)

    def _test_pairing_timeout(self, unit, msg=None):
        logger.debug("_test_pairing_timeout: unit=%s, msg=%s", unit, msg)
        unit.device.sendcmd("set_conn_stats 4")
        msg = msg or "%s should do pairing timeout" % unit
        self._test_in_expected_mode(unit, 1, msg)
        logger.debug("waiting 60s to make sure pairing timeout")
        time.sleep(60)
        self._test_in_expected_mode(unit, 0, msg)


class ReservedIDSettingTestCase(SoftPairingBaseTestCase):
    def setUp(self):
        self.resource = TestContextManager().getCurrentContext().resource
        self.txunit = self.resource.apply_txunit(0)
        self.rxunit = self.resource.apply_rxunit(0)
        self.resource.allocate_units()
        self.make_no_reserved(self.txunit)
        self.make_no_reserved(self.rxunit)

    def test_reserved_id_after_setting(self):
        self._test_set_product_id(self.txunit, self.reserved_id)
        self._test_set_product_id(self.rxunit, self.reserved_id)
        self._test_in_expected_mode(self.txunit, 0, "Tsp should in idle mode")
        self._test_in_expected_mode(self.rxunit, 0, "Rsp should in idle mode")


class PairingTimeoutTestCase(SoftPairingBaseTestCase):
    def setUp(self):
        self.resource = TestContextManager().getCurrentContext().resource
        self.txunit, self.rxunit = self.resource.acquire_pair(0, 0)
        self.make_reserved(self.txunit)
        self.make_reserved(self.rxunit)
        self.make_idle(self.txunit)
        self.make_idle(self.rxunit)

    def test_tsp_pairing_timeout(self):
        self._test_pairing_timeout(self.txunit, "Tsp should do pairing timeout")

    def test_rsp_pairing_timeout(self):
        self._test_pairing_timeout(self.rxunit, "Rsp should do pairing timeout")


class RspTspPairingTestCase(SoftPairingBaseTestCase):
    def setUp(self):
        self.resource = TestContextManager().getCurrentContext().resource
        self.txunit, self.rxunit = self.resource.acquire_pair(0, 0)
        self.make_reserved(self.txunit)
        self.make_reserved(self.rxunit)
        self.make_idle(self.txunit)
        self.make_idle(self.rxunit)

    def test_rsp_pairing_tsp(self):
        self.make_pairing(self.txunit)
        self._test_in_expected_mode(self.txunit, 1)
        self.make_pairing(self.rxunit)
        self._test_in_expected_mode(self.txunit, 2)
        self._test_in_expected_mode(self.rxunit, 2)
        #TODO: check connect

    def test_tsp_pairing_rsp(self):
        self.make_pairing(self.rxunit)
        self._test_in_expected_mode(self.rxunit, 1)
        self.make_pairing(self.txunit)
        self._test_in_expected_mode(self.txunit, 2)
        self._test_in_expected_mode(self.rxunit, 2)
        #TODO: check connect


class RspTxPairingTestCase(SoftPairingBaseTestCase):
    def setUp(self):
        self.resource = TestContextManager().getCurrentContext().resource
        self.txunit = self.resource.txunits[0]
        self.rxunit = self.resource.rxunits[0]
        self.make_no_reserved(self.txunit)
        self.make_reserved(self.rxunit)

    def test_rsp_pairing_tx(self):
        pass


class TspRxPairingTestCase(BaseTestCase):
    def test_tsp_pairing_rx(self):
        pass

