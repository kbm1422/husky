import logging
logger = logging.getLogger(__name__)

import time

from simg.test.framework import TestContextManager
from simg.devadapter.wireless.base import VendorMsg
from simg.util import sstring

from .base import BaseTestCase


class VendorMessageTestCase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        txunit, rxunit = TestContextManager.current_context().resource.acquire_pair()
        rxunit.device.reset()
        BaseTestCase().make_connected(txunit, rxunit)

    def setUp(self):
        context = TestContextManager().current_context()
        self.txunit, self.rxunit = context.resource.acquire_pair()
        
    def tearDown(self):
        pass

    def test_tx_sendmsg_rx(self):
        """
        1.make sure module in connected state or associated state
        2.set sink filter through swam3 vendor_msg_set_filter 11:11:11
        3.set dest_mac_address through "echo 112233445588> /sys/devices/virtual/video/sii6400/wihd/vendor_msg/dest_mac_addr"
        4.set vendor_id value same as sink filter or not same as filter
        5.set message to sink, through "echo 3344 > send
        6.check get message in sink
        """
        vendor_id = sink_filter = "11:11:11"
        tx_mac_addr = self.txunit.device.getMacAddress()
        rx_mac_addr = self.rxunit.device.getMacAddress()
        sendmsg = VendorMsg(vendor_id, rx_mac_addr, 3, "aa:bb:cc")
        
        self.rxunit.device.setVendorMsgFilter(sink_filter)
        self.txunit.device.sendVendorMsg(sendmsg)

        time.sleep(5)
        recvmsg = self.rxunit.device.recvVendorMsg()
        self.assertEqual(sendmsg.vendorID, recvmsg.vendorID, "RX received vendor_id should be same")
        self.assertEqual(tx_mac_addr, recvmsg.dstMacAddr, "RX received mac_addr should be same with TX")
        self.assertEqual(sendmsg.length, recvmsg.length, "RX received length should be same")
        self.assertEqual(sendmsg.data, recvmsg.data, "RX received vendor_msg should same")
    
    def test_rx_sendmsg_tx(self):
        """
        1.set BA'filter ,set filiter through  'echo 2222222> /sys/devices/virtual/video/sii6400/wihd/vendor_msg/recv_filter'
        2.set sink filter,same as BA or not
        3.send message to source ,through vendor_msg_send 11:11:11 112233445566 2 DD:DD
        """
        vendor_id = recv_filter = "22:22:22"
        data = "EE:DD:AA"
        self.txunit.device.setVendorMsgFilter(recv_filter)
        self.rxunit.device.setVendorMsgFilter(recv_filter)
        
        tx_mac_addr = self.txunit.device.getMacAddress()
        rx_mac_addr = self.rxunit.device.getMacAddress()
        
        with self.txunit.uevent.listen("vendor_msg_received") as listener:
            """
            {"event":"vendor_msg_received","data":{"vendor_id":"222222","mac_addr":"0dd694ca4f00","vendor_msg":"eeddaa"}}
            """
            msg = VendorMsg(vendor_id, tx_mac_addr, len(data.split(":")), data)
            resp = self.rxunit.device.sendVendorMsg(msg)
            self.assertIn("OK", resp, "RX send vendor message to TX should be OK")
            
            event = listener.get(timeout=5)
            self.assertIsNotNone(event, "TX should receive vendor message in 5s")

            vendor_id = event.data['vendor_id']
            self.assertEqual(vendor_id, vendor_id, "TX received vendor_id should same")
            
            mac_addr = sstring.trimMacAddress(event.data['mac_addr'])
            self.assertEqual(mac_addr, rx_mac_addr, "TX received mac_addr should same")
            
            vendor_msg = event.data['vendor_msg']
            self.assertEqual(vendor_msg, data.replace(":", "").lower(), "TX received vendor_msg should same")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )
