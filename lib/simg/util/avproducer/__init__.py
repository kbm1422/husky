#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import re
import socket
import telnetlib

from base import BaseAVProducer


class Type(object):
    QD882 = "QD882"
    VG876 = "VG876"
    BDP = "BDP"
    MOBILE = "MOBILE"
    VIDEOCARD = "VIDEOCARD"
    DVDO = "DVDO"


class AVProducerFactory(object):
    @classmethod
    def new_avproducer(cls, **kwargs):
        avp_type = kwargs.pop("type").upper() if "type" in kwargs else None
        if avp_type == Type.QD882:
            from qd882 import QD882
            return QD882(**kwargs)
        elif avp_type == Type.VG876:
            from astro import VG876
            return VG876(**kwargs)
        elif avp_type == Type.BDP:
            return BDP(**kwargs)
        elif avp_type == Type.MOBILE:
            return Mobile(**kwargs)
        elif avp_type == Type.VIDEOCARD:
            return VideoCard(**kwargs)
        elif avp_type == Type.DVDO:
            return DVDO(**kwargs)
        else:
            return BaseAVProducer(**kwargs)


class BDP(BaseAVProducer):
    pass


class Mobile(BaseAVProducer):
    pass


class DVDO(BaseAVProducer):
    pass


class VideoCard(BaseAVProducer):
    def __init__(self, host, port=22):
        super(VideoCard, self).__init__(name="GTX")
        """Initialise the communication with VideoCard, given its IP address"""
        self.host = host
        self.inited = False
        if not self.host.strip():
            raise ValueError("Supplied IP address is blank")

        # Trim any leading zeros in the IP. Eg: Convert 010.005.060.208 to 10.5.60.208
        k = dict()
        b = re.match(r"(.*)\.(.*)\.(.*)\.(.*)", self.host)
        for i in range(1, 5):
            k[i] = b.group(i).lstrip('0')
            if not k[i]:
                k[i] = '0'
        self.host = k[1]+"."+k[2]+"."+k[3]+"."+k[4]
        logger.debug("The IP address of the VideoCard is "+self.host)
        self.tn = telnetlib.Telnet()
        try:
            self.tn.open(self.host, port)
        except socket.error:
            logger.exception("ERROR: Unable to open a telnet connection with %s", self.host)
            raise

        self.inited = True