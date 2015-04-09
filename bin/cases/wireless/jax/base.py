import logging
logger = logging.getLogger(__name__)

import time
from simg.test.framework import TestCase


class BaseJaxTestCase(TestCase):
    def make_connected(self, tx_device, rx_device):
        # rx_gen3_1_state = rx_device.gen3_1.getDevState()
        # rx_gen3_2_state = rx_device.gen3_2.getDevState()
        # if rx_gen3_1_state != "connected":
        #     rx_gen3_1_mac = rx_device.gen3_1.getMacAddress()
        #     tx_device.gen3_1.connect(rx_gen3_1_mac)
        # if rx_gen3_2_state != "connected":
        #     rx_gen3_2_mac = rx_device.gen3_2.getMacAddress()
        #     tx_device.gen3_2.connect(rx_gen3_2_mac)
        # self._test_connection(rx_device)
        # self.txunit.device.nvramreset()
        self.txunit.device.reset()
        # self.rxunit.device.nvramreset()
        self.rxunit.device.reset()
        time.sleep(20)
        pass

    def _test_connection(self, device, warn_time=15, fail_time=50):
        start_time = time.time()
        connected_time = None
        while True:
            gen3_1_state = device.gen3_1.getDevState()
            gen3_2_state = device.gen3_2.getDevState()
            current_time = time.time()
            if current_time - start_time > fail_time:
                break
            if gen3_1_state == "connected" and gen3_2_state == "connected":
                connected_time = current_time
                break
            time.sleep(0.5)
        self.assertIsNotNone(connected_time, "Both Main and Sub need connected in 50s")
        self.assertLessEqual(connected_time-start_time, warn_time,
                             msg="Both Main and Sub connected spend time should less equal than 15s",
                             iswarning=True)
        time.sleep(15)

    def _test_noconnection(self, device):
        gen3_1_state = device.gen3_1.getDevState()
        gen3_2_state = device.gen3_2.getDevState()
        time.sleep(15)
        self.assertNotEqual(gen3_1_state, "connected", "gen3_main_state should not connect")
        self.assertNotEqual(gen3_2_state, "connected", "gen3_sub_state should not connect")

    def test_recovery_capability(self, device, duration=20, warn_time=15, fail_time=50):
        with device.log_subject.listen("baseband video UNMUTE") as listener:
            device.sendcmd("start_beacon_loss_test " + str(duration))
            time.sleep(duration)
            recovery_start_time = time.time()
            return_from_listener = listener.get(timeout=100)
            recovery_end_time = time.time()

            recovery_time = recovery_end_time - recovery_start_time

            if not return_from_listener:
                self.fail("The LOG is not found and the devices are disassociated.")

            self.assertLessEqual(recovery_time, warn_time, "The devices are associated again.")

            if warn_time < recovery_time < fail_time:
                self.warn("The devices are reassociated under %s seconds" % recovery_time)
            else:
                self.fail("The devices are reassociated under %s seconds" % recovery_time)