#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from simg.test.framework import TestCase
from simg.test.framework import TestContextManager
from simg.util.webcam import WebCamFactory
from simg.util.uts800.uts800 import mhl2_explorer,mhl2_analyzer,mhl3
#from simg.util.avproducer.astro import VG876
from simg.util.avproducer.qd_cts import QD882

from simg.devadapter.wired.base import MscMessage, Mhl2Interface
from simg.test.framework import TestCase, parametrize, TestContextManager

import ConfigParser
import re
import ctypes
import subprocess
import time
import os
from threading import Thread

RCP = 0x10
RCPK = 0x11
RCPE = 0x12

RAP = 0x20
RAPK = 0x21

UCP = 0x30
UCPK = 0x31
UCPE = 0x32

RAP_STATUS_CODE__NO_ERROR = 0x00
RAP_STATUS_CODE__UNRECOGNIZED_ACTION_CODE = 0x01
RAP_STATUS_CODE__UNSUPPORTED_ACTION_CODE = 0x02
RAP_STATUS_CODE__RESPONDER_BUSY = 0x03

RCP_STATUS_CODE__NO_ERROR = 0x00
RCP_STATUS_CODE__INEFFECTIVE_KEY_CODE = 0x01
RCP_STATUS_CODE__RESPONDER_BUSY = 0x02

UCP_STATUS_CODE__NO_ERROR = 0x00
UCP_STATUS_CODE__INEFFECTIVE_KEY_CODE = 0x01

flag1 = 0
testcases = {\
    "6.3.1.1": 'Name="6.3.1.1 CBM: Capability Regs" Tag="" Location=""', \
    "6.3.3.1": 'Name="6.3.3.1 CBM: DUT sends (0x62) GET_STATE command" Tag="" Location=""', \
    "6.3.3.2": 'Name="6.3.3.2 CBM: DUT sends (0x63) GET_VENDOR_ID Command" Tag="" Location=""', \
    "6.3.3.3": 'Name="6.3.3.3 CBM: DUT sends (0x6B) GET_MSC_ERRCODE Command" Tag="" Location=""', \
    "6.3.3.4": 'Name="6.3.3.4 CBM: DUT sends (0x60) SET_INT/WRITE_STAT Command" Tag="" Location=""', \
    "6.3.3.5": 'Name="6.3.3.5 CBM: DUT sends (0x6C) WRITE_BURST Command" Tag="" Location=""', \
    "6.3.3.6": 'Name="6.3.3.6 CBM: DUT sends (0x68) MSC_MSG Command" Tag="" Location=""', \
    "6.3.3.7": 'Name="6.3.3.7 CBM: DUT sends (0x6A) GET_DDC_ERRCODE Command" Tag="" Location=""', \
    "6.3.4.1": 'Name="6.3.4.1 CBM: DUT Receives NACK to MSC_MSG" Tag="" Location=""', \
    "6.3.6.1": 'Name="6.3.6.1 CBM: DUT Receives Bad Reply; Control instead of Data" Tag="" Location=""', \
    "6.3.6.2": 'Name="6.3.6.2 CBM: DUT Receives Bad Reply; Data instead of Control" Tag="" Location=""', \
    "6.3.6.3": 'Name="6.3.6.3 CBM: DUT Receives Bad Reply; Control, Control instead of Control, Data" Tag="" Location=""', \
    "6.3.6.4": 'Name="6.3.6.4 CBM: DUT Receives Result Timeout" Tag="" Location=""', \
    "6.3.6.5": 'Name="6.3.6.5 CBM: Verify No Next Command Until Hold-Off after ABORT Seen" Tag="" Location=""', \
    "6.3.7.1": 'Name="6.3.7.1 CBM: DUT Receives Disconnect during Various Commands" Tag="" Location=""', \
    "6.3.8.1": 'Name="6.3.8.1 CBM: Interrupt Regs; SET_INT (0x60); Valid Registers Respond" Tag="" Location=""', \
    "6.3.8.2": 'Name="6.3.8.2 CBM: Status Regs; WRITE_STAT (0x60); Valid Registers Respond" Tag="" Location=""', \
    "6.3.9.1": 'Name="6.3.9.1 CBM: DUT Receives Vendor-specific and Reserved Header Values" Tag="" Location=""', \
    "6.3.10.1": 'Name="6.3.10.1 CBM: DUT receives (0x62) GET_STATE Command" Tag="" Location=""', \
    "6.3.10.2": 'Name="6.3.10.2 CBM: DUT receives (0x63) GET_VENDOR_ID Command" Tag="" Location=""', \
    "6.3.10.3": 'Name="6.3.10.3 CBM: DUT receives (0x61) READ_DEVCAP Command" Tag="" Location=""', \
    "6.3.10.4": 'Name="6.3.10.4 CBM: DUT Receives (0x6B) GET_MSC_ERRCODE Command (When No Err)" Tag="" Location=""', \
    "6.3.10.5": 'Name="6.3.10.5 CBM: DUT Receives (0x6B) GET_MSC_ERRCODE Command (When Err)" Tag="" Location=""', \
    "6.3.10.6": 'Name="6.3.10.6 CBM: DUT Receives (0x6C) WRITE_BURST Command - Supported" Tag="" Location=""', \
    "6.3.10.7": 'Name="6.3.10.7 CBM: DUT Receives (0x68) MSC_MSG Command-RCP_Support=1 &amp; RAP_Support=1" Tag="" Location=""', \
    "6.3.10.8": 'Name="6.3.10.8 CBM: DUT Receives (0x6A) GET_DDC_ERRCODE Command" Tag="" Location=""', \
    "6.3.11.1": 'Name="6.3.11.1 CBM: DUT Receives Reserved Commands" Tag="" Location=""', \
    "6.3.11.2": 'Name="6.3.11.2 CBM: DUT Receives Illegal Commands" Tag="" Location=""', \
    "6.3.11.3": 'Name="6.3.11.3 CBM: DUT Receives Data While No Command Outstanding" Tag="" Location=""', \
    "6.3.11.4": 'Name="6.3.11.4 CBM: DUT Receives (0x33) ACK Packet While No Command Outstanding" Tag="" Location=""', \
    "6.3.11.5": 'Name="6.3.11.5 CBM: DUT Receives (0x34) a NACK Packet While No Command Outstanding" Tag="" Location=""', \
    "6.3.11.6": 'Name="6.3.11.6 CBM: DUT Receives (0x32) EOF While No Command Outstanding" Tag="" Location=""', \
    "6.3.11.7": 'Name="6.3.11.7 CBM: DUT Receives (0x35) ABORT While No Command Outstanding" Tag="" Location=""', \
    "6.3.11.8": 'Name="6.3.11.8 CBM: DUT Receives (0x61) READ_DEVCAP - Offset Control" Tag="" Location=""', \
    "6.3.11.9": 'Name="6.3.11.9 CBM: DUT Receives (0x61) READ_DEVCAP - Offset Invalid" Tag="" Location=""', \
    "6.3.11.10": 'Name="6.3.11.10 CBM: DUT Receives (0x60) SET_INT - Offset Control" Tag="" Location=""', \
    "6.3.11.11": 'Name="6.3.11.11 CBM: DUT Receives (0x60) SET_INT - Data Control" Tag="" Location=""', \
    "6.3.11.12": 'Name="6.3.11.12 CBM: DUT Receives (0x60) WRITE_STAT - Data Control" Tag="" Location=""', \
    "6.3.11.13": 'Name="6.3.11.13 CBM: DUT Receives (0x6C) WRITE_BURST Command - Not Supported" Tag="" Location=""', \
    "6.3.11.14": 'Name="6.3.11.14 CBM: DUT Receives (0x6C) WRITE_BURST - Offset Control" Tag="" Location=""', \
    "6.3.11.15": 'Name="6.3.11.15 CBM: DUT Receives (0x6C) WRITE_BURST - Control Instead of First Data" Tag="" Location=""', \
    "6.3.11.16": 'Name="6.3.11.16 CBM: DUT Receives (0x6C) WRITE_BURST - Data 0 EOF" Tag="" Location=""', \
    "6.3.11.17": 'Name="6.3.11.17 CBM: DUT Receives (0x6C) WRITE_BURST - Data 1 Control" Tag="" Location=""', \
    "6.3.11.18": 'Name="6.3.11.18 CBM: DUT Receives (0x6C) WRITE_BURST - Data 1 EOF" Tag="" Location=""', \
    "6.3.11.19": 'Name="6.3.11.19 CBM: DUT Receives (0x6C) WRITE_BURST - Too Much Data" Tag="" Location=""', \
    "6.3.11.20": 'Name="6.3.11.20 CBM: DUT Receives (0x6C) WRITE_BURST - Offset Wrap ABORT" Tag="" Location=""', \
    "6.3.11.21": 'Name="6.3.11.21 CBM: DUT Receives (0x68) MSC_MSG Command-Both RCP_Support &amp; RAP_Support=0" Tag="" Location=""', \
    "6.3.11.22": 'Name="6.3.11.22 CBM: DUT Receives (0x68) MSC_MSG - Data 0 Control" Tag="" Location=""', \
    "6.3.11.23": 'Name="6.3.11.23 CBM: DUT Receives (0x68) MSC_MSG - Sub-command Illegal" Tag="" Location=""', \
    "6.3.11.24": 'Name="6.3.11.24 CBM: DUT Receives (0x68) MSC_MSG - Data 1 Control" Tag="" Location=""', \
    "6.3.12.1": 'Name="6.3.12.1 CBM: DUT Receives (0x61) READ_DEVCAP - Offset Timeout" Tag="" Location=""', \
    "6.3.12.2": 'Name="6.3.12.2 CBM: DUT Receives (0x60) SET_INT / WRITE_STAT - Offset Timeout" Tag="" Location=""', \
    "6.3.12.3": 'Name="6.3.12.3 CBM: DUT Receives (0x60) SET_INT - Data Timeout" Tag="" Location=""', \
    "6.3.12.4": 'Name="6.3.12.4 CBM: DUT Receives (0x60) WRITE_STAT - Data Timeout" Tag="" Location=""', \
    "6.3.12.5": 'Name="6.3.12.5 CBM: DUT Receives (0x6C) WRITE_BURST - Offset Timeout" Tag="" Location=""', \
    "6.3.12.6": 'Name="6.3.12.6 CBM: DUT Receives (0x6C) WRITE_BURST - Data 0 Timeout" Tag="" Location=""', \
    "6.3.12.7": 'Name="6.3.12.7 CBM: DUT Receives (0x6C) WRITE_BURST - EOF Timeout" Tag="" Location=""', \
    "6.3.12.8": 'Name="6.3.12.8 CBM: DUT Receives (0x68) MSC_MSG - Data 0 Timeout" Tag="" Location=""', \
    "6.3.12.9": 'Name="6.3.12.9 CBM: DUT Receives (0x68) MSC_MSG - Data 1 Timeout" Tag="" Location=""', \
    "6.3.14.1": 'Name="6.3.14.1 CBM-Source: Source DUT Receives (0x64) SET_HPD Command" Tag="" Location=""', \
    "6.3.14.2": 'Name="6.3.14.2 CBM-Source: Source DUT Receives (0x65) CLR_HPD Command" Tag="" Location=""', \
    "6.3.15.1": 'Name="6.3.15.1 CBM-Sink: Sink DUT Sends (0x64) SET_HPD Command" Tag="" Location=""', \
    "6.3.15.2": 'Name="6.3.15.2 CBM-Sink: Sink DUT Sends (0x65) CLR_HPD Command" Tag="" Location=""', \
    "6.3.16.1": 'Name="6.3.16.1 CBM-Sink: Sink DUT Receives (0x64) SET_HPD Command" Tag="" Location=""', \
    "6.3.16.2": 'Name="6.3.16.2 CBM-Sink: Sink DUT Receives (0x65) CLR_HPD Command" Tag="" Location=""', \
    "6.3.18.1": 'Name="6.3.18.1 CBM-Source: DUT Issues DDC Short Read and Current Read" Tag="" Location=""', \
    "6.3.18.2": 'Name="6.3.18.2 CBM-Source: DUT Issues Regular DDC Read" Tag="" Location=""', \
    "6.3.18.3": 'Name="6.3.18.3 CBM-Source: DUT Issues DDC Segment Read" Tag="" Location=""', \
    "6.3.18.4": 'Name="6.3.18.4 CBM-Source: DUT Issues DDC Write" Tag="" Location=""', \
    "6.3.19.1": 'Name="6.3.19.1 CBM-Source: DUT Issues Short Read and Current" Tag="" Location=""', \
    "6.3.19.2": 'Name="6.3.19.2 CBM-Source: DUT Issues Regular Read" Tag="" Location=""', \
    "6.3.19.3": 'Name="6.3.19.3 CBM-Source: DUT Issues Segment Read" Tag="" Location=""', \
    "6.3.19.4": 'Name="6.3.19.4 CBM-Source: DUT Issues Write" Tag="" Location=""', \
    "6.3.21.1": 'Name="6.3.21.1 CBM-Sink: DUT Receives DDC Write" Tag="" Location=""', \
    "6.3.21.2": 'Name="6.3.21.2 CBM-Sink: DUT Receives DDC Current Read" Tag="" Location=""', \
    "6.3.21.3": 'Name="6.3.21.3 CBM-Sink: DUT Receives regular DDC Read" Tag="" Location=""', \
    "6.3.21.4": 'Name="6.3.21.4 CBM-Sink: DUT Receives DDC Segment Read; Segment Register Implemented" Tag="" Location=""', \
    "6.3.21.5": 'Name="6.3.21.5 CBM-Sink: DUT NACKs DDC Segment Read; Segment Register Not Implemented" Tag="" Location=""', \
    "6.3.22.1": 'Name="6.3.22.1 CBM-Sink: DUT Receives SOF, CONT" Tag="" Location=""', \
    "6.3.22.2": 'Name="6.3.22.2 CBM-Sink: DUT Receives DDC Write; Various Errs" Tag="" Location=""', \
    "6.3.22.3": 'Name="6.3.22.3 CBM-Sink: DUT Receives DDC Short Read and Current Read; Various Errs" Tag="" Location=""', \
    "6.4.3.3": 'Name="6.4.3.3 Observe: DUT Does Not Send New MHL3 CBUS Commands to MHL 2 Tester" Tag="" Location=""', \
    "6.4.3.4": 'Name="6.4.3.4 Observe: DUT Sends New MHL3 CBUS Command(s) to MHL 3 Tester" Tag="" Location=""', \
    "6.4.3.5": 'Name="6.4.3.5 Observe: Source DUT Device Implement Heartbeat" Tag="" Location=""', \
    "6.4.3.6": 'Name="6.4.3.6 Observe: Source DUT Reads Extended Device Capability Registers after it gets DCAP_RDY or DCAP_CHG" Tag="" Location=""', \
    "6.4.3.7": 'Name="6.4.3.7 Observe: Source DUT Reads Extended Device Capability Registers after it gets DCAP_RDY or DCAP_CHG" Tag="" Location=""', \
    "6.4.4.1": 'Name="6.4.4.1 Observe: Source DUT Notices Failures of oCBUS to eCBUS Transition " Tag="" Location=""', \
    "6.4.4.2": 'Name="6.4.4.2 Observe: Sink DUT Notices Failures of oCBUS to eCBUS Transition " Tag="" Location=""', \
    "6.4.4.3": 'Name="6.4.4.3 Observe: Source Heart Beat Disconnect" Tag="" Location=""', \
    "6.4.5.1": 'Name="6.4.5.1 Observe: Source DUT Writes MHL_VERSION_STAT and DCAP_RDY and XDEVCAP_SUPP" Tag="" Location=""', \
    "6.4.5.2": 'Name="6.4.5.2 Observe: Source DUT Sends MSC_MSG RAP (CBUS_MODE_UP)" Tag="" Location=""', \
    "6.4.5.3": 'Name="6.4.5.3 Observe: Source DUT Attemptes eCBUS-S Connection" Tag="" Location=""', \
    "6.4.5.4": 'Name="6.4.5.4 Observe: Source DUT first Tries eCBUS-D and then eCBUS-S" Tag="" Location=""', \
    "6.4.6.1": 'Name="6.4.6.1 Observe: Sink DUT writes MHL_VERSION_STAT and signals DCAP_RDY + XDEVCAP_SUPP" Tag="" Location=""', \
    "6.4.6.2": 'Name="6.4.6.2 Observe: Sink DUT receives MSC_MSG_RAP{CBUS_MODE_UP}" Tag="" Location=""', \
    "6.4.23.1": 'Name="6.4.23.1 Source receives RAPK{RESPONDER_BUSY} when it sends RAP{CBUS_MODE_UP}" Tag="" Location=""', \
    "6.6.1.1": 'Name="6.6.1.1 CBT-Source: Discovery; Sink Never Drives MHL+/- HIGH" Tag="" Location=""', \
    "6.6.1.2": 'Name="6.6.1.2 CBT-Source: Remove MHL+/- Pull-up for More than Glitch Reject Time" Tag="" Location=""', \
    "6.6.1.20": 'Name="6.6.1.20 RxSense Impedance Test" Tag="" Location=""' \
}

