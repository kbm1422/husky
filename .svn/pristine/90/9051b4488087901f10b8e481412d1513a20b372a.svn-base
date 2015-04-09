#!/usr/bin/env python
"""HDCP test equipment SL-8800 module"""

import os
import re
import time

    
class SL8800():
    
    __cases = {
        'RECEIVER'    : ["2C-01T1", "2C-01T2", "2C-02", "2C-03", "2C-04", "2C-05"],
        'TRANSMITTER' : ["1A-01", "1A-02", "1A-03", "1A-04", "1A-05", "1A-06", "1A-07", "1A-08", "1A-09", 
                         "1A-11T1", "1A-11T2", "1A-11T3", "1A-12", "1A-13T1", "1A-13T2","1B-01", "1B-02", 
                         "1B-03", "1B-04", "1B-05", "1B-06", "1B-07", "1B-08", "1B-09", "1B-10T0", "1B-10T1"],
        'REPEATER'    : ["Init", "3A-01", "3A-02", "3A-03", "3A-04", "3A-05T1", "3A-05T2", "3A-05T3", "3A-06", "3A-07T1", 
                         "3A-07T2","3B-01", "3B-02", "3B-03", "3B-04", "3B-05", "3B-06", "3B-07T0", "3B-07T1",
                         "3C-01-1", "3C-01-2","3C-01-3","3C-01-4", "3C-04", "3C-05", "3C-06", "3C-07", "3C-08", "3C-09-1", "3C-09-2", 
                         "3C-10-1", "3C-10-2", "3C-11", "3C-12", "3C-13", "3C-14", "3C-15", "3C-16", "3C-17", "3C-18",    
                         "3C-19", "3C-20", "3C-21", "3C-22", "3C-23", "3C-24", "3C-25T0", "3C-25T1", "3C-25T2"]
    }
    
    __props = {
        'interface' : "HDMI",
        'dut'       : "Receiver"
    }
        
    def __init__(self, **kwargs):
        self.mhl = ""
        self.props = SL8800.__props.copy()
        self.cases = SL8800.__cases
        unk = [x for x in kwargs.keys() if x not in SL8800.__props]
        assert not unk
        self.props.update(kwargs)

        self.infc = self.props['interface']
        self.dut = self.props['dut']
        
        if re.search("mhl", self.infc, re.I):
            self.mhl = " MHL"

        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.exe_receiver = os.path.join(self.dir, "ReceiverTest.exe")
        self.exe_transmitter = os.path.join(self.dir, "TransmitterTest.exe")
        self.exe_repeater = os.path.join(self.dir, "RepeaterTest.exe")
    
    def mhl_init(self):
        res = 0
        if re.search("receiver", self.dut, re.I):
            exe = self.exe_receiver
        elif re.search("repeater", self.dut, re.I):
            exe = self.exe_repeater
        else:
            raise ValueError

        res = os.system(exe + " Init MHL")
        assert res == 0, "MHL Initialization Failed"

    def test(self, case):
        assert case in self.cases[self.dut.upper()], "this case item is incorrect"

        if re.search("mhl", self.infc, re.I):
            self.mhl_init()
            time.sleep(2)

        if re.search("receiver", self.dut, re.I):
            exe = self.exe_receiver
        elif re.search("transmitter", self.dut, re.I):
            exe = self.exe_transmitter
        elif re.search("repeater", self.dut, re.I):
            exe = self.exe_repeater
        else:
            raise ValueError

        res = os.system(exe + " " + case + self.mhl)
        if res == 0:
            return res
        else:
            return -1

           
"""class test"""
def classtest():
    sl_obj = SL8800(interface = "hdmi",
                    dut = "receiver")
    res = sl_obj.test("2C-01T1")
    print(res)
    res = sl_obj.test("2C-01T2")
    print(res)
    
if __name__ == "__main__":
    classtest()
