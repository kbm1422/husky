#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
logger = logging.getLogger(__name__)

from abc import ABCMeta


class WebCamFactory(object):
    @classmethod
    def new_webcam(cls, **kwargs):
        if kwargs:
            return WebCam(**kwargs)
        else:
            return NullWebCam()


class BaseWebCam(object):
    __metaclass__ = ABCMeta

    def capture_image(self, *args, **kwargs):
        pass

    def capture_video(self, *args, **kwargs):
        pass


class WebCam(BaseWebCam):
    def __init__(self, devnum=0, show_video_window=False):
        self.devnum = int(devnum)
        self.show_video_window = show_video_window

    def capture_image(self, name, resolution=(1280, 720)):
        """
        The object construction and invoking should in same thread, otherwise it will cause blocking.
        """
        logger.debug("Capture image to '%s' with resolution '%s'", name, resolution)
        from VideoCapture import Device
        cam = Device(devnum=self.devnum)
        cam.setResolution(*resolution)
        try:
            cam.saveSnapshot(name)
        except AttributeError:
            logger.exception("")
            logger.debug("Webcam capture image failed, try is again.")
            cam.saveSnapshot(name)

    def capture_video(self, name):
        raise NotImplementedError


class NullWebCam(BaseWebCam):
    """
    See <Null Object> design pattern for detail: http://www.oodesign.com/null-object-pattern.html
    """


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )