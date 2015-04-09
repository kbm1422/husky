#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from ctypes import byref
from simg.devadapter.wired.boston.Sii9777RxLib import *
from simg.devadapter.wired.boston import BostonDeviceAdapter
from simg.test.framework import TestCase, TestContextManager, parametrize
import time


class ParseBlocks():
    """
    Description:
        Some functions for parsing block0 and block1. As block1, there are some functions to parse each data block
        and each byte.
    Structure:
                             --- __init__
                            |
                            |---edid2block
                            |
                            |---parseBlock0
              ParseBlocks---|                                     ---parseVideoDataBlock
                            |                                    |
                            |---parseBlock1 --> parseDataBlock---|---parseAudioDataBlock
                            |                                    |
                            |                                     ---parseSpeakerAllocationDataBlock
                             --- __del__

    """
    def __init__(self, strEdid):
        self.strEdid = strEdid
        self.dicBlock0 = {}
        self.dicBlock1 = {}

    def __del__(self):
        self.dicBlock0.clear()
        self.dicBlock1.clear()

    def edid2block(self):
        """
        Description:
             parse an EDID string to blocks which saved in a dictionary.
        Input:
            strEdid, an EDID string passed by an instance of class ParseBlocks().
        Output:
            some log of debug level in log file.
        Return:
            dicBlocks, an dictionary contains 2 or 4 block items.
        Steps:
            1: determine it is 2-block EDID or 4-block EDID;
            2: get the first 128 bytes(length of the string is 256) for block0;
            3: get the second 128 bytes for block1;
            4: get the third 128 bytes for block2 if exists;
            5: get the fourth 128 bytes for block2 if exists.
        eg.
            strEdid = '00FFFFFFFFFFFF0034A93BC3010101010116...0203...'
            dicBlocks = {'block0': '00FFFFFFFFFFF...', 'block1': '0203...'}
        """
        dicBlocks = {}
        if len(self.strEdid) in (512, 1024):
            dicBlocks['block0'] = self.strEdid[0:256]      # first 128 bytes
            dicBlocks['block1'] = self.strEdid[256:512]    # second 128 bytes
            if len(self.strEdid) == 1024:
                logger.debug("this is 4 blocks EDID")
                dicBlocks['block2'] = self.strEdid[512:768]     # third 128 bytes
                dicBlocks['block3'] = self.strEdid[768:1024]    # fourth 128 bytes
            else:
                logger.debug("this is 2 blocks EDID")
        else:
            logger.error("error edid length: {0}\n current edid: {1}".format(len(self.strEdid), self.strEdid))
        return dicBlocks

    def parseBlock0(self, strBlock0):
        """
        Description:
            parse a string of block0 to a dictionary.
        Input:
            strBlock0, a string of block0.
        Output:
            None
        Return:
            dicBlock0, a dictionary of block0.
        Steps:
            None
        eg.
            strBlock0 = '00FFFFFFFFFFFF00...'
            dicBlock0 = {'Block 0 Header': '00FFFFFFFFFFFF00', 'Vendor and Product ID': ..., ...}
        """
        self.dicBlock0['Block 0 Header'] = strBlock0[0:16]    # 8 bytes
        self.dicBlock0['Vendor and Product ID'] = strBlock0[16:36]    # 8 bytes
        self.dicBlock0['EDID Structure Version and Revision'] = strBlock0[36:40]      # 2 bytes
        self.dicBlock0['Basic Display Parameters and Features'] = strBlock0[40:50]    # 5 bytes
        self.dicBlock0['Color Characteristics'] = strBlock0[50:70]     # 10 bytes
        self.dicBlock0['Established Timings'] = strBlock0[70:76]       # 3 bytes
        self.dicBlock0['Standard Timing ID 1-8'] = strBlock0[76:108]   # 16 bytes
        self.dicBlock0['First Detailed Timing Descriptor'] = strBlock0[108:144]    # 18 bytes
        self.dicBlock0['Second Detailed Timing Descriptor'] = strBlock0[144:180]    # 18 bytes
        self.dicBlock0['Monitor Descriptor Currently Mandatory'] = strBlock0[180:216]    # 18 bytes
        self.dicBlock0['Second Monitor Descriptor Currently Mandatory'] = strBlock0[216:252]    # 18 bytes
        self.dicBlock0['Extension Flag'] = strBlock0[252:256]    # 2 bytes
        return self.dicBlock0

    def parseBlock1(self, strBlock1):
        """
        Description:
            parse a string of strBlock1 to a dictionary.
        Input:
            strBlock1, a string of block1.
        Output:
            None
        Return:
            dicBlock1, a dictionary of block1.
        Steps:
            1: parse all in a fixed position, such as 'Tag and Revision', 'Number of Detailed Timing Descriptors',...
            2: revoke parseDataBlock to parse each data block.
            3: update dictionary to final dicBlock1.
        eg.
            strBlock0 = '020345F1...'
            dicBlock0 = {'Tag and Revision': '0203', 'Number of Detailed Timing Descriptors': ..., ...}
        """
        dicBlockTmp = {}
        dicBlockTmp.clear()

        dicBlockTmp['Tag and Revision'] = strBlock1[0:4]    # 2 bytes
        intTmpDtdOffset = 2 * int(strBlock1[4:6], 16)       # offset of DTD string(1 byte)

        # parse strEdid[6:8], 1 byte
        strTmp = bin(int(strBlock1[6:8], 16))[2:].zfill(8)
        dicBlockTmp['underscan support'] = strTmp[0:1]
        dicBlockTmp['audio support'] = strTmp[1:2]
        dicBlockTmp['YCbCr 444 support'] = strTmp[2:3]
        dicBlockTmp['YCbCr 422 support'] = strTmp[3:4]
        dicBlockTmp['Number of Detailed Timing Descriptors'] = int(strTmp[4:], 2)

        # parse Detailed Timing Descriptor
        for intIndex in range(dicBlockTmp['Number of Detailed Timing Descriptors']):
            dicBlockTmp['block1 NO{0} Detailed Timing Descriptor'.format(intIndex+1)] = \
                strBlock1[intTmpDtdOffset:(intTmpDtdOffset + 36)]

        # parse data block collection
        dicDataBlock = self.parseDataBlock(strBlock1, intTmpDtdOffset-1)

        # merge two dictionary
        self.dicBlock1 = dict(dicBlockTmp, **dicDataBlock)
        return self.dicBlock1

    @classmethod
    def parseDataBlock(cls, strBlock1, intEndPosDataBlock):
        """
        Description:
            parse each data block of block1, according Tag Codes of data block and Extended Tag Codes of data block.
        Input:
            strBlock1, a string of block1.
            intEndPosDataBlock, the end position of data block in string block1.
        Output:
            None
        Return:
            dicDataBlock, a dictionary of all data block.
        Steps:
            1: parse data block according mapDataBlockExtendedTagCodes dictionary;
            2: revoke parseVideoDataBlock to parse video data block;
            3: revoke parseAudioDataBlock to parse audio data block;
            4: revoke parseSpeakerAllocationDataBlock to parse speaker allocation data block;
            5: parse data block according mapDataBlockTagCodes dictionary.
        eg.
            strBlock1 = '020345F1...'
            intEndPosDataBlock = 45
            dicDataBlock = {'YCbCr 4:2:0 Video Data Block': ..., 'Vendor-Specific Data Block': ..., ...}
        """
        mapDataBlockTagCodes = {0: "Reserved",
                                1: "Audio Data Block",
                                2: "Video Data Block",
                                3: "Vendor-Specific Data Block",
                                4: "Speaker Allocation Data Block",
                                5: "VESA Display Transfer Characteristic Data Block",
                                6: "Reserved",
                                7: "Use Extended Tag"}
        mapDataBlockExtendedTagCodes = {0: "Video Capability Data Block",
                                        1: "Vendor-Specific Video Data Block",
                                        2: "VESA Display Device Data Block [81]",
                                        3: "VESA Video Timing Block Extension",
                                        4: "Reserved for HDMI Video Data Block",
                                        5: "Colorimetry Data Block",
                                        6: "Reserved for video-related blocks",
                                        13: "Video Format Preference Data Block",
                                        14: "YCbCr 4:2:0 Video Data Block",
                                        15: "YCbCr 4:2:0 Capability Map Data Block",
                                        16: "Reserved for CEA Miscellaneous Audio Fields",
                                        17: "Vendor-Specific Audio Data Block",
                                        18: "Reserved for HDMI Audio Data Block",
                                        19: "Reserved for audio-related blocks",
                                        32: "InfoFrame Data Block",
                                        255: "Reserved"}
        dicDataBlock = {}
        dicDataBlock.clear()

        intIndex = 8    # offset of data block start
        while intIndex <= intEndPosDataBlock:
            strTmp = bin(int(strBlock1[intIndex:(intIndex + 2)], 16))[2:].zfill(8)
            intTagCode = int(strTmp[0:3], 2)
            intLengthBlock = 2 * int(strTmp[3:], 2)    # length of data block string
            if intLengthBlock != 0:
                if mapDataBlockTagCodes[intTagCode] == "Use Extended Tag":
                    intExtendedTagCode = int(strBlock1[(intIndex+2):(intIndex+4)], 16)
                    if 5 < intExtendedTagCode < 13:
                        keyDataBlock = "Reserved for video-related blocks"
                    elif 18 < intExtendedTagCode < 32:
                        keyDataBlock = "Reserved for audio-related blocks"
                    elif 32 < intExtendedTagCode < 256:
                        keyDataBlock = "Reserved"
                    else:
                        keyDataBlock = mapDataBlockExtendedTagCodes[intExtendedTagCode]
                    dicDataBlock[keyDataBlock] = strBlock1[intIndex:(intIndex + 2 + intLengthBlock)]
                elif mapDataBlockTagCodes[intTagCode] == "Video Data Block":
                    dicDataBlock[mapDataBlockTagCodes[intTagCode]] = \
                        cls.parseVideoDataBlock(strBlock1[(intIndex+2):(intIndex + 2 + intLengthBlock)])
                elif mapDataBlockTagCodes[intTagCode] == "Audio Data Block":
                    dicDataBlock[mapDataBlockTagCodes[intTagCode]] = \
                        cls.parseAudioDataBlock(strBlock1[(intIndex+2):(intIndex + 2 + intLengthBlock)])
                elif mapDataBlockTagCodes[intTagCode] == "Speaker Allocation Data Block":
                    dicDataBlock[mapDataBlockTagCodes[intTagCode]] = \
                        cls.parseSpeakerAllocationDataBlock(strBlock1[(intIndex+2):(intIndex + 2 + intLengthBlock)])
                else:
                    dicDataBlock[mapDataBlockTagCodes[intTagCode]] = strBlock1[intIndex:(intIndex + 2 + intLengthBlock)]
            intIndex += (intLengthBlock + 2)
        return dicDataBlock

    @classmethod
    def parseVideoDataBlock(cls, strVideoDataBlock):
        """
        Description:
            parse each byte of video data block string according video data block vic dictionary.
        Input:
            strVideoDataBlock, a string of video data block.
        Output:
            None
        Return:
            listVideoDataBlock, a list of all parsed video data block.
        Steps:
            None
        eg.
            strVideoDataBlock = '4D901F...'
            listVideoDataBlock = ['640x480p 59.94Hz/60Hz 4:3', '1920x1080p 25Hz 16:9', ...]
        """
        mapVideoDataBlockVic = {1: "640x480p 59.94Hz/60Hz 4:3", 2: "720x480p 59.94Hz/60Hz 4:3",
                                3: "720x480p 59.94Hz/60Hz 16:9", 4: "1280x720p 59.94Hz/60Hz 16:9",
                                5: "1920x1080i 59.94Hz/60Hz 16:9", 6: "720(1440)x480i 59.94Hz/60Hz 4:3",
                                7: "720(1440)x480i 59.94Hz/60Hz 16:9", 8: "720(1440)x240p 59.94Hz/60Hz 4:3",
                                9: "720(1440)x240p 59.94Hz/60Hz 16:9", 10: "2880x480i 59.94Hz/60Hz 4:3",
                                11: "2880x480i 59.94Hz/60Hz 16:9", 12: "2880x240p59.94Hz/60Hz 4:3",
                                13: "2880x240p 59.94Hz/60Hz 16:9", 14: "1440x480p 59.94Hz/60Hz 4:3",
                                15: "1440x480p 59.94Hz/60Hz 16:9", 16: "1920x1080p 59.94Hz/60Hz 16:9",
                                17: "720x576p 50Hz 4:3", 18: "720x576p 50Hz 16:9",
                                19: "1280x720p 50Hz 16:9", 20: "1920x1080i 50Hz 16:9",
                                21: "720(1440)x576i 50Hz 4:3", 22: "720(1440)x576i 50Hz 16:9",
                                23: "720(1440)x288p 50Hz 4:3", 24: "720(1440)x288p 50Hz 16:9",
                                25: "2880x576i 50Hz 4:3", 26: "2880x576i 50Hz 16:9",
                                27: "2880x288p 50Hz 4:3", 28: "2880x288p 50Hz 16:9",
                                29: "1440x576p 50Hz 4:3", 30: "1440x576p 50Hz 16:9",
                                31: "1920x1080p 50Hz 16:9", 32: "1920x1080p 23.98Hz/24Hz 16:9",
                                33: "1920x1080p 25Hz 16:9", 34: "1920x1080p 29.97Hz/30Hz 16:9",
                                35: "2880x480p 59.94Hz/60Hz 4:3", 36: "2880x480p 59.94Hz/60Hz 16:9",
                                37: "2880x576p 50Hz 4:3", 38: "2880x576p 50Hz 16:9",
                                39: "1920x1080i (1250 total) 50Hz 16:9", 40: "1920x1080i 100Hz 16:9",
                                41: "1280x720p 100Hz 16:9", 42: "720x576p 100Hz 4:3",
                                43: "720x576p 100Hz 16:9", 44: "720(1440)x576i 100Hz 4:3",
                                45: "720(1440)x576i 100Hz 16:9", 46: "1920x1080i 119.88/120Hz 16:9",
                                47: "1280x720p 119.88/120Hz 16:9", 48: "720x480p 119.88/120Hz 4:3",
                                49: "720x480p 119.88/120Hz 16:9", 50: "720(1440)x480i 119.88/120Hz 4:3",
                                51: "720(1440)x480i 119.88/120Hz 16:9", 52: "720x576p 200Hz 4:3",
                                53: "720x576p 200Hz 16:9", 54: "720(1440)x576i 200Hz 4:3",
                                55: "720(1440)x576i 200Hz 16:9", 56: "720x480p 239.76/240Hz 4:3",
                                57: "720x480p 239.76/240Hz 16:9", 58: "720(1440)x480i 239.76/240Hz 4:3",
                                59: "720(1440)x480i 239.76/240Hz 16:9", 60: "1280x720p 23.98Hz/24Hz 16:9",
                                61: "1280x720p 25Hz 16:9", 62: "1280x720p 29.97Hz/30Hz 16:9",
                                63: "1920x1080p 119.88/120Hz 16:9", 64: "1920x1080p 100Hz 16:9",
                                65: "1280x720p 23.98Hz/24Hz 64:27^6", 66: "1280x720p 25Hz 64:27^6",
                                67: "1280x720p 29.97Hz/30Hz 64:27^6", 68: "1280x720p 50Hz 64:27^6",
                                69: "1280x720p 59.94Hz/60Hz 64:27^6", 70: "1280x720p 100Hz 64:27^6",
                                71: "1280x720p 119.88/120Hz 64:27^6", 72: "1920x1080p 23.98Hz/24Hz 64:27^6",
                                73: "1920x1080p 25Hz 64:27^6", 74: "1920x1080p 29.97Hz/30Hz 64:27^6",
                                75: "1920x1080p 50Hz 64:27^6", 76: "1920x1080p 59.94Hz/60Hz 64:27^6",
                                77: "1920x1080p 100Hz 64:27^6", 78: "1920x1080p 119.88/120Hz 64:27^6",
                                79: "1680x720p 23.98Hz/24Hz 64:27^6", 80: "1680x720p 25Hz 64:27^6",
                                81: "1680x720p 29.97Hz/30Hz 64:27^6", 82: "1680x720p 50Hz 64:27^6",
                                83: "1680x720p 59.94Hz/60Hz 64:27^6", 84: "1680x720p 100Hz 64:27^6",
                                85: "1680x720p 119.88/120Hz 64:27^6", 86: "2560x1080p 23.98Hz/24Hz 64:27^6",
                                87: "2560x1080p 25Hz 64:27^6", 88: "2560x1080p 29.97Hz/30Hz 64:27^6",
                                89: "2560x1080p 50Hz 64:27^6", 90: "2560x1080p 59.94Hz/60Hz 64:27^6",
                                91: "2560x1080p 100Hz 64:27^6", 92: "2560x1080p 119.88/120Hz 64:27^6",
                                93: "3840x2160p 23.98Hz/24Hz 16:9", 94: "3840x2160p 25Hz 16:9",
                                95: "3840x2160p 29.97Hz/30Hz 16:9", 96: "3840x2160p 50Hz 16:9",
                                97: "3840x2160p 59.94Hz/60Hz 16:9", 98: "4096x2160p 23.98Hz/24Hz 256:135",
                                99: "4096x2160p 25Hz 256:135", 100: "4096x2160p 29.97Hz/30Hz 256:135",
                                101: "4096x2160p 50Hz 256:135", 102: "4096x2160p 59.94Hz/60Hz 256:135",
                                103: "3840x2160p 23.98Hz/24Hz 64:27^6", 104: "3840x2160p 25Hz 64:27^6",
                                105: "3840x2160p 29.97Hz/30Hz 64:27^6", 106: "3840x2160p 50Hz 64:27^6",
                                107: "3840x2160p 59.94Hz/60Hz 64:27^6", 108: "Reserved for the Future",
                                0: "No Video Identification Code Available"}

        listVideoDataBlock = []
        i = 0
        while i < len(strVideoDataBlock):
            intVic = int(strVideoDataBlock[i:(i+2)], 16)
            if 107 < intVic < 256:
                listVideoDataBlock.append(mapVideoDataBlockVic[108])
            else:
                listVideoDataBlock.append(mapVideoDataBlockVic[intVic])
            i += 2
        return listVideoDataBlock

    @classmethod
    def parseAudioDataBlock(cls, strAudioDataBlock):
        """
        Description:
            parse each byte of audio data block string.
        Input:
            strAudioDataBlock, a string of audio data block.
        Output:
            None
        Return:
            listAudioDataBlock, a list of all parsed audio data block.
        Steps:
            1: parse byte1
            2: parse byte2
            3: parse byte3, when strAudioFormatCode != 0001, do not parse it.
        eg.
            strAudioDataBlock = '090707'
            listAudioDataBlock = ['L-PCM', '32 kHz 44.1 kHz 48 kHz', ...]
        """
        mapAudioFormatCodeByte1 = {'0001': "L-PCM", '0010': "AC-3", '0011': "MPEG-1", '0100': "MP3", '0101': "MPEG2",
                                   '0110': "AAC LC", '0111': "DTS", '1000': "ATRAC", '1001': "One Bit Audio",
                                   '1010': "Enhanced AC-3", '1011': "DTS-HD", '1100': "MAT", '1101': "DST",
                                   '1110': "WMA Pro", '0000': "Reserved", '1111': "Reserved for Audio Format 15"}
        mapMaxChannelNumByte1 = {'001': "2 channels", '010': "3 channels", '011': "4 channels", '100': "5 channels",
                                 '101': "6 channels", '110': "7 channels", '111': "8 channels"}
        mapSampleFrequencyByte2 = {0: "32 kHz", 1: "44.1 kHz", 2: "48 kHz", 3: "88.2 kHz", 4: "96 kHz", 5: "176.4 kHz",
                                   6: "192 kHz"}
        mapSampleSizeByte3 = {0: "16 bit", 1: "20 bit", 2: "24 bit"}

        listAudioDataBlock = []
        # parse byte1
        strByte1 = bin(int(strAudioDataBlock[0:2], 16))[2:].zfill(8)
        strAudioFormatCode = strByte1[1:5]
        listAudioDataBlock.append(mapAudioFormatCodeByte1[strAudioFormatCode])
        strMaxChannelNum = strByte1[5:8]
        listAudioDataBlock.append(mapMaxChannelNumByte1[strMaxChannelNum])

        # parse byte2
        strByte2 = bin(int(strAudioDataBlock[2:4], 16))[2:].zfill(8)
        strSampleFrequencyTmp = ""
        for i in range(7):
            if strByte2[i+1] == '1':
                strSampleFrequencyTmp += (mapSampleFrequencyByte2[6-i] + " ")
        listAudioDataBlock.append(strSampleFrequencyTmp)

        # parse byte3
        strByte3 = bin(int(strAudioDataBlock[4:6], 16))[2:].zfill(8)
        if strAudioFormatCode == '0001':
            strSampleSizeTmp = ""
            for i in range(3):
                if strByte3[i+5] == '1':
                    strSampleSizeTmp += (mapSampleSizeByte3[i] + " ")
            listAudioDataBlock.append(strSampleSizeTmp)
        else:
            listAudioDataBlock.append("strByte3: "+strByte3)    # need to do detail parse
        return listAudioDataBlock

    @classmethod
    def parseSpeakerAllocationDataBlock(cls, strSpeakerAllocationDataBlock):
        """
        Description:
            parse each byte of speaker allocation data block string.
        Input:
            strSpeakerAllocationDataBlock, a string of speaker allocation data block.
        Output:
            None
        Return:
            listSpeakerAllocationDataBlock, a list of all speaker allocation data block.
        Steps:
            1: parse byte1
            2: parse byte2
        eg.
            strAudioDataBlock = '010000'
            listAudioDataBlock = ['FL/FR LFE...']
        """
        mapSpeakerAllocationDataBlockByte1 = {0: "FL/FR", 1: "LFE", 2: "FC", 3: "RL/RR", 4: "RC", 5: "FLC/FRC",
                                              6: "RLC/RRC", 7: "FLW/FRW"}
        mapSpeakerAllocationDataBlockByte2 = {0: "FLH/FRH", 1: "TC", 2: "FCH"}
        listSpeakerAllocationDataBlock = []

        # parse byte1
        strByte1 = bin(int(strSpeakerAllocationDataBlock[0:2], 16))[2:].zfill(8)
        strSpeakerAllocationDataBlockTmp = ""
        for i in range(8):
            if strByte1[i] == '1':
                strSpeakerAllocationDataBlockTmp += (mapSpeakerAllocationDataBlockByte1[7-i] + " ")

        # parse byte2
        strByte2 = bin(int(strSpeakerAllocationDataBlock[2:4], 16))[2:].zfill(8)
        for i in range(3):
            if strByte2[i] == '1':
                strSpeakerAllocationDataBlockTmp += (mapSpeakerAllocationDataBlockByte2[7-i] + " ")
        listSpeakerAllocationDataBlock.append(strSpeakerAllocationDataBlockTmp)
        return listSpeakerAllocationDataBlock


