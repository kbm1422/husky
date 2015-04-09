#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
#p-scope>help

help
Available Commands:
hdmitx: enable HDMI transmitter
heac: set HDMI 1.4 HEAC mode
hdcp2: test hdcp2 implementation
hdmi2: test hdmi2 implementation
r0: read BAR[0]:  r0 <32 bit word address in hex>
r1: read BAR[1]:  r1 <32 bit word address in hex>
r2: read BAR[2]:  r2 <32 bit word address in hex>
R0: read BAR[2]:  r2 <128 bit word address in hex>
R1: read BAR[2]:  r2 <128 bit word address in hex>
R2: read BAR[2]:  r2 <128 bit word address in hex>
w0: write BAR[0]: w0 <32 bit word address in hex> <32bit data in hex>
w1: write BAR[1]: w1 <32 bit word address in hex> <32bit data in hex>
w2: write BAR[2]: w2 <32 bit word address in hex> <32bit data in hex>
pcap: pscope capture: pcap start/stop/decode/info
pdax: pscope golden frame test usage: PDAX:[NFRS | CAPF | GFCA | GFCL | GFCU | MXER | REFG | ERRQ | NERR | PDAU]
prng: pscope pseudo-random test generator usage: PRNG:[PNST | PNAU]
scdc: HDMI 2.0 SCD control
prna: pscope pseudo-random test analyzer usage: PRNG:[ NERR | ERRQ | GNRT | GPER | PNAU | STOP | STAT]
spiw: SPI flash write: spiw  <bit file name>
gwp: SPI flash write: gwp  <bit file name>
edidw: HDMI Rx EDID write: edidw  <bit file name>
edidr: read tx EDID
edidct: tx EDID Compliance Test
i2cr: read  i2c reg: i2c  <address in hex>
i2cw: write i2c reg: i2c  <address in hex>
ddcr: read  tx ddc reg: ddc  <address in hex>
ddcw: write rx ddc reg: ddc  <address in hex>
ddcwf: write rx ddc from file
lic: license info
prat: get TMDS clock rate
pstat600: get dual RX TMDS status for HDMI 2.0 analyzer
pp: get dual RX TMDS status for HDMI 2.0 analyzer
qdb:  r | w | spir | dump|
hp: set HDMI Rx Hot Plug
setip: set Ip address, mask and gateway
getip: get Ip address, mask and gateway
mode: get the current mode
mon: set HDMI monitor mode <mhl - mhl with preamble recovery> | <mhlr - mhl raw> | <hdmi> | <stat - get status>
discover: interface card context discovery
sysinfo: get internal board info
memt: DRAM r/w test: memt <number of iteration>
ppci: scanning for box pci resources: ppci
slink: enable HDMI Link analyzer
tmdst: enable TMDS termination
calibrx: set TMDS RX calibration parameters
vinfo: RX HDMI video information
vsinfo: vstream video info
vmode: get mode of input video HDMI or DVI
ver: version number
q: quit
quit: quit
help: this help
"""

import telnetlib
import time
import re
import os
from ftplib import FTP


class FTPUtil(object):
    def __init__(self, ip, _user, _pass):
        try:
            self.session = FTP(ip, _user, _pass)
            print ('FTP: FTP session opened to ' + ip)
        except:
            print("ERROR: Unable to open a ftp connection with " + ip + ": " + str(sys.exc_info()[0]) + str(
                sys.exc_info()[1]))

    def upload(self, srcpath, destpath):
        f = open(destpath, 'wb')
        try:
            self.session.retrbinary("RETR " + srcpath, f.write)
        except Exception:
            print ("FTP: Error in uploading the remote file.")
        else:
            print ("FTP: " + srcpath + " successfully uploaded to " + destpath)
        finally:
            f.close()


class AudioInfo():
    def __init__(self, _host, _user="qd", _pass="qd"):
        self.host = _host
        self.username = _user
        self.password = _pass
        tn = telnetlib.Telnet(self.host, port=23, timeout=10)
        # tn.set_debuglevel(2)

        tn.read_until('xpscope-4a login: ')
        tn.write(self.username + '\n')

        tn.read_until('Password: ')
        tn.write(self.password + '\n')
        tn.read_until("p-scope>")
        self.tn = tn

    def get_audio_info(self, mem_size="small"):
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
        self.tn.read_until('complete')
        time.sleep(0.5)
        self.tn.write("pcap timing" + '\n')
        self.tn.read_until('type=112 complete')
        time.sleep(0.5)

        self.tn.read_until(">")
        self.tn.close()

        timing = FTPUtil(self.host, self.username, self.password)
        src = "/home/qd/pdecode.log"

        dest = os.path.dirname(os.path.abspath(__file__)) + "\\pdecode.log"
        timing.upload(src, dest)

        time.sleep(3)

        line_collection = list()
        with open(dest, 'r') as f:
            for line in f:
                if "Audio InfoFrame" in line:
                    break

            for line in f:
                if "<EOP>" in line:
                    break
                # print line.strip()
                if not line.strip() == "#":
                    line_collection.append(line.strip())

        audio_info = dict()
        for line in line_collection:
            s_line = [l.strip() for l in line.split(":")]
            audio_info[s_line[0]] = s_line[1]

        return audio_info

if __name__ == "__main__":
    host = "172.16.131.189"
    username = "qd"
    password = "qd"
    qd980 = AudioInfo(host, username, password)
    print qd980.get_audio_info(mem_size="small")