##For Astro 
#video_format = ['EIA720x480p@60' ,'EIA720x576p@50','EIA640x480p@60','EIA1280x720p@60','EIA1920x1080i@60', \
#                'EIA1440x480i@60','EIA1440x480p@60','EIA1280x720p@50','EIA1440x576i@50','EIA1440x576p@50',\
#                'EIA1920x1080p@24','EIA1920x1080p@25','EIA1920x1080p@30']
#pixel_encoding = ['RGB','4:2:2','4:4:4']
#video_format_pp = ['EIA1920x1080p@50','EIA1920x1080p@60']
#sample_size = [0,1]
#max_size = ['16','17','18','19','20','21','22','23','24']
#rcp_selection = []
#threed_video_format = ['3D 720p60 Top&Bot','3D 720p50 Top&Bot','3D 1080i60 Side_half','3D 1080i50 Side_half', '3D 1080p24 Top&Bot']
#threed_video_format_pp = ['3D 720p60 FramePack','3D 720p50 FramePack','3D 1080p24 FramePack']

video_format = ['480p60' ,'576p50','DMT0660','720p60','1080i30', \
                '480i2x30','480p2x60','720p50','1080i25','576i2x25',\
                '576p2x50','1080p24','1080p25','1080p30']
pixel_encoding = ['RGB','4:2:2','4:4:4']
video_format_pp = ['1080p@50','1080p@60']
sample_size = [0,1]
max_size = ['16','17','18','19','20','21','22','23','24']
rcp_selection = []
threed_video_format = ['3D 720p60 Top&Bot','3D 720p50 Top&Bot','3D 1080i60 Side_half','3D 1080i50 Side_half', '3D 1080p24 Top&Bot']
threed_video_format_pp = ['3D 720p60 FramePack','3D 720p50 FramePack','3D 1080p24 FramePack']

