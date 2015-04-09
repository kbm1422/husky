#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
from simg import fs
from simg.test.framework import TestContextManager, parametrize, name
from base import BaseJaxTestCase

d = {
    "lr0": (0x1a, 0x3a),
    "lr1": (0x9, 0x29),
    "lr2": (0xa, 0x2a),
    "lr3": (0xb, 0x2b),
    "lr4": (0x19, 0x39)
}


class MultichannelTestCase(BaseJaxTestCase):
    def setUp(self):
        resource = TestContextManager.current_context().resource
        self.txunit, self.rxunit = resource.acquire_pair()


        self.capture_image_dir = os.path.join(self.logdir, "images")
        self.capture_image_name = os.path.join(self.capture_image_dir, "%s_%s.jpg" % (self.name, self.cycleindex))
        self.make_connected(self.txunit.device, self.rxunit.device)
        fs.mkpath(self.capture_image_dir)

    @name("test_hr2_%(lr)s")
    @parametrize("cycle", iteration=range(2))
    @parametrize("lr", iteration=d)
    def test_hr2_lr(self):
        (t_val, r_val) = d[self.lr]
        try:
            self.txunit.device.gen3_1.sendcmd('nvramset 0x20 0x%x' % t_val)
            self.rxunit.device.gen3_1.sendcmd('nvramset 0x20 0x%x' % r_val)
            self.txunit.device.reset()
            self.rxunit.device.reset()
            self._test_connection(self.rxunit.device)
        finally:
            self.rxunit.webcam.capture_image(self.capture_image_name)

# __test_suite__ = {
#     "name": "test multichannel",
#     "subs": [
#         MultichannelTestCase.test_hr2_lr
#     ]
# }

# """
# <TestSuite name="Factory Test Suite">
#     <For list="{
#     "lr0": (0x1a, 0x3a),
#     "lr1": (0x9, 0x29),
#     "lr2": (0xa, 0x2a),
#     "lr3": (0xb, 0x2b),
#     "lr4": (0x19, 0x39)
# }" type="expression" param="lr">
#         <TestCase class="cases.wireless.jax.test_multichannel.MultichannelTestCase" method="test_hr2_lr">
#             <Attribute name="lr" value="%(lr)s"/>
#         </TestCase>
#     </For>
# </TestSuite>
# """