#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import sys
import time
import ctypes

bindir = os.path.dirname(sys.executable) if hasattr(sys, '_MEIPASS') else sys.path[0]
rootdir = os.path.dirname(bindir)
casedir = os.path.join(bindir, "cases")
dlldir = os.path.join(rootdir, "dll")
libdir = os.path.join(rootdir, "lib")
etcdir = os.path.join(rootdir, "etc")
logdir = os.path.join(rootdir, "logs")
resconf = os.path.join(etcdir, "resource.xml")
srvconf = os.path.join(etcdir, "srvconf.xml")
sys.path.append(libdir)


if sys.platform == "win32":
    dllnames = ("ftd2xx.dll", "blackbox.dll", "aardvark.dll")
elif sys.platform.endswith("linux"):
    dllnames = ()
else:
    raise ValueError("Unsupported platform %s" % sys.platform)
for name in dllnames:
    ctypes.CDLL(os.path.join(dlldir, name))


def report(runner, mail_kwargs=None):
    from simg.test.framework import TestReport
    from simg.net.smtp import SMTPClient, SMTPException

    testreport = TestReport(runner.result)
    xmlrpt = os.path.join(runner.context.logdir, "report.xml")
    htmlrpt = os.path.join(runner.context.logdir, "report.html")
    testreport.genXMLReport(xmlrpt)
    testreport.genHTMLReport(xmlrpt, htmlrpt)

    if mail_kwargs:
        sendout = mail_kwargs.pop("sendout")
        logger.debug("Mail send out is %s", sendout)
        if sendout:
            with open(htmlrpt) as f:
                htmlbody = f.read()

            subject = "TA REPORT: %s" % mail_kwargs["subject"]
            server = mail_kwargs["server"]
            attempt = mail_kwargs["attempt"]
            sender = mail_kwargs["sender"]
            receivers = mail_kwargs["receivers"]

            smtpclient = SMTPClient(server)
            try:
                for i in range(attempt):
                    try:
                        smtpclient.transmit(sender, receivers.split(";"), subject, (htmlbody, "html"))
                    except SMTPException:
                        logger.error("Send mail failed, retry...")
                        if i == attempt-1:
                            logger.exception("")
                        time.sleep(1.0)
                    else:
                        break
            finally:
                smtpclient.close()