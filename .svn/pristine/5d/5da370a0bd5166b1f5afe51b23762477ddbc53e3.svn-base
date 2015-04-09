#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module is revision version based on XieLin script on testing formats.
"""

import telnetlib
import time
import re
import os
from ftplib import FTP


class TimingInfo(object):
    def __init__(self, ip, user, _password):
        self.inited = False
        try:
            self.session = FTP(ip, user, _password)
            print ('FTP: FTP session opened to ' + ip)
            self.inited = True
        except IOError:
            print("ERROR: Unable to open a ftp connection with " + ip + ": " + str(sys.exc_info()[0]) + str(
                sys.exc_info()[1]))
            raise

    def upload(self, filepath, destpath):
        with open(destpath, 'wb') as f:
            try:
                self.session.retrbinary("RETR " + filepath, f.write)
            except ftplib.all_errors:
                print ("FTP: Error in uploading the remote file.")
                raise
            print ("FTP: " + filepath + " successfully uploaded to " + destpath)


class VideoInfo():
    def __init__(self, _host, _user, _pass):
        self.host = _host
        self.username = _user
        self.password = _pass
        self.tn = telnetlib.Telnet(self.host, port=23, timeout=10)
        self.tn.set_debuglevel(2)

        self.tn.read_until('xpscope-4a login: ')
        self.tn.write(self.username + '\n')

        self.tn.read_until('Password: ')
        self.tn.write(self.password + '\n')


    def sendcommand(self, command):
        self.tn.write(command + '\n')

    def get_basic_video_info(self):
        self.tn.write("vsinfo" + '\n')
        data = self.tn.read_until("Pixel Pack Phase")
        print "======== Basic Video Timing Info ======== \n"
        print data.split("\n")[41]
        print data.split("\n")[42]
        print data.split("\n")[44]
        print data.split("\n")[46]
        print data.split("\n")[47]
        print data.split("\n")[48]

    def get_detail_video_info(self, mem_size="small"):
        self.tn.write("vsinfo" + '\n')
        data = self.tn.read_until("Pixel Pack Phase")

        if mem_size == "small":
            self.tn.write("pcap size 6%" + '\n')
        elif mem_size == "big":
            self.tn.write("pcap size 10%" + '\n')

        self.tn.read_until('capture buffer size')
        time.sleep(0.5)

        self.tn.write("pcap mode all" + '\n')
        self.tn.read_until('No filtering')
        time.sleep(0.5)
        self.tn.write("pcap start" + '\n')
        self.tn.read_until('END: Capture complete')
        time.sleep(0.5)
        self.tn.write("pcap decode" + '\n')
        self.tn.read_until('decode request complete')
        time.sleep(0.5)
        self.tn.write("pcap stat" + '\n')
        stat = self.tn.read_until('complete')

        time.sleep(0.5)
        self.tn.write("pcap timing" + '\n')
        self.tn.read_until('type=112 complete')
        time.sleep(0.5)

        data1 = self.tn.read_until(">")
        self.tn.close()

        timing = TimingInfo(self.host, self.username, self.password)
        log = "/home/qd/ptiming.log"

        storage = os.path.dirname(os.path.abspath(__file__)) + "\\ptiming.log"
        timing.upload(log, storage)

        time.sleep(3)
        lines = []
        f = open(storage, 'r')
        lines = f.readlines()

        Color_depth = ""
        FORMAT_INFO = []
        V_FIELDS_INFO = []
        i = 0
        for line in lines:
            line = line.strip()
            if re.search("VIDEO FORMAT:", line):
                Color_depth = lines[i + 2].strip().split("]")[1].split("[")[1]
                FORMAT_INFO = lines[i + 2].strip().split("]")[2].strip().split()
                print FORMAT_INFO
                """
                ['56.25',    '1',    '3840',    '2160',    '2250',    '5280',    '1',    '1',    '88',    '52800',    '1056',    '8',    '0',    '297.000']
                ======0             ====2     =====3     =====4     =====5                    ======8               =====10   ======11         ========13
                Hfreq              Hactive     Vactive    Vtotal     Htotal                     Hsync                Hfront    Vfront           TMDS Clock
                """
            if re.search("CAPTURE V FIELDS INFO:", line):
                V_FIELDS_INFO = lines[i + 2].split("]")[2].strip().split("[")[0].split()
                print V_FIELDS_INFO
                ##['25.00',   '56.25',   '02250',   '02160',   '297.000',   '088',   '010',   '090',   '0000']
                ## ======0   =======1    ======2    ======3     ======4     =====5    ====6    ====7    ====8
                ##  Vfreq      Hfreq      Vtotal    Vactive    TMDS Clock    Hsync    Vsync
                break
            i += 1
        time.sleep(0.01)
        print "\n======== Detail Video Timing Info ========"
        print data.split("\n")[41]  # Video Active:
        print data.split("\n")[42]  # Video Total:
        print data.split("\n")[44]  # Encryption:
        print data.split("\n")[46]  # Video Format:
        print data.split("\n")[47]  # Colorimetry:

        if "Ext Clrimetry" in data:
            if "vsinfo" not in data:
                print data.split("\n")[47]  # Ext Colorimetry:
                print "$" * 100
                print data.split("\n")
                print "$" * 100
                ext_color = data.split("\n")[47].split(":")[1].strip()
                ext_color = ext_color.replace(" ", "_")
                print ext_color
                print data.split("\n")[48]  # RGB YCC Ind:
                RGB_YCC = str(data.split("\n")[48]).split("YCC Ind:")[1].strip()
                if re.search("YCbCr", RGB_YCC, re.I):
                    RGB_YCC = RGB_YCC.split()[1]
            else:
                print data.split("\n")[48]  # Ext Colorimetry:
                print "$" * 100
                print data.split("\n")
                print "$" * 100
                ext_color = data.split("\n")[48].split(":")[1].strip()
                ext_color = ext_color.replace(" ", "_")
                print ext_color
                print data.split("\n")[49]  # RGB YCC Ind:
                RGB_YCC = str(data.split("\n")[49]).split("YCC Ind:")[1].strip()
                if re.search("YCbCr", RGB_YCC, re.I):
                    RGB_YCC = RGB_YCC.split()[1]
        elif "vsinfo" in data:
            print data.split("\n")[48]
            print "#" * 100
            print data.split("\n")
            print "#" * 100
            RGB_YCC = str(data.split("\n")[48]).split("YCC Ind:")[1].strip()
            if re.search("YCbCr", RGB_YCC, re.I):
                RGB_YCC = RGB_YCC.split()[1]
            ext_color = ""
        else:
            print data.split("\n")[47]
            print "#" * 100
            print data.split("\n")
            print "#" * 100
            RGB_YCC = str(data.split("\n")[47]).split("YCC Ind:")[1].strip()
            if re.search("YCbCr", RGB_YCC, re.I):
                RGB_YCC = RGB_YCC.split()[1]
            ext_color = ""
        print "Color Depth:        " + Color_depth
        print "======" + "Color Depth:" + Color_depth + " RGB YCC Ind:" + RGB_YCC
        print "Hactive:            " + FORMAT_INFO[2]
        print "Htotal:             " + FORMAT_INFO[5]
        print "Hfront:             " + FORMAT_INFO[10]
        print "Hfreq:              " + FORMAT_INFO[0]
        print "Hsync:              " + FORMAT_INFO[8]

        print "Vactive:            " + str(int(V_FIELDS_INFO[3]))  ## or FORMAT_INFO[3]
        print "Vtotal:             " + str(int(V_FIELDS_INFO[2]))  ## or FORMAT_INFO[4]
        print "Vfront:             " + FORMAT_INFO[11]
        print "Vfreq:              " + V_FIELDS_INFO[0]
        print "Vsync:              " + str(int(V_FIELDS_INFO[6]))

        print "TMDS Clock Freq:    " + FORMAT_INFO[13]
        Color_depth = Color_depth.split(" bit")[0]
        if not "vsinfo" in data:
            Colorimetry = "-".join(data.split("\n")[46].split()[1:])
        else:
            Colorimetry = "-".join(data.split("\n")[47].split()[1:])
        info1_0 = data.split("Format:")[1].split()[0]
        info1_1 = data.split("Format:")[1].split()[1].split("Hz")[0]
        info1_2 = data.split("Format:")[1].strip().split("VIC=")[1].split("]")[0]

        info1 = "Video_Format:" + info1_0 + "_" + info1_1 + "Hz_VIC=" + info1_2 + " Color_Depth:" + Color_depth + " RGB_YCC:" + RGB_YCC
        info2 = " Hactive:" + FORMAT_INFO[2] + " Htotal:" + FORMAT_INFO[5] + " Hfront:" + FORMAT_INFO[10] + " Hfreq:" + \
                FORMAT_INFO[0] + " Hsync:" + FORMAT_INFO[8] \
                + " Vactive:" + str(int(V_FIELDS_INFO[3])) + " Vtotal:" + str(int(V_FIELDS_INFO[2])) + " Vfront:" + \
                FORMAT_INFO[11] + " Vfreq:" + V_FIELDS_INFO[0] + " Vsync:" + str(int(V_FIELDS_INFO[6])) \
                + " TMDS_Clock:" + FORMAT_INFO[13] + " Colorimetry:" + Colorimetry + " Ext_Color:" + ext_color

        print str(info1) + str(info2)
        return info1 + info2

if __name__ == "__main__":
    #host="172.16.131.189"
    host = "172.16.131.189"
    username = "qd"
    password = "qd"
    qd980 = VideoInfo(host, username, password)
    raw_info = qd980.get_detail_video_info(mem_size="big")
    raw_info_list = raw_info.split()
    d = dict()
    for item in raw_info_list:
        if "RGB_YCC" in item:
            color_format = item.split(":")[1:]
            if color_format[0] == "RGB":
                d['color_format'] = "RGB444"
            else:
                d['color_format'] = "YCbCr" + "".join(color_format)
        if "Color_Depth" in item:
            color_depth = int(item.split(":")[1]) / 3
            d['color_depth'] = color_depth

        if "Ext_Color" in item:
            ext_color = item.split(":")[1].strip()
            d['ext_color'] = ext_color

        if "Colorimetry" in item:
            colorimetry = item.split(":")[1]
            d['colorimetry'] = colorimetry

    if d["colorimetry"] == "extended" and d["ext_color"]:
        d["colorimetry"] = d["ext_color"]

    print d

