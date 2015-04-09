#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import tempfile

from abc import ABCMeta
from collections import OrderedDict

from simg.test.framework import TestResource, TestContextManager
from simg.util.powerswitch import PSOutlet
from simg.util.avproducer import AVProducerFactory
from simg.util.webcam import WebCamFactory
from simg.devadapter import DeviceAdapterFactory
from simg.devadapter.wireless.jax import JaxDeviceAdapter
from simg.devadapter.wireless.ba import BADriverAdapter
from simg.devadapter.wireless.gen3 import Gen3DeviceAdapter


class TestBench(TestResource):
    def __init__(self, conf):
        self.conf = conf
        self.name = self.conf.get("name")
        self.__txunits = OrderedDict()
        self.__rxunits = OrderedDict()
        self.__all_units = OrderedDict()
        self.__all_acquired_units = OrderedDict()

    def getAllUnits(self):
        return self.__all_units.values()

    def getAcquiredUnits(self):
        return self.__all_acquired_units.values()

    def addTxUnitFromData(self, txdata):
        logger.debug("TestBench '%s' addTxUnitFromData: %s", self.name, txdata)
        txunit = TxUnit(txdata)
        if txdata.name in self.__txunits:
            raise KeyError("unit already exists")
        self.__txunits[txdata.name] = txunit
        self.__all_units[txdata.name] = txunit

    def addRxUnitFromData(self, rxdata):
        logger.debug("TestBench '%s' addRxUnitFromData: %s", self.name, rxdata)
        rxunit = RxUnit(rxdata)
        if rxdata.name in self.__rxunits:
            raise KeyError("unit already exists")
        self.__rxunits[rxdata.name] = rxunit
        self.__all_units[rxdata.name] = rxunit

    def apply_txunit(self, index=0):
        logger.info("Apply TxUnit with index: %s", index)
        txname = self.__txunits.keys()[index]
        txunit = self.__txunits.values()[index]
        self.__all_acquired_units[txname] = txunit
        return txunit

    def apply_rxunit(self, index=0):
        logger.info("Apply RxUnit with index: %s", index)
        rxname = self.__rxunits.keys()[index]
        rxunit = self.__rxunits.values()[index]
        self.__all_acquired_units[rxname] = rxunit
        return rxunit

    def apply_txunits(self, *indexs):
        if not indexs:
            raise ValueError
        return [self.apply_txunit(index) for index in indexs]

    def apply_rxunits(self, *indexs):
        if not indexs:
            raise ValueError
        return [self.apply_rxunit(index) for index in indexs]

    def apply_pair(self, txindex=None, rxindex=None):
        return self.apply_txunit(txindex), self.apply_rxunit(rxindex)

    def acquire_pair(self, txindex=0, rxindex=0):
        txunit = self.apply_txunit(txindex)
        rxunit = self.apply_rxunit(rxindex)
        self.allocate_units()
        return txunit, rxunit

    def acquire_units(self, txindexs, rxindexs):
        if not isinstance(txindexs, (list, tuple)):
            raise TypeError
        if not isinstance(rxindexs, (list, tuple)):
            raise TypeError

        txunits = self.apply_txunits(*txindexs)
        rxunits = self.apply_rxunits(*rxindexs)
        self.allocate_units()
        return txunits, rxunits

    def allocate_units(self):
        logger.info("Allocate all units according to application")
        for unit in self.__all_acquired_units.values():
            logger.info("enable unit %s", unit)
            unit.enable()

        for unit in set(self.__all_units.values()) - set(self.__all_acquired_units.values()):
            logger.info("disable unit %s", unit)
            unit.disable()
        logger.debug("current acquired units: %s", self.__all_acquired_units)

    def __call_actions_in_context(self, type):
        logger.info("Call actions in context with type: %s", type)
        actions = getattr(TestContextManager().getCurrentContext(), "actions", [])
        if type == UnitAction.Type.ON_RUNNER_START or type == UnitAction.Type.ON_RUNNER_STOP:
            units = self.__all_units
        elif type == UnitAction.Type.ON_CASE_START or type == UnitAction.Type.ON_CASE_STOP:
            units = self.__all_acquired_units
        else:
            raise ValueError

        for action in actions:
            new_action = action.copy()
            if int(new_action.pop("type")) == type:
                logger.debug("Call action: %s", action)
                unit = units[new_action.pop("unit")]
                func = getattr(unit, new_action.pop("method"))
                func(**new_action)

    def initinalize(self):
        for unitelement in list(self.conf):
            unitname = unitelement.get("name")
            develement = unitelement.find("Device")
            devkwargs = develement.attrib
            pwselement = unitelement.find("PSOutlet")
            pwskwargs = pwselement.attrib if pwselement is not None else {}
            if unitelement.tag == "TxUnit":
                avpelement = unitelement.find("AVProducer")
                avpkwargs = avpelement.attrib if avpelement is not None else {}
                txdata = UnitData(unitname, devkwargs, avpkwargs, pwskwargs)
                self.addTxUnitFromData(txdata)
            elif unitelement.tag == "RxUnit":
                avcelement = unitelement.find("AVConsumer")
                avckwargs = avcelement.attrib if avcelement is not None else {}
                camelement = unitelement.find("WebCam")
                camkwargs = camelement.attrib if camelement is not None else {}
                rxdata = UnitData(unitname, devkwargs, avckwargs, pwskwargs, camkwargs)
                self.addRxUnitFromData(rxdata)
            else:
                raise ValueError

    def finalize(self):
        pass

    def on_runner_start(self):
        self.initinalize()
        for unit in self.__all_units.values():
            unit.initialize()
        self.__call_actions_in_context(UnitAction.Type.ON_RUNNER_START)

    def on_case_start(self, test):
        # FIXME: __all_acquired_units are always empty before case setup
        self.__call_actions_in_context(UnitAction.Type.ON_CASE_START)
        for unit in self.__all_units.values():
            if isinstance(unit.device, (Gen3DeviceAdapter, JaxDeviceAdapter)):
                server_logname = os.path.join(test.logdir, "%s_%s_%s.log" % (test.name, test.cycleindex, unit.data.name))
                unit.device.set_ss_server_logname(server_logname)
                test.extlognames.append(server_logname)
                if isinstance(unit.device, JaxDeviceAdapter):
                    test.extlognames.append(unit.device.gen3_1.log_subject.logname)
                    test.extlognames.append(unit.device.gen3_2.log_subject.logname)
            elif isinstance(unit.device, BADriverAdapter):
                uevent_logname = os.path.join(test.logdir, "%s_uevent_%s.log" % (test.name, test.cycleindex))
                unit.device.uevent.logname = uevent_logname
                test.extlognames.append(uevent_logname)

    def on_case_stop(self, test):
        for unit in self.__all_units.values():
            if isinstance(unit.device, (Gen3DeviceAdapter, JaxDeviceAdapter)):
                unit.device.set_ss_server_logname(tempfile.mkstemp()[1] + ".log")
        self.__call_actions_in_context(UnitAction.Type.ON_CASE_STOP)

        # release all acquired units
        self.__all_acquired_units = OrderedDict()

    def on_runner_stop(self):
        try:
            self.__call_actions_in_context(UnitAction.Type.ON_RUNNER_STOP)
        finally:
            for unit in self.__all_units.values():
                unit.finalize()
        self.finalize()


