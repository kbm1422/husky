#!/usr/bin/python
# -*- coding: utf-8 -*-
#Access QD980 via Telnet

import telnetlib
import time
import re
import os
from ftplib import FTP

class TimingInfo():
    def __init__(self, ip, user, passwd):
            self.inited = False
            try:
                    self.session = FTP(ip, user, passwd)
                    print ('FTP: FTP session opened to ' + ip)
                    self.inited = True
            except:
                    print("ERROR: Unable to open a ftp connection with "+ip+": "+str(sys.exc_info()[0]) +str(sys.exc_info()[1]))
                    return
            return
        
    def upload(self, filepath, storepath):
            #self.session.login()
            f2 = open(storepath, 'wb')
            try:
                    self.session.retrbinary("RETR " + filepath, f2.write)
            except Exception:
                    print ("FTP: Error in uploading the remote file.")
                    return -1
            else:
                    print ("FTP: " + filepath + " successfully uploaded to " + storepath)
            f2.close()
            return 0
        
class VideoInfo():
    def __init__(self, host, username, password):
        self.host=host
        self.username=username
        self.password=password
        tn = telnetlib.Telnet(self.host, port=23, timeout=10)
        tn.set_debuglevel(2)
        
        tn.read_until('xpscope-4a login: ')
        tn.write(self.username + '\n')
        
        tn.read_until('Password: ')
        tn.write(self.password + '\n')
        self.tn=tn

    def sendcommand(self,command):
        self.tn.write(command+'\n' )

    def get_basic_video_info(self):
        self.tn.write("vsinfo"+'\n' )
        data = self.tn.read_until("Pixel Pack Phase")
        print "======== Basic Video Timing Info ======== \n"
        print data.split("\n")[41]        
        print data.split("\n")[42]
        print data.split("\n")[44]
        print data.split("\n")[46]
        print data.split("\n")[47]
        print data.split("\n")[48]
        
    def get_detail_video_info(self,mem_size="small"):
        self.tn.write("vsinfo"+'\n' )
        data = self.tn.read_until("Pixel Pack Phase")
      
        if mem_size == "small":        
            self.tn.write("pcap size 6%"+'\n' )
        elif  mem_size == "big":
            self.tn.write("pcap size 10%"+'\n' )
            
        self.tn.read_until('capture buffer size')
        time.sleep(0.5)

        self.tn.write("pcap mode all"+'\n' )
        self.tn.read_until('No filtering')
        time.sleep(0.5)
        self.tn.write("pcap start"+'\n' )
        self.tn.read_until('END: Capture complete')
        time.sleep(0.5)
        self.tn.write("pcap decode"+'\n' )
        self.tn.read_until('decode request complete')
        time.sleep(0.5)
        self.tn.write("pcap stat"+'\n' )
        self.tn.read_until('complete')
        time.sleep(0.5)
        self.tn.write("pcap timing"+'\n' )
        self.tn.read_until('type=112 complete')
        time.sleep(0.5)          
            
        data1 = self.tn.read_until(">")
        self.tn.close()
        
        timing = TimingInfo(self.host,self.username,self.password)
        log = "/home/qd/ptiming.log"
        
        storage = os.path.dirname(os.path.abspath(__file__)) + "\\ptiming.log"
        timing.upload(log,storage)
        
        time.sleep(3)
        lines = []
        f = open(storage, 'r')
        lines = f.readlines()
    
        Color_depth =""
        FORMAT_INFO = []
        ##[4K x 2K 25Hz]  2 [24 bits per pixel] 56.25     1  3840  2160  2250  5280     1     1    88 52800  1056     8     0 297.000
        ##     [1080p60] 16 [24 bits per pixel] 67.50     1  1920  1080  1125  2200     1     1    44 11000    88     4     0 148.500
        #3D#   [unknown] 34 [24 bits per pixel] 67.43     1  1920  2205  2250  2200     1     1    44 11000    88     4     0 148.351 
        V_FIELDS_INFO = []
        ##         [4K x 2K 25Hz][001:17425659129.220: 40000.052] 25.00 56.25 02250 02160 297.000 088 010 090 0000 [00:000:00]
        ## [1920x1080p 59.9/60Hz][001:682454917.990: 16666.688] 60.00 67.50 01125 01080 148.500 044 005 045 0000 [00:000:00]
        i=0
        for line in lines:
            line = line.strip()
            if re.search("VIDEO FORMAT:",line):
                Color_depth = lines[i+2].strip().split("]")[1].split("[")[1]
                FORMAT_INFO = lines[i+2].strip().split("]")[2].strip().split()
                print FORMAT_INFO
                ##['56.25',    '1',    '3840',    '2160',    '2250',    '5280',    '1',    '1',    '88',    '52800',    '1056',    '8',    '0',    '297.000']
                ##  ======0             ====2     =====3     =====4     =====5                    ======8               =====10   ======11         ========13
                ##  Hfreq              Hactive     Vactive    Vtotal     Htotal                     Hsync                Hfront    Vfront           TMDS Clock
            if re.search("CAPTURE V FIELDS INFO:",line):
                V_FIELDS_INFO = lines[i+2].split("]")[2].strip().split("[")[0].split()
                print V_FIELDS_INFO
                ##['25.00',   '56.25',   '02250',   '02160',   '297.000',   '088',   '010',   '090',   '0000']
                ## ======0   =======1    ======2    ======3     ======4     =====5    ====6    ====7    ====8
                ##  Vfreq      Hfreq      Vtotal    Vactive    TMDS Clock    Hsync    Vsync
                break
            i += 1
            
        print "\n======== Detail Video Timing Info ========"
        print data.split("\n")[41]  #Video Active:      
        print data.split("\n")[42]  #Video Total:
        #Hactive = data.split("\n")[41].split(":")[1].strip().split("x")[0]
        #Vactive = data.split("\n")[41].split(":")[1].strip().split("x")[1]
        #Htotal =  data.split("\n")[42].split(":")[1].strip().split("x")[0]
        #Vtotal =  data.split("\n")[42].split(":")[1].strip().split("x")[1]
        print data.split("\n")[44]  #Encryption:
        print data.split("\n")[46]  #Video Format:
        print data.split("\n")[47]  #Colorimetry:
        print data.split("\n")[48]  #RGB YCC Ind:
        RGB_YCC = str(data.split("\n")[48]).split("YCC Ind:")[1].strip()
        if re.search("YCbCr",RGB_YCC,re.I):
            RGB_YCC = RGB_YCC.split()[1]
        print "Color Depth:        " + Color_depth
        print "======"+ "Color Depth:" + Color_depth +" RGB YCC Ind:"+RGB_YCC 
        print "Hactive:            " + FORMAT_INFO[2]
        print "Htotal:             " + FORMAT_INFO[5]
        print "Hfront:             " + FORMAT_INFO[10]        
        print "Hfreq:              " + FORMAT_INFO[0]
        print "Hsync:              " + FORMAT_INFO[8]

        print "Vactive:            " + str(int(V_FIELDS_INFO[3])) ## or FORMAT_INFO[3]
        print "Vtotal:             " + str(int(V_FIELDS_INFO[2])) ## or FORMAT_INFO[4]
        print "Vfront:             " + FORMAT_INFO[11]
        print "Vfreq:              " + V_FIELDS_INFO[0]
        print "Vsync:              " + str(int(V_FIELDS_INFO[6]))
        
        print "TMDS Clock Freq:    " + FORMAT_INFO[13]
        Color_depth = Color_depth.split(" bit")[0]
        Colorimetry = "-".join(data.split("\n")[47].split()[1:])
        info1_0 =data.split("Format:")[1].split()[0]
        info1_1 =data.split("Format:")[1].split()[1].split("Hz")[0]
        info1_2 =data.split("Format:")[1].strip().split("VIC=")[1].split("]")[0]
        
        info1 = "Video_Format:" + info1_0+"_"+info1_1+"Hz_VIC="+info1_2 + " Color_Depth:" + Color_depth +" RGB_YCC:"+RGB_YCC
        info2 = " Hactive:" + FORMAT_INFO[2] + " Htotal:" + FORMAT_INFO[5]+" Hfront:" + FORMAT_INFO[10]+ " Hfreq:" + FORMAT_INFO[0]+" Hsync:"+ FORMAT_INFO[8]\
             +" Vactive:" + str(int(V_FIELDS_INFO[3])) +" Vtotal:" + str(int(V_FIELDS_INFO[2]))+" Vfront:" + FORMAT_INFO[11]+" Vfreq:" + V_FIELDS_INFO[0]+" Vsync:" + str(int(V_FIELDS_INFO[6]))\
             +" TMDS_Clock:" + FORMAT_INFO[13] + " Colorimetry:" + Colorimetry
        
        #print "Hactive:            " + Hactive
        #print "Htotal:             " + Htotal
        #print "Hfront:             " + FORMAT_INFO[10]        
        #print "Hfreq:              " + FORMAT_INFO[0]
        #print "Hsync:              " + FORMAT_INFO[8]
        #
        #print "Vactive:            " + Vactive
        #print "Vtotal:             " + Vtotal
        #print "Vfront:             " + FORMAT_INFO[11]
        #print "Vfreq:              " + V_FIELDS_INFO[0]
        #print "Vsync:              " + str(int(V_FIELDS_INFO[6]))
        #
        #print "TMDS Clock Freq:    " + FORMAT_INFO[13]
        #Color_depth = Color_depth.split(" bit")[0]
        #
        #info1_0 =data.split("Format:")[1].split()[0]
        #info1_1 =data.split("Format:")[1].split()[1].split("Hz")[0]
        #info1_2 =data.split("Format:")[1].strip().split("VIC=")[1].split("]")[0]
        #
        #info1 = "Video_Format:" + info1_0+"_"+info1_1+"Hz_VIC="+info1_2 + " Color_Depth:" + Color_depth +" RGB_YCC:"+RGB_YCC 
        #info2 = " Hactive:" + Hactive + " Htotal:" + Htotal+" Hfront:" + FORMAT_INFO[10]+ " Hfreq:" + FORMAT_INFO[0]+" Hsync:"+ FORMAT_INFO[8]\
        #     +" Vactive:" + Vactive +" Vtotal:" + Vtotal+" Vfront:" + FORMAT_INFO[11]+" Vfreq:" + V_FIELDS_INFO[0]+" Vsync:" + str(int(V_FIELDS_INFO[6]))\
        #     +" TMDS Clock:" + FORMAT_INFO[13]
        print str(info1)+str(info2)
        return info1+info2

#    
if __name__=="__main__":
    #host="172.16.131.189"
    host="172.16.132.244"
    username="qd"
    password="qd"
    qd980 = VideoInfo(host,username,password)
    raw_info = qd980.get_detail_video_info(mem_size="big")
    raw_info_list = raw_info.split()
    d = dict()
    for item in raw_info_list:
        if "RGB_YCC" in item:
            color_format = item.split(":")[1:]
            if color_format == "RGB":
                d['color_format'] = "RGB444"
            else:
                d['color_format'] = "YCbCr" + "".join(color_format)
        if "Color_Depth" in item:
            color_depth = int(item.split(":")[1]) / 3
            d['color_depth'] = color_depth
        if "Colorimetry" in item:
            colorimetry = item.split(":")[1]
            d['colorimetry'] = colorimetry

    print d


                                        