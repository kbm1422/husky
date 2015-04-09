#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import smtplib
import email
from smtplib import SMTPException


class SMTPClient(smtplib.SMTP):
    def transmit(self, sender, receivers, subject, body=None, attachments=None):
        """
        @param body: body used as params of email.mime.Text.MIMEText, it should be a str or tuple
                         if it is a str, the subtype is 'plain', and charset is None
                         if it is a tuple (_text, _subtype='plain', _charset=None), you can specify the subtype and charset
                         for example: if we send body is a html, we need to set body as (htmlcontent, "html")
                        
        """
        attachments = attachments or []
        logger.debug("Send mail: sender=%s, receivers=%s, subject=%s, attachments=%s",
                     sender,
                     receivers,
                     subject,
                     attachments)
        msg = email.MIMEMultipart.MIMEMultipart()
        msg.add_header("From", sender)
        msg.add_header("To", ", ".join(receivers))
        msg.add_header("Subject", subject)
        
        if body is not None:
            if isinstance(body, tuple):
                msg.attach(email.mime.Text.MIMEText(*body))
            elif isinstance(body, str):
                msg.attach(email.mime.Text.MIMEText(body))
            else:
                raise TypeError()

        for attachment in attachments:
            part = email.MIMEBase.MIMEBase('application', "octet-stream")
            part.set_payload(open(attachment, "rb").read())
            email.encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment;filename=%s" % os.path.basename(attachment))
            msg.attach(part)

        self.sendmail(sender, receivers, msg.as_string())

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )

    report = r"D:\Unit Test Report.htm"
    smtp = SMTPClient("172.25.0.3")
    with open(report, "rb") as f:
        smtp.transmit("sqagroup@siliconimage.com", ["yale.yang@siliconimage.com"], "test subject", (f.read(), "html"))
    smtp.close()
#     smtp.quit()
#     message = email.message.Message()
#     message.add_header("From", "From %s" % "yale.yang@siliconimage.com")
#     message.add_header("To", "To %s" % ", ".join(["yale.yang@siliconimage.com"]))
#     message.add_header("Subject", "test")
#     message.set_payload("test content")
#     print(message.as_string())