class cts(TestCase):
    
    def test_mhl2_source_explorer(self):
        self.resource = TestContextManager().getCurrentContext().resource
        xml_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) +r'\lib\simg\util\uts800\MHL2_CTS_PART1\Test Case'
        xml_file = xml_path + "\\CommonTestCase.xml"
        #xml_file = r'C:\husky\lib\simg\util\uts800\MHL2_CTS_PART1\Test Case\CommonTestCase.xml'
        print xml_file
        f = open(xml_file,'w')
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<CommonTest>\n')
        f.write('    <TestCase ID="'+self.item+'" '+testcases["6.3.1.1"]+ '/>\n')
        f.write('</CommonTest>\n')
        f.close()
        time.sleep(2)
        cts = mhl2_explorer(self.cdf_path)
        res = cts.test_mhl2_explorer()
        self.assertEquals(res, 0, "Return code should be \"0\" ")
        time.sleep(10)
        cf = ConfigParser.ConfigParser()
        cf.read(self.cdf_path)
        log_name = cf.get("SOURCE DEVICE DECLARATIONS", "CDF_SRC_CONNECT_MFR_NAME")  
        f = open(os.path.join(os.path.dirname(self.cdf_path),"Source_common_"+log_name+".txt"),'r')
        lines = f.readlines()
        f.close
        f1 = open(os.path.join(self.logdir,"test_logs.txt"),'a')
        actual_result = ""
        for line in lines:
            f1.write(line)
            if re.search("RESULT    :         PASS",line,re.I):
                actual_result = "PASS"
                break
        f1.close        
        self.assertEquals(actual_result, "PASS", "Keywords 'PASS' should be found in log")
    

    @parametrize("device", type=Mhl2Interface, fetch=parametrize.FetchType.LAZY)    
    def test_mhl2_analyzer(self):
        global actual_rcp_msg
        self.resource = TestContextManager().getCurrentContext().resource
        #IMAGE_2D="Acer1"
        IMAGE_2D="CheckBy6"
        iface ="HDMI"
        qd = QD882("172.16.131.250")
        av_source = self.subitem.split("]_[")[0].split("[")[1]
        print av_source
        if re.search("2D",self.subitem,re.I):
            #av_source = self.subitem.split("]_[")[0].split("[")[1]
            #print av_source
            structure, formats, color_space, color_depth = av_source.split('_')
            qd.load(iface, IMAGE_2D, "/card0/Library/formats/" + formats, color_space, color_depth)
        elif re.search("3D",self.subitem,re.I):
            flag, fmt, structure, color_space, color_depth, image = av_source.split('_')
            qd.load_3d(image, "/card0/Library/formats/"+fmt, structure, color_space, color_depth)
        elif re.search("audio",self.subitem,re.I):
            match = re.search("(audio)_(.*)Ch_(.*)_(.*)KHz", av_source, re.I)
            audio_channel_number = match.group(2)  # Number of channels (eg: 2, 6, 8)
            audio_format = match.group(3)  # Format (eg: LPCM, SPDIF, Dolby etc)
            audio_frequency = match.group(4)  # Sampling frequency (eg: 32, 44.1, 48, 88.2, 96, 176.4, 192)
            
            video_format = "720p60"
            video_color_space = "RGB"
            video_color_depth = "8"
            
            if audio_channel_number == "2":
                audio_type = "AudioLR"
            elif audio_channel_number == "6" or audio_channel_number == "8":
                audio_type = "Audio_Xf"
            else:
                raise ValueError("Unsupported channel number: %s" % audio_channel_number)
            
            qd.load_audio(iface,
                            audio_type,
                            "/card0/Library/formats/"+video_format,
                            video_color_space,
                            video_color_depth,
                            audio_frequency,
                            audio_channel_number)
        else:
            raise ValueError("Wrong subitem formats in xml!")
        time.sleep(5)
        
        cmd = self.subitem.split("]_[")[1].split("]")[0]
        print cmd
        
        cts = mhl2_analyzer(self.device_type)
        
        if re.search("RCP Transmitting",self.subitem,re.I):
            sp = self.subitem.find("Test_")
            rcp_code = self.subitem[sp+5:sp+9]
            
            def sendrcp():
                print 'RCP Code 0x'+rcp_code +' will be sent after 15 seconds'
                time.sleep(15)
                expect_rcp_msg = MscMessage(RCP, int(rcp_code,16))
                self.device.send_msc_message(expect_rcp_msg)
            
            t1 = Thread(target=sendrcp,args=())
            t1.start()
            
            res = cts.test_mhl2_analyzer(cmd,checklog=True)
            for i in range (2):
                if res == 0:
                    break;
                
                t1 = Thread(target=sendrcp,args=())
                t1.start()
                res = cts.test_mhl2_analyzer(cmd)
            self.assertEquals(res, 0, "Return code should be \"0\" ")    
                
        elif re.search("RCP Receiving",self.subitem,re.I):
            sp = self.subitem.find("Test_")
            ep = self.subitem.find("[2D")
            rcp_code = self.subitem[sp+5:ep]
            
            def receivercp():
                global flag1 
                flag1 = 0
                print 'DUT will try to receive RCP Code '+rcp_code
                time.sleep(15)
                actual_rcp_msg = self.device.recv_msc_message()
                actual_rcp_msg = str(actual_rcp_msg)
                #print 'Actual received msg='+actual_rcp_msg
                sp1 = self.subitem.find(")>")
                actual_rcp_code=actual_rcp_msg[30:sp1-1]
                print 'Actual received rcp='+actual_rcp_code
                if rcp_code == actual_rcp_code:
                    # If expected rcp code is received, finished test, if not, try three times
                    flag1 = 0
                    self.assertEquals(rcp_code, actual_rcp_code, "RCP Code "+rcp_code +" is received!")
                else:
                    print "=======expected rcp code is NOT received========="
                    flag1 = 1
            
            t1 = Thread(target=receivercp,args=())
            t1.start()
            res = cts.test_mhl2_analyzer(cmd,checklog=True)            
             
            for i in range(3):
                if flag1 == 0:
                    break;
                if i == 2:
                    self._fail("Expected rcp code"+rcp_code+ " is NOT received!")
                    #self.assertEquals(1, 0, "expected rcp code is NOT received!")
                    return
                t1 = Thread(target=receivercp,args=())
                t1.start()
                res = cts.test_mhl2_analyzer(cmd,checklog=True)
                time.sleep(1)
     
             
        elif re.search("UCP Transmitting",self.subitem,re.I):
            sp = self.subitem.find("Test_")
            ucp_code = self.subitem[sp+5:sp+9]            
            expect_ucp_msg = MscMessage(UCP, int(ucp_code,16))
            self.device.send_msc_message(expect_ucp_msg)
            time.sleep(3)
            res = cts.test_mhl2_analyzer(cmd,checklog=True)
            self.assertEquals(res, 0, "Return code should be \"0\" ")
        else:    
            res = cts.test_mhl2_analyzer(cmd,checklog=False)
            for i in range (2):
                #if not res == 0:
                #     res = cts.test_mhl2_analyzer(cmd)
                if res == 0:
                    break;
                res = cts.test_mhl2_analyzer(cmd)
            self.assertEquals(res, 0, "Return code should be \"0\" ")
        



    def test_mhl3_cts_part1(self):
        self.resource = TestContextManager().getCurrentContext().resource
        xml_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) +r'\lib\simg\util\uts800\MHL3_CTS_PART1'
        xml_file = xml_path + "\\test.xml"
        #xml_file = r'C:\husky\lib\simg\util\uts800\MHL3_CTS_PART1\test.xml'
        test_item = self.item.split("_")[0]
        sub_item = self.item.split("_")[1]
        f = open(xml_file,'w')
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<TestList>\n')
        f.write('<Test TestName="'+test_item+'" ParamIndex="'+sub_item+'" />\n')
        f.write('</TestList>\n')
        f.close()
        time.sleep(2)
        cts = mhl3(self.cdf_path,self.test_list)
        res = cts.test_mhl3_part1()
        self.assertEquals(res, "PASS", "Keywords 'PASS' should be found in log")    
        
if __name__ == '__main__':
    a = hdcp()
    a.test_receiver()