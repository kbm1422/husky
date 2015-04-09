#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
logger = logging.getLogger(__name__)

import time
import urllib2
import base64
from abc import ABCMeta
from HTMLParser import HTMLParser

from simg.pattern import Singleton


class SwitchOutletError(Exception):
    pass


class PowerSwitchOutletFactory(object):
    __metaclass__ = Singleton

    @classmethod
    def new_psoutlet(cls, **kwargs):
        if kwargs:
            logger.debug("kwargs is not empty, create a PowerSwitchOutlet")
            return PSOutlet(**kwargs)
        else:
            logger.debug("kwargs is empty, create a NullPowerSwitchOutlet")
            return NullPSOutlet()


class BasePSOutlet(object):
    __metaclass__ = ABCMeta

    def turnon(self):
        pass

    def turnoff(self):
        pass

    def cycle(self, interval=0.0):
        pass

    def get_status(self):
        pass


class NullPSOutlet(BasePSOutlet):
    """
    See <Null Object> design pattern for detail: http://www.oodesign.com/null-object-pattern.html
    """


class PSOutlet(BasePSOutlet):
    def __init__(self, host, outlet, port=80, username="admin", password="sqa"):
        self._powswitch = PowerSwitchController(host, port, username, password)
        self._outlet = outlet

    def turnon(self):
        self._powswitch.turnon(self._outlet)
    
    def turnoff(self):
        self._powswitch.turnoff(self._outlet)

    def cycle(self, interval=1.0):
        self._powswitch.cycle(self._outlet, interval)

    def get_status(self):
        self._powswitch.get_status(self._outlet)


class PowerSwitchController(object):
    def __init__(self, host, port=80, username="admin", password="1234"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def _request(self, url):
        request = urllib2.Request("http://%s:%s%s" % (self.host, self.port, url))
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        try:
            result = urllib2.urlopen(request).read()
        except urllib2.URLError:
            logger.exception("")
            raise
        return result
    
    def turnoff(self, outlet):
        logger.info("request power switch outlet %s OFF", outlet)
        self._request('/outlet?%s=OFF' % outlet)
        if self.get_status(outlet) != "OFF":
            raise SwitchOutletError
    
    def turnon(self, outlet):
        logger.info("request power switch outlet %s ON", outlet)
        self._request('/outlet?%s=ON' % outlet)
        if self.get_status(outlet) != "ON":
            raise SwitchOutletError

    def cycle(self, outlet, interval=1.0):
        if self.get_status(outlet) != "OFF":
            self.turnoff(outlet)
            time.sleep(interval)
            self.turnon(outlet)

    def get_status(self, outlet):
        allstatus = self.get_all_status()
        return allstatus[int(outlet) - 1]

    def get_all_status(self):
        states = []
        resp = self._request("/index.htm")

        class Parser(HTMLParser):
            def handle_data(self, data):
                if data == "ON" or data == "OFF":
                    states.append(data)
        parser = Parser()
        try:
            parser.feed(resp)
        finally:
            parser.close()
        logger.debug("power switch all outlets status: %s", states)
        return states


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )
    null = NullPSOutlet()
    null.turnon()
