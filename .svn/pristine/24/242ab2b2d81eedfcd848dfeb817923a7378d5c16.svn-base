#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import importlib

from xml.etree import ElementTree


class TestBenchFactory(object):
    @classmethod
    def buildTestBenchByElement(cls, element):
        if not isinstance(element, ElementTree.Element):
            raise TypeError("Param 'element' should be an instance of xml.etree.ElementTree.Element")
        bench_type = element.get("type").lower()
        bench_module = importlib.import_module(cls.__module__ + "." + bench_type)
        return bench_module.TestBench(element)


class TestBenchConfiguration(object):
    def __init__(self, filename):
        self.__filename = filename
        tree = ElementTree.parse(self.__filename)
        self.__root = tree.getroot()

    def buildAllTestBench(self):
        benches = []
        for benchelement in list(self.__root.find("Resources")):
            bench = TestBenchFactory.buildTestBenchByElement(benchelement)
            benches.append(bench)
        return benches

    def buildTestBenchByName(self, name):
        xpath = "./Resources/TestBench[@name='%s']" % name
        benchelement = self.__root.find(xpath)
        if benchelement is None:
            raise ValueError("Can't get TestBench element by path: %s" % xpath)
        return TestBenchFactory.buildTestBenchByElement(benchelement)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )