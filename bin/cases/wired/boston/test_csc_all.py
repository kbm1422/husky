#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This Module is the test suites covering all of scenarios in color space conversion of SII products.

/**
* @brief Color Format
*
* Color Format includes color space, colorimetry, and range (Full vs. Limited).
*/
typedef enum
{
    SII9777_CLR_FMT__NO_DATA,                //!< No information or default selection
    SII9777_CLR_FMT__RGB_F,                  //!< RGB Full Range
    SII9777_CLR_FMT__RGB_L,                  //!< RGB Limited Range
    SII9777_CLR_FMT__YC601_F,                //!< YCbCr ITU-601 Full Range
    SII9777_CLR_FMT__YC601_L,                //!< YCbCr ITU-601 Limited Range
    SII9777_CLR_FMT__YC709_F,                //!< YCbCr ITU-709 Full Range
    SII9777_CLR_FMT__YC709_L,                //!< YCbCr ITU-709 Limited Range
    SII9777_CLR_FMT__XV601,                  //!< xvYCC ITU-601
    SII9777_CLR_FMT__XV709,                  //!< xvYCC ITU-709
    SII9777_CLR_FMT__YC2020_CL,              //!< YCbCr BT-2020 Constant Luminance
    SII9777_CLR_FMT__YC2020_NCL,             //!< YCbCr BT-2020 Non-Constant Luminance
} Sii9777ClrFmt_t;

/**
* @brief Chroma sampling
*/
typedef enum
{
    SII9777_CR_SMPL__NO_DATA,                //!< No information or default selection
    SII9777_CR_SMPL__444,                    //!< 4:4:4
    SII9777_CR_SMPL__422,                    //!< 4:2:2
    SII9777_CR_SMPL__420,                    //!< 4:2:0
} Sii9777CrSmpl_t;

/**
* @brief Bit Depth
*/
typedef enum
{
    SII9777_BIT_DEPTH__NO_DATA,              //!< No information or default selection
    SII9777_BIT_DEPTH__8,                    //!< 8 bit
    SII9777_BIT_DEPTH__10,                   //!< 10 bit
    SII9777_BIT_DEPTH__12,                   //!< 12 bit
} Sii9777BitDepth_t;

"""

import logging
logger = logging.getLogger(__name__)

from simg.devadapter.wired.boston import BostonDeviceAdapter
from simg.devadapter.wired.boston.Sii9777RxLib import *
from inspect import currentframe, getframeinfo
from simg.test.framework import TestCase, parametrize, TestContextManager, skip
from simg.util.avproducer.astro import VG876


@parametrize("device", type=BostonDeviceAdapter, fetch=parametrize.FetchType.LAZY)
class GeneralCSCTestCase(TestCase):
    def setUp(self):
        pStatus = Sii9777PixFmtConv_t()
        with self.device.lock:
            pEnable = bool_t(True)
            convset_return = Sii9777PixelFormatConversionSet(self.device.drv_instance, pEnable)
            assert convset_return == 0, "The instruction for format conversion set is not done properly."

        with self.device.lock:
            query_ret = Sii9777PixelFormatConversionQuery(self.device.drv_instance, pStatus)
            assert query_ret == 0, "The instruction for format conversion query is not done properly."
            assert pStatus.value == 1, "The format conversion should be enabled."

        with self.device.lock:
            pConversionStatus = bool_t(False)
            Sii9777PixelFormatConversionGet(self.device.drv_instance, pConversionStatus)
            assert pConversionStatus.value is True, "The pixel format conversion is not enabled."

    def tearDown(self):
        with self.device.lock:
            pConversionStatus = bool_t(False)
            Sii9777PixelFormatConversionGet(self.device.drv_instance, pConversionStatus)

        with self.device.lock:
            pEnable = bool_t(False)
            convset_return = Sii9777PixelFormatConversionSet(self.device.drv_instance, pEnable)
            assert convset_return == 0, "The instruction for format conversion set is not done properly."

    def csc_helper(self, color_format, chroma_sampling, bit_depth):
        with self.device.lock:
            clrFmt = Sii9777ClrFmt_t(color_format)
            crSmpl = Sii9777CrSmpl_t(chroma_sampling)
            bitDepth = Sii9777BitDepth_t(bit_depth)
            pPixFmt = Sii9777PixFmt_t(clrFmt, crSmpl, bitDepth)
            opfs = Sii9777OutputPixelFormatSet(self.device.drv_instance, pPixFmt)
            assert opfs == 0, "The instruction for output pixel format set is not done properly."

    def convert_YCbCr422BT709(self):
        self.csc_helper(SII9777_CLR_FMT__YC709_F, SII9777_CR_SMPL__422, SII9777_BIT_DEPTH__8)

    def convert_YCbCr444BT709(self):
        self.csc_helper(SII9777_CLR_FMT__YC709_F, SII9777_CR_SMPL__444, SII9777_BIT_DEPTH__8)

    def convert_YCbCr422BT2020(self):
        self.csc_helper(SII9777_CLR_FMT__YC2020_NCL, SII9777_CR_SMPL__422, SII9777_BIT_DEPTH__8)

    def convert_YCbCr444BT2020(self):
        self.csc_helper(SII9777_CLR_FMT__YC2020_NCL, SII9777_CR_SMPL__444, SII9777_BIT_DEPTH__8)

    def convert_xvYCC422BT709(self):
        self.csc_helper(SII9777_CLR_FMT__XV709, SII9777_CR_SMPL__422, SII9777_BIT_DEPTH__8)

    def convert_xvYCC444BT709(self):
        self.csc_helper(SII9777_CLR_FMT__XV709, SII9777_CR_SMPL__444, SII9777_BIT_DEPTH__8)

    def convert_RGB444LR(self):
        self.csc_helper(SII9777_CLR_FMT__RGB_L, SII9777_CR_SMPL__444, SII9777_BIT_DEPTH__8)

    def convert_RGB444FR(self):
        self.csc_helper(SII9777_CLR_FMT__RGB_F, SII9777_CR_SMPL__444, SII9777_BIT_DEPTH__8)

    def get_csc_info(self):
        from simg.util.avproducer.infoframe import VideoInfo

        host = "172.16.131.189"
        username = "qd"
        password = "qd"
        qd980 = VideoInfo(host, username, password)
        raw_info = qd980.get_detail_video_info(mem_size="big")
        print raw_info
        raw_info_list = raw_info.split()
        d = dict()
        for item in raw_info_list:
            if "RGB_YCC" in item:
                color_format = item.split(":")[1:]
                if color_format[0].strip() == "RGB":
                    d['color_format'] = "RGB444"
                else:
                    d['color_format'] = "YCbCr" + "".join(color_format)
            if "Color_Depth" in item:
                color_depth = int(item.split(":")[1]) / 3
                d['color_depth'] = color_depth
            if "Colorimetry" in item:
                colorimetry = item.split(":")[1]
                d['colorimetry'] = colorimetry
            if "Ext_Color" in item:
                ext_color = item.split(":")[1].strip()
                d["ext_color"] = ext_color

        if d["colorimetry"] == "extended" and d["ext_color"]:
            d["colorimetry"] = d["ext_color"]

        try:
            del d["ext_color"]
        except Exception:
            pass

        return d


class CSCRGB444FullRangeTestCase(GeneralCSCTestCase):
    def setUp(self):
        super(CSCRGB444FullRangeTestCase, self).setUp()
        self.vg876 = VG876("172.16.131.188")
        self.vg876.set_csc_params(ext_color="AdobeRGB", avi_range="Full Range", basic_color="No Data")
        self.vg876.load_video('EIA4096x2160p@30', 'Color Bar 100/100-H', 'RGB', '8-bit')

    def tearDown(self):
        super(CSCRGB444FullRangeTestCase, self).tearDown()
        print "Cheers! " + self.__class__.__name__ + "::" + self._testMethodName + " Done!"

    def test_YCbCr422BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr422BT709()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "ITU709-[6]"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr444BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr444BT709()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "ITU709-[6]"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr422BT2020_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr422BT2020()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "BT.2020_YCC_5"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr444BT2020_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr444BT2020()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "BT.2020_YCC_5"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_xvYCC422BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_xvYCC422BT709()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "xvYCC709_1"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_xvYCC444BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_xvYCC444BT709()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "xvYCC709_1"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_RGB444LR_conversion(self):
        """
        TODO: It's hard to capture Limited Range in 980. We may have to run the test case in manual mode.
        """
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444LR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))


class CSCRGB444LimitedRangeTestCase(GeneralCSCTestCase):
    def setUp(self):
        super(CSCRGB444LimitedRangeTestCase, self).setUp()
        self.vg876 = VG876("172.16.131.188")
        self.vg876.set_csc_params(ext_color="AdobeRGB", avi_range="Limited Range", basic_color="No Data")
        self.vg876.load_video('EIA4096x2160p@30', 'Color Bar 100/100-H', 'RGB', '8-bit')

    def tearDown(self):
        super(CSCRGB444LimitedRangeTestCase, self).tearDown()
        print self.__class__.__name__ + "::" + self._testMethodName + "Done!"

    def test_YCbCr422BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr422BT709()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "ITU709-[6]"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr444BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr444BT709()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "ITU709-[6]"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr422BT2020_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr422BT2020()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "BT.2020_YCC_5"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr444BT2020_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr444BT2020()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "BT.2020_YCC_5"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_xvYCC422BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_xvYCC422BT709()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "xvYCC709_1"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_xvYCC444BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_xvYCC444BT709()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "xvYCC709_1"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_RGB444FR_conversion(self):
        """
        TODO: it's hard to capture Full Range information in 980. We may have to run this test case in
        manual mode.
        """
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444FR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))


class CSCYCbCr444BT709TestCase(GeneralCSCTestCase):
    def setUp(self):
        super(CSCYCbCr444BT709TestCase, self).setUp()
        self.vg876 = VG876("172.16.131.188")
        self.vg876.set_csc_params(ext_color="AdobeRGB", avi_range="Limited Range")
        self.vg876.load_video('EIA4096x2160p@30', 'Color Bar 100/100-H', 'YCbCr444', '8-bit')

    def tearDown(self):
        super(CSCYCbCr444BT709TestCase, self).tearDown()
        print self.__class__.__name__ + "::" + self._testMethodName + "Done!"

    def test_RGB444FR_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444FR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_RGB444LR_conversion(self):
        """
        TODO: The LIMITED RANGE is hard to be captured in 980. We may have to run this test case in manual
        mode.
        """
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444LR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr422BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr422BT709()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "ITU709-[6]"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_xvYCC444BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_xvYCC444BT709()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "xvYCC709_1"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))


class CSCYCbCr444BT2020TestCase(GeneralCSCTestCase):
    def setUp(self):
        super(CSCYCbCr444BT2020TestCase, self).setUp()
        self.vg876 = VG876("172.16.131.188")
        self.vg876.set_csc_params(ext_color="AdobeRGB", avi_range="Limited Range", basic_color="Extend")
        self.vg876.load_video('EIA4096x2160p@30', 'Color Bar 100/100-H', 'YCbCr444', '8-bit')

    def tearDown(self):
        super(CSCYCbCr444BT2020TestCase, self).tearDown()
        print self.__class__.__name__ + "::" + self._testMethodName + "Done!"

    def test_RGB444FR_conversion(self):
        """
        TODO: Full Range is hard to be captured in 980. We may have to run this test case in manual mode.
        """
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444FR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_RGB444LR_conversion(self):
        """
        TODO: Limited Range is hard to be captured in 980. We may have to run this test case in manual mode.
        """
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444LR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr422BT2020_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr422BT2020()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "BT.2020_YCC_5"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_xvYCC444BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_xvYCC444BT709()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "xvYCC709_1"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))


class CSCYCbCr422BT709TestCase(GeneralCSCTestCase):
    def setUp(self):
        super(CSCYCbCr422BT709TestCase, self).setUp()
        self.vg876 = VG876("172.16.131.188")
        self.vg876.set_csc_params(ext_color="AdobeRGB", avi_range="Limited Range")
        self.vg876.load_video('EIA4096x2160p@30', 'Color Bar 100/100-H', 'YCbCr422', '8-bit')

    def tearDown(self):
        super(CSCYCbCr422BT709TestCase, self).tearDown()
        print self.__class__.__name__ + "::" + self._testMethodName + "Done!"

    def test_RGB444FR_conversion(self):
        """
        TODO: It's hard to capture Full Range in 980. We may have to run this test case in manual mode.
        """
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444FR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_RGB444LR_conversion(self):
        """
        TODO: It's hard to capture Limited Range in 980. We may have to run this test case in manual mode.
        """
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444LR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr444BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr444BT709()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "ITU709-[6]"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_xvYCC422BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_xvYCC422BT709()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "xvYCC709_1"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))


class CSCYCbCr422BT2020TestCase(GeneralCSCTestCase):
    def setUp(self):
        super(CSCYCbCr422BT2020TestCase, self).setUp()
        self.vg876 = VG876("172.16.131.188")
        self.vg876.set_csc_params(ext_color="ITU-BT2020YCC", avi_range="Limited Range", basic_color="Extend")
        self.vg876.load_video('EIA4096x2160p@30', 'Color Bar 100/100-H', 'YCbCr422', '8-bit')

    def tearDown(self):
        super(CSCYCbCr422BT2020TestCase, self).tearDown()
        print self.__class__.__name__ + "::" + self._testMethodName + "Done!"

    def test_RGB444FR_conversion(self):
        """
        TODO: It's hard to capture Full Range in 980. We may have to run this test case in manual mode.
        """
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444FR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_RGB444LR_conversion(self):
        """
        TODO: It's hard to capture Limited Range in 980. We may have to run this test case in manual mode.
        """
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_RGB444LR()
        expect_csc_info = {"color_format": "RGB444", "color_depth": 8, "colorimetry": "no-data"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr444BT2020_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr444BT2020()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "BT.2020_YCC_5"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_xvYCC422BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_xvYCC422BT709()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "xvYCC709_1"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))


@skip("YCbCr420 is not supported by astro right now. We have to skip the testing for this situation.")
class CSCYCbCr420BT709TestCase(GeneralCSCTestCase):
    def setUp(self):
        super(CSCYCbCr420BT709TestCase, self).setUp()
        self.vg876 = VG876("172.16.131.188")
        self.vg876.set_csc_params(ext_color="AdobeRGB", avi_range="Limited Range")
        self.vg876.load_video('EIA4096x2160p@30', 'Color Bar 100/100-H', 'YCbCr420', '8-bit')

    def tearDown(self):
        super(CSCYCbCr420BT709TestCase, self).tearDown()
        print self.__class__.__name__ + "::" + self._testMethodName + "Done!"

    def test_YCbCr422BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr422BT709()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "ITU709-[6]"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr444BT709_conversion(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr444BT709()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "ITU709-[6]"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))


@skip("YCbCr420 is not supported by astro right now. We have to skip the testing for this situation.")
class CSCYCbCr420BT2020TestCase(GeneralCSCTestCase):
    def setUp(self):
        super(CSCYCbCr420BT2020TestCase, self).setUp()
        self.vg876 = VG876("172.16.131.188")
        self.vg876.set_csc_params(ext_color="ITU-BT2020YCC", avi_range="Limited Range", basic_color="Extend")
        self.vg876.load_video('EIA4096x2160p@30', 'Color Bar 100/100-H', 'YCbCr420', '8-bit')

    def tearDown(self):
        super(CSCYCbCr420BT2020TestCase, self).tearDown()
        print self.__class__.__name__ + "::" + self._testMethodName + "Done!"

    def test_YCbCr422BT2020(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr422BT2020()
        expect_csc_info = {"color_format": "YCbCr422", "color_depth": 8, "colorimetry": "BT.2020_YCC_5"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))

    def test_YCbCr444BT2020(self):
        self.name = self.__class__.__name__ + "::" + getframeinfo(currentframe())[2]
        self.convert_YCbCr422BT2020()
        expect_csc_info = {"color_format": "YCbCr444", "color_depth": 8, "colorimetry": "BT.2020_YCC_5"}
        real_csc_info = self.get_csc_info()
        self.assertDictEqual(expect_csc_info, real_csc_info,
                             "The real color space %s should be same as the expected %s after Boston conversion." % (
                                 real_csc_info, expect_csc_info))
