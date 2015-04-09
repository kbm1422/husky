#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


import errno
import random
import socket


def get_tcpport_not_in_use(a=40000, b=65535):
    logger.info("random a tcpport not in use, range from %d to %d", a, b)
    while True:
        sock = socket.socket()
        port = random.randint(a, b)
        addr = ("0.0.0.0", port)
        try:
            sock.bind(addr)
        except socket.error as err:
            if err.errno == errno.EADDRINUSE:
                logger.debug("addr <%d:%d> is in use, random another port", a, b)
                continue
            else:
                raise
        else:
            return port
        finally:
            sock.close()