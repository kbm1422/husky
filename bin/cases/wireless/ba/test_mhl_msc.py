#!/usr/bin/evn python
# -*- coding: UTF-8 -*-
#B&A MHL RCP test suite
#Including test case: rcp_input_device_write, rcp_in_status_write, rcp_recv_code_read, rcp_send_code_write_read, rcp_out_status_read
#Note: before test, make sure B&A has connected with windows PC through USB cable  and installed ADB enviroment in windows OS  , driver has been installed and MHL firwmare has been loaded
import logging
logger = logging.getLogger(__name__)

import time
from .base import BaseTestCase
from simg.test.framework import TestContextManager,parametrize
from simg.devadapter.wired.base import MscMessage
import random

"""
RCP: Remote Control Protocol


RAP: Request Action Protocol
    0x00 – POLL
    0x10 – CONTENT_ON
    0x11 – CONTENT_OFF
    0x20 – CBUS_MODE_DOWN request to change from eCBUS mode to MHL1/MHL2 mode
    0x21 – CBUS_MODE_UP request to change from MHL1/MHL2 mode to eCBUS mode

UCP: UTF-8 Character Protocol
"""

RCP = 0x10
RCPK = 0x11
RCPE = 0x12

RAP = 0x20
RAPK = 0x21

UCP = 0x30
UCPK = 0x31
UCPE = 0x32


vals = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05,0x06,0x07,0x08,0x09, 0x0d, 0x20, 0x21, 0x22, 0x23,\
        0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2b,0x33,0x44, 0x45, 0x46, 0x48, 0x49, 0x4a,0x4b, 0x4c,\
        0x60,0x61,0x64]
temp = map(lambda x:eval(hex(x+128)),vals)

RCP_SUPPORTED_KEY_CODES = vals+temp
UCP_SUPPORTED_CODES = range(0, 256)



class MhlRcpTestCase(BaseTestCase):
    def setUp(self):
        context = TestContextManager().getCurrentContext()
        self.txunit, self.rxunit = context.resource.acquire_pair()
        logger.debug("Before test, change mode to mhl first")
        self.make_mode(self.txunit,"mhl")



    def test_rcp_input_device_write(self):
        """Test RCP input device can be written and read correctly.
           Steps: 1. Make sure driver in MHL mode
           2. Write value 0 or 1 to input device node of RCP(0: Route RCP traffic to sysfs and uevent interfaces;1: Handle
            RCP traffice within the driver.
           3. Check pint1: read back value of input device, and check if it's same as the setting"""

        vals = [0, 1]
        val = random.choice(vals)
        logger.debug("current rcp input_device setting value is %s" % val)
        self.txunit.device.setMSCInputDevice("rcp",val)
        time.sleep(1)
        current_val = self.txunit.device.getMSCInputDevice("rcp")
        self.assertEqual(val, int(current_val,16),"should get rcp input_dev value is same as %s" % val)

    def test_rcp_in_status_write(self):
        """Test RCP input status can be written correclty.
           Steps: 1. Make sure MHL connection established
           2. Set input_dev node of RCP to 0
           3. Write value to input status node(0x00:No Error;0x01:Ineffective Key Code,RCPE;0x02: Responder Busy)
           4. Check point1: check valid value can be written successfully """


        vals = [0x00, 0x01,0x02]
        val = random.choice(vals)
        logger.debug("current rcp in_status setting value is %s" % val)
        self.txunit.device.enableMSCInputDev("rcp")
        current_val = self.txunit.device.setMSCInStatus("rcp",val)
        time.sleep(0.5)
        self.assertEqual(0,current_val,"should get returncode is 0 ")
    #
    @parametrize("rcp_code", type=int, iteration=RCP_SUPPORTED_KEY_CODES)
    def test_rcp_send_code_write_read(self):
        """steps: 1.make sure MHL connection establish
                  2.Set input_dev node of RCP to 0 """
        self.name = ("current rcp send is 0x%02X" % self.rcp_code)
        self.txunit.device.enableMSCInputDev("rcp")
        resp = self.txunit.device.send_msc_message("rcp", self.rcp_code)
        self.assertFalse(resp[0], "should set rcp successfully and return code is none")
        self.assertEqual(self.rcp_code, int(resp[1],16), "should cat same rcp code from out node and current send is %s" % self.rcp_code)
        self.assertEqual(0x00,resp[2],"should get RCPK")
        time.sleep(0.5)
        resp2=self.rxunit.device.recv_msc_message()
        self.assertEqual(0x10, resp2.type, "should receive opcode is 0x10")
        self.assertEqual(self.rcp_code, resp2.code, "downstream device should receive same rcp key code")

    @parametrize("rcp_code", type=int, iteration=RCP_SUPPORTED_KEY_CODES)
    def test_rcp_recv_code_read(self):
        """need add Rogue as prior device to send rcp key to BA """
        self.name = ("current rcp recv is 0x%02X" % self.rcp_code)
        self.txunit.device.enableMSCInputDev("rcp")
        message = MscMessage(0x10,self.rcp_code)
        self.rxunit.device.send_msc_message(message)
        time.sleep(0.5)
        resp = self.txunit.device.recv_msc_message("rcp")
        self.assertEqual(self.rcp_code,int(resp[0],16),"should receive same rcp code from in node")
        self.assertRegexpMatches(resp[1], ".*Permission denied", "should not set remote and feeback is Permission denied ")


    def test_rap_input_device_write(self):
        """Test RCP input device can be written and read correctly.
           Steps: 1. Make sure driver in MHL mode
           2. Write value 0 or 1 to input device node of RAP(0: Route RAP traffic to sysfs and uevent interfaces;1: Handle
            RAP traffice within the driver.
           3. Check pint1: read back value of input device, and check if it's same as the setting"""
        vals = [0, 1]
        val = random.choice(vals)
        logger.debug("current rap input_device setting value is %s" % val)
        self.txunit.device.setMSCInputDevice("rap",val)
        time.sleep(1)
        current_val = self.txunit.device.getMSCInputDevice("rap")
        self.assertEqual(val, int(current_val,16),"should get rap input_dev value is same as %s" % val)

    def test_rap_in_status_write(self):
        """Test RAP input status can be written correclty.
           Steps: 1. Make sure MHL connection established
           2. Set input_dev node of RAP to 0
           3. Write value to input status node(0x00:No Error;0x03: Responder Busy)
           4. Check point1: check valid value can be written successfully """


        vals = [0x00,0x03]
        val = random.choice(vals)
        logger.debug("current rap in_status setting value is %s" % val)
        self.txunit.device.enableMSCInputDev("rap")
        current_val = self.txunit.device.setMSCInStatus("rap",val)
        time.sleep(0.5)
        self.assertEqual(0,current_val,"should get returncode is 0 ")

    @parametrize("rap_code", type=int, iteration=[0x10, 0x00, 0x11])
    def test_rap_send_code_write_read(self):
        """steps: 1.make sure MHL connection establish
                  2.Set input_dev node of RAP to 0 """
        self.txunit.device.enableMSCInputDev("rap")
        resp = self.txunit.device.send_msc_message("rap", self.rap_code)
        self.assertFalse(resp[0], "should set rap successfully and return code is none")
        self.assertEqual(self.rap_code, int(resp[1],16), "should cat same rap code from out node and current send is %s" % self.rap_code)
        self.assertEqual(0x00,resp[2],"should get RAPK")
        time.sleep(2)
        resp2=self.rxunit.device.recv_msc_message()
        self.assertEqual(0x20, resp2.type, "should receive opcode is 0x20")
        self.assertEqual(self.rap_code, resp2.code, "downstream device should receive same rap key code")

    @parametrize("rap_code", type=int, iteration=[0x00, 0x10, 0x11])
    def test_rap_recv_code_read(self):
        """need add Rogue as prior device to send rcp key to BA """
        self.txunit.device.enableMSCInputDev("rap")
        message = MscMessage(0x20,self.rap_code)
        self.rxunit.device.send_msc_message(message)
        time.sleep(1)
        resp = self.txunit.device.recv_msc_message("rap")
        print "rap recv is "
        print resp
        self.assertEqual(self.rap_code,int(resp[0],16),"should receive same rap code from in node and current node is %s"%int(resp[0],16))
        print resp[0]
        self.assertRegexpMatches(resp[1], ".*Permission denied", "should not set remote and feeback is Permission denied ")

    def test_ucp_input_device_write(self):
        """Test UCP input device can be written and read correctly.
           Steps: 1. Make sure driver in MHL mode
           2. Write value 0 or 1 to input device node of RCP(0: Route RCP traffic to sysfs and uevent interfaces;1: Handle
            RCP traffice within the driver.
           3. Check pint1: read back value of input device, and check if it's same as the setting"""
        vals = [0, 1]
        val = random.choice(vals)
        logger.debug("current rcp input_device setting value is %s" % val)
        self.txunit.device.setMSCInputDevice("ucp",val)
        time.sleep(1)
        current_val = self.txunit.device.getMSCInputDevice("ucp")
        self.assertEqual(val, int(current_val,16),"should get ucp input_dev value is same as %s" % val)

    def test_ucp_in_status_write(self):
        """Test RCP input status can be written correclty.
           Steps: 1. Make sure MHL connection established
           2. Set input_dev node of RCP to 0
           3. Write value to input status node(0x00:No Error;0x01:Ineffective Key Code)
           4. Check point1: check valid value can be written successfully """


        vals = [0x00, 0x01]
        val = random.choice(vals)
        logger.debug("current rcp in_status setting value is %s" % val)
        self.txunit.device.enableMSCInputDev("ucp")
        current_val = self.txunit.device.setMSCInStatus("rcp",val)
        time.sleep(0.5)
        self.assertEqual(0,current_val,"should get returncode is 0 ")

    @parametrize("ucp_code", type=int, iteration=UCP_SUPPORTED_CODES)
    def test_ucp_send_code_write_read(self):
        """steps: 1.make sure MHL connection establish
                  2.Set input_dev node of RCP to 0 """
        self.name = ("current ucp send is 0x%02X" % self.ucp_code)
        self.txunit.device.enableMSCInputDev("ucp")
        resp = self.txunit.device.send_msc_message("ucp", self.ucp_code)
        self.assertFalse(resp[0], "should set ucp successfully and return code is none")
        self.assertEqual(self.ucp_code, int(resp[1],16), "should cat same ucp code from out node and current send is %s" % self.ucp_code)
        self.assertEqual(0x00,resp[2],"should get UCPK")
        time.sleep(0.5)
        resp2=self.rxunit.device.recv_msc_message()
        self.assertEqual(0x30, resp2.type, "should receive opcode is 0x30")
        self.assertEqual(self.ucp_code, resp2.code, "downstream device should receive same Ucp key code")

    @parametrize("ucp_code", type=int, iteration=UCP_SUPPORTED_CODES)
    def test_ucp_recv_code_read(self):
        self.name = ("current ucp recv is 0x%02X" % self.ucp_code)
        self.txunit.device.enableMSCInputDev("ucp")
        message = MscMessage(0x30,self.ucp_code)
        self.rxunit.device.send_msc_message(message)
        time.sleep(0.5)
        resp = self.txunit.device.recv_msc_message("ucp")
        self.assertEqual(self.ucp_code,int(resp[0],16),"should receive same ucp code from in node")
        self.assertRegexpMatches(resp[1], ".*Permission denied", "should not set remote and feeback is Permission denied ")
















