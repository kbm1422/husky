import logging
logger = logging.getLogger(__name__)
from simg.test.framework import TestContextManager, parametrize
from base import BaseJaxTestCase
import time


class SimBlockerTestCase(BaseJaxTestCase):
    def setUp(self):
        resource = TestContextManager.current_context().resource
        self.txunit, self.rxunit = resource.acquire_pair()
        self.dur = 20
        self.tx_gen3_1 = self.txunit.device.gen3_1
        self.tx_gen3_2 = self.txunit.device.gen3_2
        self.rx_gen3_1 = self.rxunit.device.gen3_1
        self.rx_gen3_2 = self.rxunit.device.gen3_2
        self.capture_image_dir = os.path.join(self.logdir, "images")
        fs.mkpath(self.capture_image_dir)
        self.capture_image_name = os.path.join(self.capture_image_dir, self.name + ".jpg")
        self.make_connected(self.txunit.device, self.rxunit.device)

    def tearDown(self):
        self.rxunit.webcam.capture_image(self.capture_image_name)

    def test_block_tx_main_bb(self):
        self.test_recovery_capability(self.tx_gen3_1)

    def test_block_tx_sub_bb(self):
        self.test_recovery_capability(self.tx_gen3_2)

    def test_block_rx_main_bb(self):
        self.test_recovery_capability(self.rx_gen3_1)

    def test_block_rx_sub_bb(self):
        self.test_recovery_capability(self.rx_gen3_2)