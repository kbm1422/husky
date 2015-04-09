import logging
logger = logging.getLogger(__name__)

import os
import time

from ctypes import byref
from base import RX_PORT_MAPPER
from simg import fs
from simg.test.framework import TestCase, TestContextManager, parametrize
from simg.devadapter import BaseDeviceAdapter
from simg.util.avconsumer import BaseAVConsumer
from simg.util.avproducer import BaseAVProducer
from simg.devadapter.wired.boston.Sii9777RxLib import Sii9777RxPort_t, Sii9777InputSelectSet



@parametrize("listen_timeout", type=float, default=20)
@parametrize("device", type=BaseDeviceAdapter, fetch=parametrize.FetchType.LAZY)
@parametrize("rx_port", type=str, choice=RX_PORT_MAPPER.keys())
class PowerCycleTestCase(TestCase):
    def setUp(self):
        capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(capture_image_dir)
        self.capture_image_name = os.path.join(capture_image_dir, self.name + ".jpg")
        self.webcam = TestContextManager.current_context().resource.webcam

    def _set_input(self):
        logger.debug("select input to %s", self.rx_port)
        port = Sii9777RxPort_t(RX_PORT_MAPPER[self.rx_port])
        with self.device.lock:
            retcode = Sii9777InputSelectSet(self.device.drv_instance, byref(port))
        assert retcode == 0, "Sii9777InputSelectSet %s failed" % self.rx_port

    def test_powercycle_device(self):
        try:
            self.device.close()
            self.device.psoutlet.turnoff()
            time.sleep(10)
            self.device.psoutlet.turnon()
            self.device.open()
            with self.device.log_subject.listen("TX0 AVMUTE=0") as listener0,\
                 self.device.log_subject.listen("TX1 AVMUTE=0") as listener1,\
                 self.device.log_subject.listen("TX2 AVMUTE=0") as listener2:
                self._set_input()
                starttime = time.time()
                event0 = listener0.get(timeout=self.listen_timeout)
                event1 = listener1.get(timeout=self.listen_timeout)
                event2 = listener2.get(timeout=self.listen_timeout)
                stoptime = time.time()
                self.assertIsNotNone(event0, msg="should get log keyword 'TX0 AVMUTE=0' in %ss" % self.listen_timeout)
                self.assertIsNotNone(event1, msg="should get log keyword 'TX1 AVMUTE=0' in %ss" % self.listen_timeout)
                self.assertIsNotNone(event2, msg="should get log keyword 'TX2 AVMUTE=0' in %ss" % self.listen_timeout)

                conn_time = round(stoptime-starttime, 3)
                self.add_concern("connection time", conn_time)
            time.sleep(15)
        finally:
            self.webcam.capture_image(self.capture_image_name)

    @parametrize("sink", type=BaseAVConsumer, fetch=parametrize.FetchType.LAZY)
    @parametrize("listen_keyword", type=str)
    def test_powercycle_sink(self):
        self._set_input()
        self.sink.psoutlet.turnoff()
        time.sleep(8)
        try:
            with self.device.log_subject.listen(self.listen_keyword) as listener:
                self.sink.psoutlet.turnon()
                starttime = time.time()
                event = listener.get(timeout=self.listen_timeout)
                stoptime = time.time()
                self.assertIsNotNone(event, msg="should get log keyword '%s' in %ss" % (self.listen_keyword,
                                                                                        self.listen_timeout))

                conn_time = round(stoptime-starttime, 3)
                self.add_concern("connection time", conn_time)
            time.sleep(15)
        finally:
            self.webcam.capture_image(self.capture_image_name)

    @parametrize("source", type=BaseAVProducer, fetch=parametrize.FetchType.LAZY)
    def test_powercycle_source(self):
        self._set_input()
        self.source.psoutlet.turnoff()
        time.sleep(10)

        try:
            with self.device.log_subject.listen("TX0 AVMUTE=0") as listener0,\
                self.device.log_subject.listen("TX1 AVMUTE=0") as listener1,\
                self.device.log_subject.listen("TX2 AVMUTE=0") as listener2:
                self.source.psoutlet.turnon()
                starttime = time.time()
                event0 = listener0.get(timeout=self.listen_timeout)
                event1 = listener1.get(timeout=self.listen_timeout)
                event2 = listener2.get(timeout=self.listen_timeout)
                stoptime = time.time()
                self.assertIsNotNone(event0, msg="should get log keyword 'TX0 AVMUTE=0' in %ss" % self.listen_timeout)
                self.assertIsNotNone(event1, msg="should get log keyword 'TX1 AVMUTE=0' in %ss" % self.listen_timeout)
                self.assertIsNotNone(event2, msg="should get log keyword 'TX2 AVMUTE=0' in %ss" % self.listen_timeout)

                conn_time = round(stoptime-starttime, 3)
                self.add_concern("connection time", conn_time)
            time.sleep(15)
        finally:
            self.webcam.capture_image(self.capture_image_name)