@parametrize("device", type=BostonDeviceAdapter, fetch=parametrize.FetchType.LAZY)
@parametrize("rx_port", type=int, default=SII9777_RX_PORT__0)
@parametrize("offset", type=int, default=0)
@parametrize("length", type=int, default=256)
class EDIDTestCase(TestCase):
    def setUp(self):
        resource = TestContextManager.current_context().resource
        self.qd = resource.avproducer
        self.tv = resource.avconsumer

    def tearDown(self):
        pass

    # TODO(Two ways to get native EDID):
    # TODO 1. Connect a switch to control boston to do power cycle.
    # TODO 2. Only test once, get native EDID first, then set to True to get TV EDID.
    def get_edid_from_API(self, boolReplicate):
        """
        Description:
            get EDID string from api.
        Input:
            rx_port
            offset, EDID offset.
            length, EDID length.
            boolReplicate, set for getting EDID from RX or from TV.
        Output:
            None
        Return:
            strApiEdid, a string of EDID.
        Steps:
            1. revoke Sii9777EdidReplicateEnableGet to get boolReplicate;
            2: revoke Sii9777EdidReplicateEnableSet to set boolReplicate when needs;
            3: revoke Sii9777EdidGet to get EDID from fixed port;
            4: convert int array to hex string.
        eg.
            strApiEdid = '00FFFFFFFFFFFF004...'
        """
        pbOnGet = bool_t()
        with self.device.lock:
            retcodeGet = Sii9777EdidReplicateEnableGet(self.device.drv_instance, byref(pbOnGet))
        self.assertEquals(retcodeGet, 0, "Sii9777EdidReplicateEnableGet return code should be SII_RETVAL__SUCCESS")

        pbOnSet = bool_t(boolReplicate)
        if pbOnGet.value != pbOnSet.value:
            if boolReplicate:
                with self.device.lock:
                    retcode0 = Sii9777EdidReplicateEnableSet(self.device.drv_instance, byref(pbOnSet))
                self.assertEquals(retcode0, 0, "Sii9777EdidReplicateEnableSet retcode should be SII_RETVAL__SUCCESS")
            else:
                self.fail("Must power cycle boston when change boolReplicate from True to False!!!")
                # logger.error("Must power cycle boston when change boolReplicate from True to False!!!")

        pData = (uint8_t * self.length)()
        with self.device.lock:
            retcode1 = Sii9777EdidGet(self.device.drv_instance, Sii9777RxPort_t(self.rx_port), uint16_t(self.offset),
                                      pData, self.length)
        self.assertEquals(retcode1, 0, "Sii9777EdidGet return code should be SII_RETVAL__SUCCESS")

        # convert int array to hex string
        strApiEdid = ""
        for i in range(len(pData)):
            strApiEdid += hex(pData[i])[2:].upper().zfill(2)
        return strApiEdid

    def get_edid_from_qd(self):
        """
        Description:
            revoke QD interface to get EDID string from QD.
        Input:
            None
        Output:
            None
        Return:
            strQdEdid, a string of EDID.
        Steps:
            None
        eg.
            strQdEdid = '00FFFFFFFFFFFF004...'
        """
        time.sleep(5)
        strQdEdid = self.qd.capture_edid()
        return strQdEdid

    def get_edid_from_tv(self):
        """
        Get Edid from edid.ini
        """
        strTvEdid = self.tv.edid
        return strTvEdid

    def compare_block(self, blockNo, dicBlockBase, dicBlockTest):
        """
        Description:
            compare two parsed dictionary of block1 or block0.
        Input:
            blockNo, which block to compare.
            dicBlockBase, block dictionary which EDID gotten from QD.
            dicBlockTest, block dictionary which EDID gotten from API.
        Output:
            None
        Return:
            None
        Steps:
            1. when the value of block dictionary is a list, compare each item of the list;
            2. if not in 1, just compare each value of block dictionary directly.
        eg.
            None
        """
        for strKeyBase in dicBlockBase:
            if isinstance(dicBlockBase.get(strKeyBase), list):
                for i in range(len(dicBlockBase.get(strKeyBase))):
                    self.assertEquals(dicBlockBase.get(strKeyBase)[i], dicBlockTest.get(strKeyBase)[i],
                                      "{0}: {1} should include {2}, actually include {3}"
                                      .format(blockNo, strKeyBase, dicBlockBase.get(strKeyBase)[i], dicBlockTest.
                                              get(strKeyBase)[i]))
            else:
                self.assertEquals(dicBlockBase.get(strKeyBase), dicBlockTest.get(strKeyBase),
                                  "{0}: {1} should be {2}, actual value is {3}"
                                  .format(blockNo, strKeyBase, dicBlockBase.get(strKeyBase), dicBlockTest.get(
                                      strKeyBase)))

    def edidTest(self, boolReplicate):
        """
        Description:
            To test EDID by calling those functions listed upon.
        Input:
            None
        Output:
            None
        Return:
            None
        Steps:
            1. get EDID from API and QD;
            2. create a instance of ParseBlocks which input EDID gotten from API, then parse EDID string to block
               dictionary, then parse block0 and
               block1 separately.
            3. create a instance of ParseBlocks which input EDID gotten from QD, then parse EDID string to block
               dictionary, then parse block0 and block1 separately.
            4. compare block0 and block1 of QD and API EDID.
        eg.
            None
        """
        strApiEdid = self.get_edid_from_API(boolReplicate)
        strQdEdid = self.get_edid_from_qd()

        logger.debug("parsing API EDID...")
        instanceApiEdidParse = ParseBlocks(strApiEdid)
        dicApiBlocks = instanceApiEdidParse.edid2block()
        dicApiBlock0 = instanceApiEdidParse.parseBlock0(dicApiBlocks['block0'])
        dicApiBlock1 = instanceApiEdidParse.parseBlock1(dicApiBlocks['block1'])

        logger.debug("parsing QD EDID...")
        instanceQdEdidParse = ParseBlocks(strQdEdid)
        dicQdBlocks = instanceQdEdidParse.edid2block()
        dicQdBlock0 = instanceQdEdidParse.parseBlock0(dicQdBlocks['block0'])
        dicQdBlock1 = instanceQdEdidParse.parseBlock1(dicQdBlocks['block1'])

        # compare
        self.compare_block('block0', dicQdBlock0, dicApiBlock0)
        self.compare_block('block1', dicQdBlock1, dicApiBlock1)

    def testRxEdid(self):
        """
        Description:
            Revoke edidTest to test RX EDID.
        Input:
            None
        Output:
            None
        Return:
            None
        Steps:
            None
        eg.
            None
        """
        logger.debug("Starting RX EDID test......")
        self.edidTest(False)
        logger.debug("End of RX EDID test.")

    def testTvEdid(self):
        """
        Description:
            Revoke edidTest to test TV EDID.
        Input:
            None
        Output:
            None
        Return:
            None
        Steps:
            None
        eg.
            None
        """
        logger.debug("Starting TV EDID test......")
        self.edidTest(True)
        logger.debug("End of TV EDID test.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s %(thread)-5d [%(levelname)-8s] - %(message)s'
    )

