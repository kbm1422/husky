#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


import re
import time
import sys
import socket
import telnetlib


class QD882(object):
    prompt = "tffs0>"       # Prompt string on the QD
    QD_IMAGE = "Acer1"      # Default image used
    SAVE_IMAGE = "Acer1"
    PRE_IAMGE = ""
    CUR_IMAGE = "Acer1"     # Default status for current image

    def __init__(self, host, port=23):
        """Initialise the communication with QD, given its IP address"""
        self.inited = False
        
        if not host.strip():
            raise ValueError("Supplied IP address is blank")

        # Trim any leading zeros in the IP. Eg: Convert 010.005.060.208 to 10.5.60.208
        k = dict()
        b = re.match("(.*)\.(.*)\.(.*)\.(.*)", host)
        for i in range(1, 5):
            k[i] = b.group(i).lstrip('0')
            if not k[i]:
                k[i] = '0'
        host = k[1]+"."+k[2]+"."+k[3]+"."+k[4]
        logger.debug("The IP address of the QD is "+host)
        self.tn = telnetlib.Telnet()
        try:
            self.tn.open(host, port)
        except socket.error:
            logger.exception("ERROR: Unable to open a telnet connection with %s", host)
            raise
        
        resp = self.tn.read_until(self.prompt, 3)
        if re.search(self.prompt, str(resp)):
            # Reset the generator (soft-Reset)
            if self.send_cmd("*RST") == 0:
                return
            # Enable HDMI-H interface
            if self.send_cmd("XVSI 4") == 0:
                return
            # Enable Hot plug bypass. If HPD bypass is disabled, sometimes
            # even though the HPD signal is enabled, QD does not sent out video
            if self.send_cmd("HPBG 1") == 0:
                return

            if self.load("HDMI", self.QD_IMAGE, "/tffs0/Library/formats/1080p59", "RGB", "8") == 0:
                return
            if self.send_cmd("ALLU") == 0:
                return
            
            self.inited = True
            return
        else:
            logger.debug("Unable to see the prompt "+self.prompt)
            return

    def query_idn(self):
        """Query the identification string of the QD"""

        self.tn.write("*IDN?\n")
        resp = self.tn.expect([self.prompt], 3)
        return resp[2]

    def send_cmd(self, cmd):
        """Send the command cmd to the QD"""

        RETRY_COUNT = 3    

        #Retry the command upto 3 times
        for count in range(0, RETRY_COUNT):
            # Clear the buffers by reading out the data
            self.tn.read_very_eager()
            
            logger.debug("Attempt"+str(count+1)+": Sending "+cmd+" to the QD...")
            self.tn.write(cmd+"\n")
            if cmd == "ALLU":
                timeout = 15
            elif cmd == "PDAX:VIEW":
                timeout = 20
            elif cmd == "*RST" or "*CLS":
                timeout = 5
            elif re.search("FILE:SCREENCAP", cmd, re.I):
                timeout = 15
            else:
                timeout = 1
            resp = self.tn.expect([self.prompt], timeout)

            if (not resp[1]) or (re.search("error", str(resp[2]), re.I)):
                logger.debug("Response: "+str(resp[1])+str(resp[2]))
                continue
            logger.debug("Response: "+str(resp[1])+str(resp[2]))
            if cmd == "PDAX:NERR?":
                res = resp[2]
                return res
            return 1

        #If the code gets here, it means all the retries failed
        return 0

    def send_cmd_longtime(self, cmd):
        """Send the command cmd to the QD"""

        RETRY_COUNT = 3    

        #Retry the command upto 3 times
        for count in range(0, RETRY_COUNT):
            # Clear the buffers by reading out the data
            self.tn.read_very_eager()
            
            logger.debug("Attempt"+str(count+1)+": Sending "+cmd+" to the QD...")
            self.tn.write(cmd+"\n")
            if cmd == "ALLU":
                timeout = 20
            elif cmd == "*RST":
                timeout = 5
            else:
                timeout = 1

            resp = self.tn.expect([self.prompt], timeout)
            
            if (not resp[1]) or (re.search("error", str(resp[2]), re.I)):
                logger.debug("Response: "+str(resp[1])+str(resp[2]))
                continue
            logger.debug("Response: "+str(resp[1])+str(resp[2]))
            return 1

        #If the code gets here, it means all the retries failed
        return 0
        
    def back_2d(self):
        """Switch QD from 3D mode to 2D mode"""
        if self.send_cmd("*RST") == 0:
            return
        if self.send_cmd("HPBG 1") == 0:
            return
        if self.send_cmd("X3DM 0") == 0:
            return

    def avmute(self, val):
        """Enable and disable AVMute"""
        if self.send_cmd("MUTE "+val) == 0:
            return 0
        time.sleep(10)
        
    def reset(self):
        """Reset QD"""
        if self.send_cmd("*RST") == 0:
            return 0
        time.sleep(1)

    def load(self, iface, image, fmt, cspace, cdepth):
        """Loads the supplied image, format, color space and color depth on the QD"""
        self.CUR_IMAGE = image
        if iface == "DVI":
            # Enable HDMI-D interface
            logger.debug("Setting HDMI-D interface (XVSI 3)...")
            if self.send_cmd("XVSI 3") == 0:
                return 0
        else:
            # Enable HDMI-H interface
            logger.debug("Setting HDMI-H interface (XVSI 4)...")
            if self.send_cmd("XVSI 4") == 0:
                return 0
            
        logger.debug("Setting the image to " + image + " ...")
        if self.send_cmd("IMGL "+image) == 0:
            return 0
        
        logger.debug("Setting the analog video signal type to 0...")
        if self.send_cmd("AVST 0") == 0:
            return 0

        logger.debug("Setting the format " + fmt + "...")
        if self.send_cmd("FMTL "+fmt) == 0:
            return 0
        
        logger.debug("Setting the color space to " + cspace + "...")
        if cspace == "RGB":
            logger.debug("Setting the DVST to 10...")
            if self.send_cmd("DVST 10") == 0:
                return 0
            
            logger.debug("Setting the DVSM to 0...")
            if self.send_cmd("DVSM 0") == 0:
                return 0
            
        elif cspace == "444":
            logger.debug("Setting the DVST to 15...")
            if self.send_cmd("DVST 15") == 0:
                return 0

            logger.debug("Setting the DVSM to 4...")
            if self.send_cmd("DVSM 4") == 0:
                return 0
        elif cspace == "422":
            logger.debug("Setting the DVST to 15...")
            if self.send_cmd("DVST 15") == 0:
                return 0

            logger.debug("Setting the DVSM to 2...")
            if self.send_cmd("DVSM 2") == 0:
                return 0
        else:
            logger.debug("ERROR: Unknown Color space: " + cspace)
            return 0

        if cdepth == "8":
            logger.debug("Setting the NBPC to 8...")
            if self.send_cmd("NBPC 8") == 0:
                return 0
            logger.debug("Setting the PELD to 32...")
            if self.send_cmd("PELD 32") == 0:
                return 0
        elif cdepth == "10":
            logger.debug("Setting the NBPC to 10...")
            if self.send_cmd("NBPC 10") == 0:
                return 0
            logger.debug("Setting the PELD to 32...")
            if self.send_cmd("PELD 32") == 0:
                return 0
        elif cdepth == "12":
            logger.debug("Setting the NBPC to 12...")
            if self.send_cmd("NBPC 12") == 0:
                return 0
            logger.debug("Setting the PELD to 32...")
            if self.send_cmd("PELD 32") == 0:
                return 0
        else:
            logger.debug("ERROR: Unknown color depth: " + cdepth)

        #time.sleep(1)
        logger.debug("Sending the ALLU command...")
        if self.send_cmd("ALLU") == 0:
            return 0
        
        return 1
                
    def load_3d(self, image, fmt, struc, cspace, cdepth):
        """Loads the supplied image, format, structure on the QD"""
        self.CUR_IMAGE = image
        #For QD's reason, need set interface to HDMI-D to send SBSF first, set it to HDMI-H again after ALLU.
        if re.match("SBSF", struc, re.I):
            logger.debug("Setting HDMI-D interface (XVSI 3)...")
            if self.send_cmd("XVSI 3") == 0:
                return 0
        else:
            logger.debug("Setting HDMI-H interface (XVSI 4)...")
            if self.send_cmd("XVSI 4") == 0:
                return 0
    
        time.sleep(1)
        
        logger.debug("Setting the image to " + image + " ...")
        if self.send_cmd("IMGL "+"/card0/library/userdata/"+image+".bmp") == 0:
            return 0
        time.sleep(3)
        
        logger.debug("Setting the format " + fmt + "...")
        if self.send_cmd("FMTL "+fmt) == 0:
            return 0
        time.sleep(3)
        
        logger.debug("Setting the structure to " + struc + "...")
        if struc == "TP":
            logger.debug("Setting the X3DM to 16...")
            if self.send_cmd("X3DM 1 6") == 0:
                return 0        
            
        elif struc == "FP":
            logger.debug("Setting the X3DM to 10...")
            if self.send_cmd("X3DM 1 0") == 0:
                return 0

        elif struc == "LALT":
            logger.debug("Setting the X3DM to 12...")
            if self.send_cmd("X3DM 1 2") == 0:
                return 0

        elif struc == "SBSF":
            logger.debug("Setting the X3DM to 13...")
            if self.send_cmd("X3DM 1 3") == 0:
                return 0

        elif struc == "HHEE":
            logger.debug("Setting the X3DM to 183...")
            if self.send_cmd("X3DM 1 8 3") == 0:
                return 0

        elif struc == "HHEO":
            logger.debug("Setting the X3DM to 182...")
            if self.send_cmd("X3DM 1 8 2") == 0:
                return 0

        elif struc == "HHOE":
            logger.debug("Setting the X3DM to 181...")
            if self.send_cmd("X3DM 1 8 1") == 0:
                return 0

        elif struc == "HHOO":
            logger.debug("Setting the X3DM to 180...")
            if self.send_cmd("X3DM 1 8 0") == 0:
                return 0
            
        elif struc == "HQEE":
            logger.debug("Setting the X3DM to 187...")
            if self.send_cmd("X3DM 1 8 7") == 0:
                return 0

        elif struc == "HQEO":
            logger.debug("Setting the X3DM to 186...")
            if self.send_cmd("X3DM 1 8 6") == 0:
                return 0

        elif struc == "HQOE":
            logger.debug("Setting the X3DM to 185...")
            if self.send_cmd("X3DM 1 8 5") == 0:
                return 0

        elif struc == "HQOO":
            logger.debug("Setting the X3DM to 184...")
            if self.send_cmd("X3DM 1 8 4") == 0:
                return 0

        else:
            logger.debug("ERROR: Unknown structure: " + struc)

        time.sleep(3)
        
        logger.debug("Setting the color space to " + cspace + "...")
        if cspace == "RGB":
            logger.debug("Setting the DVST to 10...")
            if self.send_cmd("DVST 10") == 0:
                return 0
            
            logger.debug("Setting the DVSM to 0...")
            if self.send_cmd("DVSM 0") == 0:
                return 0
            
        elif cspace == "444":
            logger.debug("Setting the DVST to 15...")
            if self.send_cmd("DVST 15") == 0:
                return 0

            logger.debug("Setting the DVSM to 4...")
            if self.send_cmd("DVSM 4") == 0:
                return 0
        elif cspace == "422":
            logger.debug("Setting the DVST to 15...")
            if self.send_cmd("DVST 15") == 0:
                return 0

            logger.debug("Setting the DVSM to 2...")
            if self.send_cmd("DVSM 2") == 0:
                return 0
        else:
            logger.debug("ERROR: Unknown Color space: " + cspace)
            return 0
        time.sleep(2)

        if cdepth == "8":
            logger.debug("Setting the NBPC to 8...")
            if self.send_cmd("NBPC 8") == 0:
                return 0
            logger.debug("Setting the PELD to 32...")
            if self.send_cmd("PELD 32") == 0:
                return 0
        elif cdepth == "10":
            logger.debug("Setting the NBPC to 10...")
            if self.send_cmd("NBPC 10") == 0:
                return 0
            logger.debug("Setting the PELD to 32...")
            if self.send_cmd("PELD 32") == 0:
                return 0
        elif cdepth == "12":
            logger.debug("Setting the NBPC to 12...")
            if self.send_cmd("NBPC 12") == 0:
                return 0
            logger.debug("Setting the PELD to 32...")
            if self.send_cmd("PELD 32") == 0:
                return 0
        else:
            logger.debug("ERROR: Unknown color depth: " + cdepth)
        time.sleep(2)
        logger.debug("Sending the ALLU command...")

        #The QD cannot responde any command after load and use the 3D SBSF tree image,
        #so always configure failed when receiving ALLU cmd

        if self.send_cmd_longtime("ALLU") == 0:
            return 0
        logger.debug("sending ALLU with long time")
        #QD usually configure failure when sending SBSF structure, so send X3DM 1 3 again make sure QD can configure successfully
        if re.match("SBSF", struc,re.I):
            time.sleep(3)
            logger.debug("Configure QD to SBSF structure...")
            if self.send_cmd("FMTL "+fmt) == 0:
                return 0
            time.sleep(2)
            if self.send_cmd("X3DM 1 3") == 0:
                return 0
            time.sleep(2)
            if self.send_cmd_longtime("ALLU") == 0:
                return 0
            time.sleep(8)
            logger.debug("Setting HDMI-H interface (XVSI 4)...")
            if self.send_cmd("XVSI 4") == 0:
                return 0
            time.sleep(1)
            if self.send_cmd_longtime("ALLU") == 0:
                return 0
        return 1                

    def load_audio(self, iface, image, fmt, cspace, cdepth, afreq="48", ach="2"):
        """Loads the supplied audio image and sets the appropriate rendition to give out
        the specified audio sampling frequency"""

        if iface == "DVI":
            # Enable HDMI-D interface
            logger.debug("Setting HDMI-D interface (XVSI 3)...")
            if self.send_cmd("XVSI 3") == 0:
                return 0
        else:
            # Enable HDMI-H interface
            logger.debug("Setting HDMI-H interface (XVSI 4)...")
            if self.send_cmd("XVSI 4") == 0:
                return 0
            
        logger.debug("Setting the image to " + image + " ...")
        if self.send_cmd("IMGL "+image) == 0:
            return 0

        logger.debug("Setting the analog video signal type to 0...")
        if self.send_cmd("AVST 0") == 0:
            return 0

        logger.debug("Setting the format " + fmt + "...")
        if self.send_cmd("FMTL " + fmt) == 0:
            return 0
        
        logger.debug("Setting the color space to " + cspace + "...")
        if cspace == "RGB":
            logger.debug("Setting the DVST to 10...")
            if self.send_cmd("DVST 10") == 0:
                return 0
            
            logger.debug("Setting the DVSM to 0...")
            if self.send_cmd("DVSM 0") == 0:
                return 0
            
        elif cspace == "444":
            logger.debug("Setting the DVST to 15...")
            if self.send_cmd("DVST 15") == 0:
                return 0
            
            logger.debug("Setting the DVSM to 4...")
            if self.send_cmd("DVSM 4") == 0:
                return 0
            
        elif cspace == "422":
            logger.debug("Setting the DVST to 15...")
            if self.send_cmd("DVST 15") == 0:
                return 0

            logger.debug("Setting the DVSM to 2...")
            if self.send_cmd("DVSM 2") == 0:
                return 0

        else:
            logger.debug("ERROR: Unknown Color space: " + cspace)
            return 0

        if cdepth == "8":
            logger.debug("Setting the NBPC to 8...")
            if self.send_cmd("NBPC 8") == 0:
                return 0
            logger.debug("Setting the PELD to 32...")
            if self.send_cmd("PELD 32") == 0:
                return 0
        elif cdepth == "10":
            logger.debug("Setting the NBPC to 10...")
            if self.send_cmd("NBPC 10") == 0:
                return 0
            logger.debug("Setting the PELD to 32...")
            if self.send_cmd("PELD 32") == 0:
                return 0
        elif cdepth == "12":
            logger.debug("Setting the NBPC to 12...")
            if self.send_cmd("NBPC 12") == 0:
                return 0
            logger.debug("Setting the PELD to 32...")
            if self.send_cmd("PELD 32") == 0:
                return 0
        else:
            logger.debug("ERROR: Unknown color depth: " + cdepth)    

        if afreq == "88.2":
            logger.debug("Setting the ARAT to 88.2e3...")
            if self.send_cmd("ARAT 88.2e3") == 0:
                return 0
        elif afreq == "96":
            logger.debug("Setting the ARAT to 96.0e3...")
            if self.send_cmd("ARAT 96.0e3") == 0:
                return 0
        elif afreq == "48":
            logger.debug("Setting the ARAT to 48.0e3...")
            if self.send_cmd("ARAT 48.0e3") == 0:
                return 0
        elif afreq == "44.1":
            logger.debug("Setting the ARAT to 44.1e3...")
            if self.send_cmd("ARAT 44.1e3") == 0:
                return 0
        elif afreq == "32":
            logger.debug("Setting the ARAT to 32.0e3...")
            if self.send_cmd("ARAT 32.0e3") == 0:
                return 0
        elif afreq == "176.4":
            logger.debug("Setting the ARAT to 176.4e3...")
            if self.send_cmd("ARAT 176.4e3") == 0:
                return 0
        elif afreq == "192":
            logger.debug("Setting the ARAT to 192.0e3...")
            if self.send_cmd("ARAT 192.0e3") == 0:
                return 0
        else:
            logger.debug("ERROR: Unknown audio sampling frequency: "+afreq)
            return 0

        if ach == "2":
            logger.debug("Setting the NDAC to 2...")
            if self.send_cmd("NDAC 2") == 0:
                return 0
        elif ach == "6":
            logger.debug("Setting the NDAC to 8...")
            if self.send_cmd("NDAC 8") == 0:
                return 0
            logger.debug("Setting the DACA to 63...")
            if self.send_cmd("DACA 63") == 0:
                return 0
            logger.debug("Setting the DACG to 63...")
            if self.send_cmd("DACG 63") == 0:
                return 0
            logger.debug("Setting the DAXA to 63...")
            if self.send_cmd("DAXA 63") == 0:
                return 0
            logger.debug("Setting the DAXG to 63...")
            if self.send_cmd("DAXG 63") == 0:
                return 0
            logger.debug("Setting the XAUD:CA to 11...")
            if self.send_cmd("XAUD:CA 11") == 0:
                return 0
            
        elif ach == "8":
            logger.debug("Setting the NDAC to 8...")
            if self.send_cmd("NDAC 8") == 0:
                return 0
            logger.debug("Setting the DACA to 255...")
            if self.send_cmd("DACA 255") == 0:
                return 0
            logger.debug("Setting the DACG to 255...")
            if self.send_cmd("DACG 255") == 0:
                return 0
            logger.debug("Setting the DAXA to 447...")
            if self.send_cmd("DAXA 447") == 0:
                return 0
            logger.debug("Setting the DAXG to 447...")
            if self.send_cmd("DAXG 447") == 0:
                return 0
            logger.debug("Setting the XAUD:CA to 19...")
            if self.send_cmd("XAUD:CA 19") == 0:
                return 0
        else:
            logger.debug("ERROR: Incorrect numbe of channels: "+str(ach))
            return 0
        
        #time.sleep(1)
        logger.debug("Sending the ALLU command...")
        if self.send_cmd("ALLU") == 0:
                return 0
        
        return 1
    def capture_edid(self):
        self.tn.write("EDID?\n")
        time.sleep(1.0)
        list1 = "^\\tffs0>EDID\?*\\tffs0>$"
        data = self.tn.expect([list1], timeout=5)
        edid_data = (re.split("\\\\", re.split("\?", data[2])[1])[0].rstrip()).lstrip()
        return edid_data

    def capture_bmp(self, filename):
        """save input in input port to QD buffer"""
        """if self.send_cmd('XVSI:IN ' + str(port)) == 0:
            return 0
        if self.send_cmd("PDAX:REFG 0") == 0:
            return 0
        if self.send_cmd("PDAX:RPTG 0") == 0:
            return 0
        if self.send_cmd("PELD 32") == 0:
            return 0
        logger.debug("QD: Capturing frame on input HDMI port IN" + str(port) + " to buffer")
        if self.send_cmd('PDAX:CAPF') == 0:
            return 0
        sys.stdout.write('QD: Display buffer on HDMI output OUT1')      
        if self.send_cmd('PDAX:VIEW') == 0:
            return 0
        if self.send_cmd('FILE:SCREENCAP ' + filename) == 0:
            return 0
        logger.debug('\n')
        status = 0
        s = '.'
        sys.stdout.write('QD: Saving buffer to ' + filename)
        while(status == 0):
            try:
                status = self.send_cmd('LEDS?', 1)
                sys.stdout.write(s)
                sys.stdout.flush()
                time.sleep(2)
            except:
                logger.debug("Unexpected error:", sys.exc_info()[0])
                time.sleep(5)
                logger.debug("QD: Error in LEDS command after save buffer.")
                return 0"""
        
        if self.send_cmd("DVQM 0") == 0:
            return 0
        if self.send_cmd("ALLU") == 0:
            return 0
        time.sleep(5)
        if self.send_cmd("PDAX:REFG 0") == 0:
            return 0
        if self.send_cmd("PDAX:RPTG 0") == 0:
            return 0
        if self.send_cmd("PELD 32") == 0:
            return 0
        logger.debug("capture fram on HDMI port IN1 to buffer ")
        print("capture fram on HDMI port IN1 to buffer ")
        if self.send_cmd("PDAX:CAPF") == 0:
            return 0
        time.sleep(10)
        logger.debug("Display buffer on HDMI output OUT1")
        print("Display buffer on HDMI output OUT1")
        if self.send_cmd("PDAX:VIEW") == 0:
            print("Error")
            return 0
        time.sleep(10)
        logger.debug("Saving buffer to /card0/"+filename)
        print("Saving buffer to /card0/"+filename)
        status = 0
        s = "."
        if self.send_cmd("FILE:SCREENCAP /card0/"+filename) == 0:
            return 0
        """status = 0
        s = '.'
        sys.stdout.write('QD: Saving buffer to ' + filename)
        while(status == 0):
            try:
                status = self.send_cmd('LEDS?')
                sys.stdout.write(s)
                sys.stdout.flush()
                time.sleep(2)
            except:
                logger.debug("Unexpected error:", sys.exc_info()[0])
                time.sleep(5)
                logger.debug("QD: Error in LEDS command after save buffer.")
                return 0"""
        time.sleep(20)
        return 1
     
    def compareToGoldenFrame(self, path, numberOfFrames):
        path = str(path)
        if self.send_cmd("PDAX:FRMS " + str(numberOfFrames)) == 0:
            return -1
        if self.send_cmd("PDAX:REFG 0") == 0:
            return -1
        if self.send_cmd("PDAX:GFCL " + path) == 0:
            return -1
        if self.send_cmd("PDAX:GFCU") == 0:
            return -1
        status = 0
        s = '.'
        logger.debug('QD: Loading golden frame ')
        while status == 0:
                status = self.send_cmd('LEDS?')
                sys.stdout.write(s)
                sys.stdout.flush()
                time.sleep(2)
        logger.debug('\n')
        if self.send_cmd("PDAU") == 0:
            return -1
        status = 0
        s = '.'
        logger.debug('QD: Comparing ')
        while status == 0:
                status = self.send_cmd('LEDS?')
                sys.stdout.write(s)
                sys.stdout.flush()
                time.sleep(0.5)
        logger.debug('\n')
        errors = self.send_cmd("PDAX:NERR?")
        errors = errors[12:16]
        logger.debug("QD: Number of errors: " + str(int(errors)))
        return int(errors)

    def compareToBuffer(self, numberOfFrames):
        if self.send_cmd("DVQM 0") == 0:
            return -1
        if self.send_cmd("PDAX:FRMS " + str(numberOfFrames)) == 0:
            return -1
        #if self.send_cmd("PDAX:MXER 1000") == 0:
        #    return -1
        if self.send_cmd("PDAX:RPTG 1") == 0:
            return -1
        if self.send_cmd("PDAX:REFG 0") == 0:
            return -1
        if self.send_cmd("PDAX:CAPF") == 0:
            return -1
        if self.send_cmd("PDAU") == 0:
            return -1
        status = 0
        s = '.'
        logger.debug('QD: Comparing ')
        while status == 0:
            status = self.send_cmd('LEDS?')
            sys.stdout.write(s)
            sys.stdout.flush()
            time.sleep(0.5)
        logger.debug('\n')
        errors = self.send_cmd("PDAX:NERR?")
        logger.debug("error = "+str(errors))
        error_value = errors[12:16]
        logger.debug("QD: Number of errors: " + str(error_value))
        return int(error_value)

    def compareToPreBuffer(self, numberOfFrames):
        if self.send_cmd("DVQM 0") == 0:
            return -1
        if self.send_cmd("PDAX:FRMS " + str(numberOfFrames)) == 0:
            return -1
        if self.send_cmd("PDAU") == 0:
            return -1
        status = 0
        s = '.'
        logger.debug('QD: Comparing ')
        while status == 0:
            status = self.send_cmd('LEDS?')
            sys.stdout.write(s)
            sys.stdout.flush()
            time.sleep(0.5)
        logger.debug('\n')
        errors = self.send_cmd("PDAX:NERR?")
        logger.debug("error = "+str(errors))
        error_value = errors[12:16]
        logger.debug("QD: Number of errors: " + str(error_value))
        return int(error_value)
    
    def captureToBuffer(self):
        if self.send_cmd("PDAX:REFG 0") == 0:
            return 0
        if self.send_cmd("PDAX:CAPF") == 0:
            return 0
        status = 0
        s = '.'        
        while status == 0:
            status = self.send_cmd('LEDS?')
            sys.stdout.write(s)
            sys.stdout.flush()
            time.sleep(0.5)
        logger.debug('\n')
        return 1
    
    def savebuffertofile(self, filename):
        if self.send_cmd("PDAX:GFCA /card0/Library/UserData/captures/" + filename) == 0:
            return 0
        status = 0
        s = '.'
        logger.debug('QD: Saving frame to /card0/Library/UserData/captures/' + filename)
        while status == 0:
            status = self.send_cmd('LEDS?')
            sys.stdout.write(s)
            sys.stdout.flush()
            time.sleep(1)
        logger.debug('\n')
        return 1

    def detectFormat(self):
        self.send_cmd("TMAU")
        VRES = self.send_cmd('TMAX:VRES?')
        HRES = self.send_cmd('TMAX:HRES?')
        
        if VRES != 0:
            VRES = int(VRES[12:19])
        if HRES != 0:
            HRES = int(HRES[12:19])
            
        SCAN = self.send_cmd('TMAX:SCAN?')
        VRAT = self.send_cmd('TMAX:VRAT?')
    
        if SCAN != 0:
            if int(SCAN[12:18]) == 1:
                                if (VRES == 720) or (VRES == 480) or (VRES == 1080):
                                        scan = 'P'
                                else:
                                        scan = ''                                       
            elif int(SCAN[12:18]) == 2:
                scan = 'I'
            else:
                scan = 'ERROR'
    
        if VRAT != 0:
            VRAT = float(VRAT[12:24])
            rate = int(VRAT)

        if (VRES == 0) or (HRES == 0):
            return 0
        else:
            return str(HRES) + "X" + str(VRES) + scan + "@" + str(rate)

    def setPseudoRandomNoise(self):        
        if self.send_cmd("DVQM 0") == 0:
            return 0
        if self.send_cmd("PELD 32") == 0:
            return 0
        if self.send_cmd("ISUB 1") == 0:
            return 0
        if self.send_cmd("IVER 1") == 0:
            return 0
        if self.send_cmd("IMGL PRN24BIT") == 0:
            return 0
        if self.send_cmd("IMGU") == 0:
            return 0
        if self.send_cmd("IMGL PRN24BIT") == 0:
            return 0
        if self.send_cmd("ALLU") == 0:
            return 0
        status = 0
        s = '.'
        logger.debug('QD: Setting up Pseudo Random Noise image ')
        while status == 0:
                status = self.send_cmd('LEDS?')
                sys.stdout.write(s)
                sys.stdout.flush()
                time.sleep(2)
        logger.debug('\n')
        if self.send_cmd("PDAX:RPTG 0") == 0:
            return 0
        if self.send_cmd("PDAX:REFG 0") == 0:
            return 0
        return 1
     
    def PseudoNoiseTestOn(self):
        if self.send_cmd("XVSI 4") == 0:
            return 0
        if self.send_cmd("ALLU") == 0:
            return 0
        if self.send_cmd("PNSA 1") == 0:
            return 0
        if self.send_cmd("PNSM 0") == 0:
            return 0
        if self.send_cmd("PNSG 1") == 0:
            return 0
        if self.send_cmd("PNGU") == 0:
            return 0
        
    def PseudoNoiseTestRun(self):   
        if self.send_cmd("PNSP 100") == 0:
            return 0
        if self.send_cmd("PNAU") == 0:
            return 0
        if self.send_cmd("GPER?") == 0:
            return 0
        
    def changeColorSpace(self, colorSpace):

        if colorSpace == 'RGB':
            if self.send_cmd("DVST 10") == 0:
                return 0
            if self.send_cmd("DVSM 0") == 0:
                return 0
        elif colorSpace == 'YC444':
            if self.send_cmd("DVST 15") == 0:
                return 0
            if self.send_cmd("DVSM 4") == 0:
                return 0
        elif colorSpace == 'YC422':
            if self.send_cmd("DVST 15") == 0:
                return 0
            if self.send_cmd("DVSM 2") == 0:
                return 0
        else:            
            logger.debug('QD ERROR: Color Space: ' + colorSpace + ' not available.')
            return 0
        if self.send_cmd("ALLU") == 0:
            return 0
        logger.debug('QD: Color Space set to: ' + colorSpace)
        return 1

    def popimage(self):
        logger.debug("reload the saved image")
        self.PRE_IMAGE = self.CUR_IMAGE
        self.load("HDMI", self.SAVE_IMAGE, "/tffs0/Library/formats/1080p59", "RGB", "8")
        return 0

    def pushimage(self):
        logger.debug("save the last test image")
        self.SAVE_IMAGE = self.PRE_IMAGE
        return 0

    def close(self):
        """Close the telnet connection"""

        self.tn.close()

