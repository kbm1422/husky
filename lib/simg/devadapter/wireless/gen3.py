#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import re
import time
import errno

from .swam3 import SWAM3DeviceAdapter, SWAM3Connection


class Gen3SWAM3Connection(SWAM3Connection):
    def upgradeFirmware(self, filename):
        if not os.path.exists(filename):
            raise OSError(errno.ENOENT, "Firmware '%s' not exists" % filename)

        resetflag = False
        logger.debug("Querying the Enable Host bootup with BB in resetmode NVRAM (0x67) value on Gen3...")
        val = self.sendcmd("nvramget 0x67")
        if re.search("Parameter 0x67=0x01", val, re.I):
            logger.debug("Setting the Enable Host bootup with BB in resetmode NVRAM (0x67) value on Gen3 to 0...")
            self.sendcmd("nvramset 0x67 0x0")
            resetflag = True

        logger.debug("Querying the Sleep duration on inactivity (0x66) value on Gen3...")
        val = self.sendcmd("nvramget 0x66")
        if not re.search("Parameter 0x67=0x0", val, re.I):
            logger.debug("Setting the Sleep duration on inactivity (0x66) value on Gen3 to 0...")
            self.sendcmd("nvramset 0x66 0x0")
            resetflag = True

        if resetflag:
            self.reset()
            time.sleep(15)

        self.sendcmd("nvram_update_flag 0 1")
        self.sendcmd("ss_server embeddedupgrade=%s" % filename)
        self.sendcmd("nvram_update_flag 0 0")
        self.reset()
        time.sleep(15)

    def reset(self):
        return self.sendcmd("reset")


class Gen3DeviceAdapter(SWAM3DeviceAdapter):
    Connection = Gen3SWAM3Connection

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )