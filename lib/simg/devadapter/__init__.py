#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from abc import ABCMeta, abstractmethod


class DeviceAdapterFactory(object):
    @classmethod
    def new_device_adapter(cls, **kwargs):
        device_type = kwargs.pop("type").lower()
        if device_type == "jax":
            from .wireless.jax import JaxDeviceAdapter
            return JaxDeviceAdapter(**kwargs)
        elif device_type == "gen3":
            from .wireless.gen3 import Gen3DeviceAdapter
            return Gen3DeviceAdapter(**kwargs)
        elif device_type == "ba" or device_type == "b&a":
            from .wireless.ba import BADriverAdapter
            return BADriverAdapter(**kwargs)
        elif device_type == "rogue":
            from .wired.rogue.adapter import RogueDeviceAdapterFactory
            return RogueDeviceAdapterFactory.new_rogue_device_adapter(**kwargs)
        elif device_type == "wolverine60":
            from .wired.wolverine60 import Wolverine60DeviceAdapter
            return Wolverine60DeviceAdapter(**kwargs)
        elif device_type == "boston":
            from .wired.boston.adapter import BostonDeviceAdapter
            return BostonDeviceAdapter(**kwargs)
        elif device_type == "titan":
            from .wired.titan import TitanDeviceAdapter
            return TitanDeviceAdapter(**kwargs)
        elif device_type == "strom":
            from .wired.strom import StromDeviceAdapter
            return StromDeviceAdapter(**kwargs)
        else:
            raise NotImplementedError


class BaseDeviceAdapter(object):
    __metaclass__ = ABCMeta

    def __init__(self, id=None, **kwargs):
        self.id = int(id, 16) if isinstance(id, str) else id
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass


class DeviceAdapterError(Exception):
    pass


class DeviceEndType(object):
    SOURCE = 1
    SINK = 2
    DONGLE = 3