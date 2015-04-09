#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


def singleton(cls):
    """
    See <Singleton> design pattern for detail: http://www.oodesign.com/singleton-pattern.html
    Python <Singleton> reference: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    Recommend use Singleton as a metaclass

    Usage:
        @singleton
        class MyClass(object):
            pass
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


class Singleton(type):
    """
    Usage:
        class MyClass(object):
            __metaclass__ = Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]