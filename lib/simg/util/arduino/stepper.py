#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import serial
import time


class Stepper(object):
    def __init__(self, comport=None, baudrate=9600):
        self.arduino = serial.Serial()
        if comport is not None:
            self.open(comport, baudrate)

    def open(self, comport, baudrate=9600):
        self.arduino.port = comport
        self.arduino.baudrate = baudrate
        self.arduino.open()
        time.sleep(2.0)

    def goForward(self):
        self.arduino.write("F")
        time.sleep(1.0)

    def goBackward(self):
        self.arduino.write("B")
        time.sleep(1.0)

    def close(self):
        if self.arduino.isOpen():
            self.arduino.close()

    def __del__(self):
        self.close()


class PlugInConnector(Stepper):
    def __init__(self, comport, baudrate=9600, steps=7):
        Stepper.__init__(self, comport, baudrate)
        self.steps = steps

    def connect(self, holdseconds=None):
        for _ in range(self.steps):
            self.goForward()
        if holdseconds:
            time.sleep(holdseconds)

    def disconnect(self, holdseconds=None):
        for _ in range(self.steps):
            self.goBackward()
        if holdseconds:
            time.sleep(holdseconds)

    def cycle(self, disconntime=None, conntime=None):
        self.disconnect(disconntime)
        self.connect(conntime)

if __name__ == "__main__":
    stepper = Stepper("COM9")
    stepper.goBackward()
    stepper.goForward()
    stepper.close()

