#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
B&A debug logging test suite
Test B&A firmware shell commands send out and response
Note: before test, make sure B&A has connected with Linux PC through USB cable, driver has been installed and
firmware has been loaded
"""

import logging

logger = logging.getLogger(__name__)

from simg.test.framework import TestCase
from simg.test.framework import TestContextManager

cmd_list = """
nvram_show
show_version
nvramset 0x66 0
nvramget 0x66
nvram_set_defaults
umac_sm_show
custparamget 1
custparamget 2
custparamget 3
custparamget 4
disconnect_device 0
wvan_rescan
scan_status
switch_wvan %s
find_wvan %s
dev_table_dump 0
dev_table_dump 2
connect_device 0
dump_edid 0
dev_table_dump 1
get_av_info
"""


class ShellCmdTestCase(TestCase):
    def setUp(self):
        context = TestContextManager().getCurrentContext()
        self.txunits = context.resource.txunits
        self.rxunits = context.resource.rxunits
        self.p_cmd_list = cmd_list % self.txunits[0]

    def test_shellcmd(self):
        """Steps:
        1. Load commands from B&A_shell_command.txt
        2. Change debug logging mode according to serial or SPI setup
        3. Issue commands in B&A_shell_command.txt one by one
        4. Checkpoint: check response of issued command, report fail if response "FAIL", "ERROR", NONE, timeout > 60s, no <EOF>, otherwise report pass
        """
        m_cmd_list = [item for item in self.p_cmd_list.split('\n') if item]

        for cmd in m_cmd_list:
            self.txunits[0].emptyCmdOutput()
            self.txunits[0].runCmd(cmd)
            result = self.txunits[0].catCmdOutput()
            if re.search("Exc Thread:", str(resp2), re.I) \
                    or re.search("ERROR: Invalid Command", str(resp2), re.I) \
                    or re.search("FAIL", str(resp2), re.I):
                self._fail("The shell command %s is executed with error: %s" % (cmd, result))
            else:
                self._pass("The shell command %s is executed successfully")