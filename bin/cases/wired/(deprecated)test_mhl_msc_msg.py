#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import time
import random

from simg.devadapter import BaseDeviceAdapter
from simg.test.framework import TestCase, parametrize, TestContextManager

"""
rap opcode should be:
0x00: No Error
0x01: Unrecognized Action Code
0x02: Unsupported Code
0x03: Responder Busy
"""


@parametrize("device_transmitter", type=BaseDeviceAdapter, fetch=parametrize.FetchType.LAZY)
@parametrize("device_receiver", type=BaseDeviceAdapter, fetch=parametrize.FetchType.LAZY)
class MSCTestCaseReceive(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_msc_msg_rap(self):
        try:
            rap_codes = [16, 17]
            code = random.choice(rap_codes)
            self.device_transmitter.send_rap(code)
            time.sleep(3)
            message = self.device_receiver.recv_msc_message()
            self.assertEqual(message.type, 0x20, "should receive RAP 0x20 opcode and current is 0x%02X" % message.type)
            self.assertEqual(message.code, code, "should receive RAP key value is 0x%02X" % code)
            rapk = self.device_receiver.send_msc_message(0x21, code)
        finally:
            self.device_transmitter.send_rap(10)

        #below is check whether transmitter received msg is correct or not
        # message = self.device_transmitter.recv_msc_message()
        # self.assertEqual(0x21, message.type,
        #                  "should receive rapk 0x21 from responder and current rapk is 0x%02X, current send key is 0x%02X" % (message.type, key))
        # self.assertEqual(message.code, 0x00, "should receive rap opcode 0x00 and current is 0x%02X" % message.code)

    def test_msc_msg_rap_unrecognized(self):
        rap_codes = [0xFF, 0x77, 0x76]
        code = random.choice(rap_codes)
        self.device_transmitter.send_rap(code)
        time.sleep(3)
        message = self.device_transmitter.recv_msc_message()
        self.assertEqual(0x21, message.type,
                         "should receive rapk 0x21 from responder and current rapk is 0x%02X, current send key is 0x%02X" % (message.type, code))
        self.assertEqual(message.code, 0x01, "should receive rap opcode 0x01 and current is 0x%02X" % message.code)

    def test_msc_msg_rap_unsupported(self):
        rap_codes = [0x20, 0x21]
        code = random.choice(rap_codes)
        self.device_transmitter.send_rap(code)
        time.sleep(3)
        message = self.device_transmitter.recv_msc_message()
        self.assertEqual(0x21, message.type,
                         "should receive rapk 0x21 from responder and current rapk is 0x%02X, current send key is 0x%02X" % (message.type, code))
        self.assertEqual(message.code, 0x02, "return value should be 0x02 and current is 0x%02X" % message.code)

    def test_msc_msg_rcp_receive_normal(self):
        rcp_codes = [0x41, 0x42, 0x43, 0x65, 0x66]
        code = random.choice(rcp_codes)
        self.device_transmitter.send_rcp(code)
        time.sleep(3)
        message = self.device_receiver.recv_msc_message()
        self.assertEqual(message.type, 0x10, "should receive RCP 0x10 opcode and current is 0x%02X" % message.type)
        self.assertEqual(message.code, code, "should receive RCP key value is 0x%02X" % code)

    def test_msc_msg_rcp_receive_optional(self):
        rcp_codes = [
            0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D,
            0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x50, 0x51, 0x20, 0x21, 0x22,
            0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x60, 0x61, 0x62, 0x63,
            0x64, 0x65, 0x66, 0x67, 0x68, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,
            0x71, 0x72, 0x73, 0x74, 0x75, 0x7E
        ]
        code = random.choice(rcp_codes)
        self.device_transmitter.send_rcp(code)
        time.sleep(3)
        message = self.device_receiver.recv_msc_message()
        self.assertEqual(message.type, 0x10, "should receive RCP 0x10 opcode and current is 0x%02X" % message.code)
        self.assertEqual(message.code, code, "should receive RCP key value is 0x%02X" % code)

#not ready ,because we can't see any RCPK sending from Boston now.
    # def test_msg_rcp_receive_reserved(self):
    #     supported_rcp_code = [0x10,0x4D]
    #     key = random.choice(supported_rcp_code)
    #     self.device_transmitter.send_rcp(key)
    #     time.sleep(3)
    #     message = self.device_receiver.recv_msc_message()
    #     print hex(msg.subCmd), hex(msg.codeValue)
    #     self.assertNotEqual(msg.subCmd, 0x20, "should not receive RCP 0x10 opcode and current is %s " % hex(msg.subCmd))
    #     self.assertNotEqual(msg.codeValue, key, "should not receive RCP key value is 0x%02X" % key)

    def test_msc_msg_ucp(self):
        all_codes = range(0, 256)
        reversed_codes = [192, 193, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
        supported_ucp_codes = list(set(all_codes)-set(reversed_codes))
        code = random.choice(supported_ucp_codes)
        self.device_transmitter.send_ucp(code)
        time.sleep(5)
        message = self.device_receiver.recv_msc_message()
        self.assertEqual(message.type, 0x30,
                         "should receive UCP 0x30 opcode and current is 0x%02X and current send key is 0x%02X" % (message.type, code))
        self.assertEqual(message.code, code, "should receive UCP key value is 0x%02X" % code)

    # def test_msc_msg_rbp(self):
    #     rbp_key = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
    #     key = random.choice(rbp_key)
    #     self.device_transmitter.send_rbp[key]
    #     time.sleep(3)
    #     message = self.device_receiver.recv_msc_message()
    #     print hex(message.subCmd), hex(message.codeValue)
    #     self.assertEqual(message.subCmd, 0x22,
    #                      "should receive RBP 0x22 opcode and current is %s and current sendkey is %02X" % (
    #                          hex(message.subCmd), key))
    #     self.assertEqual(message.codeValue, key, "should receive RBP key value is 0x%02X" % key)


@parametrize("device_transmitter", type=BaseDeviceAdapter, fetch=parametrize.FetchType.LAZY)
@parametrize("device_receiver", type=BaseDeviceAdapter, fetch=parametrize.FetchType.LAZY)
class MSCTestCaseSend(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_msc_msg_rap(self):
        try:
            rap_codes = [00, 16, 17]
            code = random.choice(rap_codes)
            self.device_receiver.send_msc_message(0x20,code)
            time.sleep(3)
            received_key = self.device_transmitter.receive_rap()
            print "recv key is "
            print received_key
            self.assertEqual(received_key, code, "should receive RAP key value is same as sending code 0x%02X  and current recv RAP is 0x%02X " % (code, received_key))

            #should receive RAPK in Boston
            message = self.device_receiver.recv_msc_message()
            self.assertEqual(message.type, 0x21, "should receive RAPK 0x21 opcode and current is 0x%02X  and current send key is 0x%02X" % (message.type, code))
            self.assertEqual(message.code, 0x00, "should receive RAPK opcode is 0x00")

        finally:
            self.device_transmitter.send_rap(10)

    def test_msc_msg_rcp(self):
        supported_rcp_key = [
            0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x09, 0x0D,
            0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2B, 0x2C,
            0x33, 0x44, 0x45, 0x46, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x60, 0x61, 0x64
        ]
        code = random.choice(supported_rcp_key)
        # for i in range(0,len(supported_rcp_key)):
        #     code = supported_rcp_key[i]
        #first make sure titan can read received RCP value
        self.device_transmitter.disable_rcp_input_dev()
        self.device_receiver.send_msc_message(0x10, code)
        time.sleep(3)
        received_key = self.device_transmitter.receive_rcp()
        self.assertEqual(received_key, code,
                         "should receive RCP key value is same as sending code 0x%02X  and current recv RCP is 0x%02X" % (code, received_key))
        #second make sure Boston can read receive RCPK which is sent by titan
        self.device_transmitter.enable_rcp_input_dev()
        self.device_receiver.send_msc_message(0x10, code)
        time.sleep(3)
        message = self.device_receiver.recv_msc_message()
        self.assertEqual(message.type, 0x11,
                         "should receive RCPK 0x11 opcode and current is 0x%02X and current send key is 0x%02X" % (message.type, code))
        self.assertEqual(message.code, code, "should receive RCP key value is 0x%02X" % code)

    def test_msc_msg_rcp_reserved(self):
        reserved_key = [0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B,
                        0x1C, 0x1D, 0x1E, 0x1F, 0x2D, 0x2E, 0x2F, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3F, 0x40, 0x52, 0x53,
                        0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x67, 0x69, 0x6A, 0x6B,
                        0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7F]

        key = random.choice(reserved_key)
         # for i in range(0,len(reserved_key)):
         #     key = reserved_key[i]
         #make sure Boston can read receive RCPE and RCPK which is sent by titan
        self.device_transmitter.enable_rcp_input_dev()
        self.device_receiver.send_msc_message(0x10, key)
        message_e = self.device_receiver.recv_msc_message()
        self.assertEqual(message_e.type, 0x12,
                         "should receive RCPE 0x12 opcode and current is 0x%02X " % message_e.type)
        time.sleep(5)
        message_k = self.device_receiver.recv_msc_message()

        self.assertEqual(message_k.type, 0x11,
                         "should receive RCPK 0x11 opcode and current is 0x%02X  and current send key is 0x%02X" % (message_k.type, key))
        self.assertEqual(message_k.code, key, "should receive RCP key value is 0x%02X" % key)

    def test_msc_msg_ucp(self):
        all_codes = range(0, 256)
        reversed_codes = [192, 193, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
        supported_ucp_codes = list(set(all_codes)-set(reversed_codes))
        code = random.choice(supported_ucp_codes)
        # for i in range(0, 256):
        #     code = i
        self.device_transmitter.disable_ucp_input_dev()
        self.device_receiver.send_msc_message(0x30, code)
        time.sleep(3)
        received_key = self.device_transmitter.receive_ucp()
        self.assertEqual(received_key, code,
                         "should receive UCP key value is same as sending code 0x%02X  and current recv UCP is 0x%02X" % (code, received_key))
        time.sleep(3)
        self.device_transmitter.enable_ucp_input_dev()
        self.device_receiver.send_msc_message(0x30, code)
        time.sleep(2)
        message_k = self.device_receiver.recv_msc_message()
        time.sleep(2)
        self.assertEqual(message_k.type, 0x31,
                         "should receive UCP 0x31 opcode and current is 0x%02X and current send key is 0x%02X " % (message_k.type, code))
        self.assertEqual(message_k.code, code, "should receive UCP key value is 0x%02X" % code)

    def test_msc_msg_rbp(self):
        rbp_key = [0x0, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x20, 0x21, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35]
        code = random.choice(rbp_key)
        # for i in range(0,len(rbp_key)):
        #     code = rbp_key[i]
        self.device_transmitter.disable_rbp_input_dev()
        self.device_receiver.send_msc_message(0x22, code)
        time.sleep(3)
        received_key = self.device_transmitter.receive_rbp()
        self.assertEqual(received_key, code,
                         "should receive RBP key value is same as sending code 0x%02X  and current recv RBP is 0x%02X " % (code, received_key))
        time.sleep(3)
        self.device_transmitter.enable_rbp_input_dev()
        self.device_receiver.send_msc_message(0x22, code)
        time.sleep(2)
        message_k = self.device_receiver.recv_msc_message()
        time.sleep(3)
        self.assertEqual(message_k.type, 0x23,
                         "should receive RBPK 0x23 opcode and current is 0x%02X and current send key is 0x%02X " % (message_k.type, code))

        self.assertEqual(message_k.code, code, "should receive RBP key value is 0x%02X" % code)

    def test_msc_msg_rbp_reserved(self):
        rbp_key = [0x0, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x20, 0x21, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35]
        all_codes = range(0, 256)
        reserved_key = list(set(all_codes) - set(rbp_key))
        key = random.choice(reserved_key)
        # for i in range(0,len(reserved_key)):
        #     key = reserved_key[i]
        self.device_transmitter.enable_rbp_input_dev()
        self.device_receiver.send_msc_message(0x22, key)
        message_e = self.device_receiver.recv_msc_message()
        time.sleep(2)
        self.assertEqual(message_e.type, 0x24,
                         "should receive RBPE 0x24 opcode and current is 0x%02X " % message_e.type)
        time.sleep(3)
        message_k = self.device_receiver.recv_msc_message()
        self.assertEqual(message_k.type, 0x23,
                         "should receive RBPK 0x11 opcode and current is 0x%02X and current send key is 0x%02X" % (message_k.type, key))
        self.assertEqual(message_k.code, key, "should receive RBP key value is 0x%02X" % key)