class BaseUnit(object):
    __metaclass__ = ABCMeta

    def __init__(self, data):
        if not isinstance(data, UnitData):
            raise TypeError
        self.data = data
        self.device = None
        self.psoutlet = None
        self.is_available = None

    def initialize(self):


        if self.data.pwskwargs:
            self.psoutlet = PSOutlet(**self.data.pwskwargs)
            self.psoutlet.turnon()
        self.data.devkwargs["name"] = self.data.name
        self.device = DeviceAdapterFactory.new_device_adapter(**self.data.devkwargs)
        self.device.open()
        self.is_available = True

    def finalize(self):
        if self.device is not None:
            self.device.close()
            self.device = None
        self.is_available = False

    def enable(self):
        if not self.is_available:
            self.initialize()

    def disable(self):
        if self.is_available:
            self.finalize()

    def upgrade(self, image):
        logger.info("Upgrade %s firmware to: %s", self, image)


class TxUnit(BaseUnit):
    def __init__(self, txdata):
        BaseUnit.__init__(self, txdata)
        self.avproducer = None

    def __repr__(self):
        return "<TxUnit: %s>" % self.data.name

    def __str__(self):
        return self.__repr__()

    def initialize(self):
        BaseUnit.initialize(self)
        self.avproducer = AVProducerFactory.new_avproducer(**self.data.avxkwargs)

    def finalize(self):
        BaseUnit.finalize(self)
        if self.avproducer and hasattr(self.avproducer, "close"):
            self.avproducer.close()
            self.avproducer = None


class RxUnit(BaseUnit):
    def __init__(self, rxdata):
        BaseUnit.__init__(self, rxdata)
        self.webcam = None

    def __repr__(self):
        return "<RxUnit: %s>" % self.data.name

    def __str__(self):
        return self.__repr__()

    def initialize(self):
        BaseUnit.initialize(self)
        self.webcam = WebCamFactory.new_webcam(**self.data.camkwargs)


class UnitAction(object):
    class Type(object):
        ON_RUNNER_START = 1
        ON_CASE_START = 2
        ON_CASE_STOP = 3
        ON_RUNNER_STOP = 4


class UnitData(object):
    def __init__(self, name, devkwargs, avxkwargs, pwskwargs=None, camkwargs=None, build=None):
        if not isinstance(devkwargs, dict):
            raise TypeError
        if not isinstance(avxkwargs, dict):
            raise TypeError
        if pwskwargs and not isinstance(pwskwargs, dict):
            raise TypeError
        if camkwargs and not isinstance(camkwargs, dict):
            raise TypeError
        self.name = name
        self.devkwargs = devkwargs
        self.avxkwargs = avxkwargs
        self.pwskwargs = pwskwargs
        self.camkwargs = camkwargs
        self.build = build

    def __repr__(self):
        return "<UnitData: name=%s, devkwargs=%s, avpkwargs=%s, pwskwargs=%s, camkwargs=%s, build=%s>" % (
            self.name, self.devkwargs, self.avxkwargs, self.pwskwargs, self.camkwargs, self.build)

    def __str__(self):
        return self.__repr__()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )

