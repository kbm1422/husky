#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from simg.test.framework import TestResource
from simg.util.sl8800 import SL8800
from simg.util.uts800 import UTS800
from simg.util.avproducer import AVProducerFactory
from simg.util.avconsumer import AVConsumerFactory
from simg.util.webcam import WebCamFactory
from simg.util.powerswitch import PSOutlet
from simg.devadapter import DeviceAdapterFactory


class Devices(object):
    def __init__(self):
        self.transmitter = None
        self.repeater = None
        self.receiver = None


class TestBench(TestResource):
    def __init__(self, conf):
        self.conf = conf
        self.name = self.conf.get("name")

        self.device = None
        self.devs = []
        self.devices = Devices()
        self.avproducer = None
        self.avconsumer = None
        self.avproducers = []
        self.avconsumers = []
        self.sl8800 = None
        self.webcam = None
        self.uts800 = None

    def initialize(self):
        for device_element in self.conf.findall("Device"):
            dev = DeviceAdapterFactory.new_device_adapter(**device_element.attrib)
            dev_psoutlet_element = device_element.find("PSOutlet", None)
            if dev_psoutlet_element is not None:
                dev.psoutlet = PSOutlet(**dev_psoutlet_element.attrib)
            self.devs.append(dev)

        if self.devs:
            self.device = self.devs[0]

        devices_element = self.conf.find("Devices")
        if devices_element is not None:
            transmitter_element = devices_element.find("Transmitter")
            if transmitter_element is not None:
                self.devices.transmitter = DeviceAdapterFactory.new_device_adapter(**transmitter_element.attrib)
                transmitter_psoutlet_element = transmitter_element.find("PSOutlet")
                if transmitter_psoutlet_element is not None:
                    self.devices.transmitter.psoutlet = PSOutlet(**transmitter_psoutlet_element.attrib)

            repeater_element = devices_element.find("Repeater")
            if repeater_element is not None:
                self.devices.repeater = DeviceAdapterFactory.new_device_adapter(**repeater_element.attrib)
                repeater_psoutlet_element = repeater_element.find("PSOutlet")
                if repeater_psoutlet_element is not None:
                    self.devices.repeater.psoutlet = PSOutlet(**repeater_psoutlet_element.attrib)

            receiver_element = devices_element.find("Receiver")
            if receiver_element is not None:
                self.devices.receiver = DeviceAdapterFactory.new_device_adapter(**receiver_element.attrib)
                receiver_psoutlet_element = receiver_element.find("PSOutlet")
                if receiver_psoutlet_element is not None:
                    self.devices.receiver.psoutlet = PSOutlet(**receiver_psoutlet_element.attrib)
        else:
            raise ValueError("Devices element can't be None")

        avp_elements = self.conf.findall("AVProducer", None)
        for avp_element in avp_elements:
            avproducer = AVProducerFactory.new_avproducer(**avp_element.attrib)
            self.avproducers.append(avproducer)
            avp_psoutlet_element = avp_element.find("PSOutlet", None)
            if avp_psoutlet_element is not None:
                avproducer.psoutlet = PSOutlet(**avp_psoutlet_element.attrib)

        if self.avproducers:
            self.avproducer = self.avproducers[0]

        avc_elements = self.conf.findall("AVConsumer", None)
        for avc_element in avc_elements:
            avconsumer = AVConsumerFactory.new_avconsumer(**avc_element.attrib)
            self.avconsumers.append(avconsumer)
            avc_psoutlet_element = avc_element.find("PSOutlet", None)
            if avc_psoutlet_element is not None:
                avconsumer.psoutlet = PSOutlet(**avc_psoutlet_element.attrib)
        if self.avconsumers:
            self.avconsumer = self.avconsumers[0]

        sl8800_element = self.conf.find("SL8800")
        if sl8800_element is not None:
            self.sl8800 = SL8800(**sl8800_element.attrib)

        uts800_element = self.conf.find("UTS800")
        if uts800_element is not None:
            self.uts800 = UTS800.new_mhl(**uts800_element.attrib)

        webcam_element = self.conf.find("WebCam")
        webcam_kwargs = webcam_element.attrib if webcam_element is not None else {}
        self.webcam = WebCamFactory.new_webcam(**webcam_kwargs)

    def finalize(self):
        self.device = None
        self.devs = []
        self.devices = None
        self.avproducer = None
        self.avconsumer = None
        self.avproducers = []
        self.avconsumers = []
        self.sl8800 = None
        self.webcam = None
        self.uts800 = None

    def on_runner_start(self):
        self.initialize()
        for dev in self.devs:
            dev.open()

        if self.devices.transmitter is not None:
            self.devices.transmitter.open()

        if self.devices.repeater is not None:
            self.devices.repeater.open()

        if self.devices.receiver is not None:
            self.devices.receiver.open()

    def on_runner_stop(self):
        for dev in self.devs:
            dev.close()

        if self.devices.receiver is not None:
            self.devices.receiver.close()

        if self.devices.repeater is not None:
            self.devices.repeater.close()

        if self.devices.transmitter is not None:
            self.devices.transmitter.close()

        if self.avproducer is not None:
            self.avproducer.close()

        self.finalize()

    def __repr__(self):
        return "<TestBench '%s'>" % self.name

    def __str__(self):
        return self.__repr__()