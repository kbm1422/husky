#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import datetime
import urllib2
import json
from urlparse import urlsplit, urlunsplit

import pprint
import collections
import unittest
import shelve


from abc import ABCMeta, abstractmethod


class TestResult(unittest.TestResult):
    def __init__(self, *args, **kwargs):
        super(TestResult, self).__init__(*args, **kwargs)
        self.successes = []
        self.warnings = []
        self.case_records = []
        self.suite_records = []
        self.shouldPause = False
        self.__case_record_handlers = []
        self.starttime = None
        self.stoptime = None

    def addCaseRecordHandler(self, handler):
        logger.info("add record handler: %s", handler)
        if not issubclass(handler.__class__, BaseCaseRecordHandler):
            raise TypeError
        self.__case_record_handlers.append(handler)

    def removeCaseRecordHandler(self, handler):
        logger.info("remove record handler: %s", handler)
        if not issubclass(handler.__class__, BaseCaseRecordHandler):
            raise TypeError
        self.__case_record_handlers.remove(handler)

    def callCaseRecordHandlers(self, record):
        for handler in self.__case_record_handlers:
            handler.emit(record)

    def __getstate__(self):
        keys = ("starttime", "stoptime", "suite_records", "failfast", "testsRun")
        d = {}
        for key in keys:
            d[key] = self.__dict__[key]
        return d

    def startTestRun(self):
        self.starttime = datetime.datetime.now()

    def stopTestRun(self):
        self.stoptime = datetime.datetime.now()

    def startTest(self, test):
        super(TestResult, self).startTest(test)
        test.starttime = datetime.datetime.now()

    def stopTest(self, test):
        super(TestResult, self).stopTest(test)
        test.endtime = datetime.datetime.now()
        test.record.duration = round((test.endtime - test.starttime).total_seconds(), 3)
        self.addTestCaseResultRecord(test.record)

    def addTestCaseResultRecord(self, record):
        self.case_records.append(record)
        self.callCaseRecordHandlers(record)

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        if test.record.warnings:
            status = TestCaseResultRecord.Status.WARNING
            self.warnings.append(test)
        else:
            status = TestCaseResultRecord.Status.PASSED
            self.successes.append(test)
        test.record.status = status

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)

        # The test may be a _ErrorHolder object which has not attribute exc_info_to_string
        # In this case, call TestResult._exc_info_to_string instead to output the log
        if isinstance(test, unittest.TestCase):
            error = self._format_error(err, test)
            test.record.status = TestCaseResultRecord.Status.ERRONEOUS
            test.record.error = error
        else:
            error = self._exc_info_to_string(err, test)
            logger.error(error)
            test.record = TestCaseResultRecord()
            test.record.name = test.description
            test.record.status = TestCaseResultRecord.Status.ERRONEOUS
            test.record.error = error

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        error = self._format_error(err, test)
        test.record.status = TestCaseResultRecord.Status.FAILED
        test.record.error = error

    def addSkip(self, test, reason):
        unittest.TestResult.addSkip(self, test, reason)
        test.record.status = TestCaseResultRecord.Status.SKIPPED
        test.record.skipreason = reason

    def addExpectedFailure(self, test, err):
        unittest.TestResult.addExpectedFailure(self, test, err)
        error = self._format_error(err, test)
        test.record.status = TestCaseResultRecord.Status.PASSED
        test.record.error = error

    def addUnexpectedSuccess(self, test):
        unittest.TestResult.addUnexpectedSuccess(self, test)
        test.record.status = TestCaseResultRecord.Status.FAILED

    @staticmethod
    def _format_error(exc_info, test):
        error = (exc_info[0], exc_info[1], test.exc_info_to_string(exc_info))
        logger.error(error[2])
        return error

    def pause(self):
        self.shouldPause = True

    def resume(self):
        self.shouldPause = False


class TestCaseResultRecord(object):
    class Status(object):
        PASSED = 1
        WARNING = 2
        FAILED = 3
        SKIPPED = 4
        ERRONEOUS = 5

    STATUS_MAPPER = {Status.PASSED: "PASSED",
                     Status.WARNING: "WARNING",
                     Status.FAILED: "FAILED",
                     Status.SKIPPED: "SKIPPED",
                     Status.ERRONEOUS: "ERRONEOUS"}

    def __init__(self):
        self.caseid = None
        self.testid = None
        self.name = None
        self.clsname = None
        self.status = None
        self.error = None
        self.skipreason = None
        self.warnings = []
        self.checkpoints = []
        self.concerns = collections.OrderedDict()
        self.duration = None

    def __repr__(self):
        return "<TestCaseResultRecord(name:%s, id:%s, status:%s)>" % (self.name,
                                                                      self.testid,
                                                                      self.STATUS_MAPPER[self.status])

    def __str__(self):
        return self.__repr__()


class TestSuiteResultRecord(object):
    def __init__(self, suiteid=None, testid=None, name=None):
        self.suiteid = suiteid
        self.testid = testid
        self.name = name
        self.subrecords = []

    def addSubTestResultRecord(self, record):
        self.subrecords.append(record)

    def getLastTestCaseResultRecord(self):
        lastSubRecord = self.subrecords[-1]
        if isinstance(lastSubRecord, TestSuiteResultRecord):
            return lastSubRecord.getLastTestCaseResultRecord()
        else:
            return lastSubRecord

    def __repr__(self):
        return "<TestSuiteResultRecord(name:%s, suiteid: %s, testid:%s, subrecords:%s)>" % (self.name,
                                                                                            self.suiteid,
                                                                                            self.testid,
                                                                                            pprint.pformat(self.subrecords))

    def __str__(self):
        return self.__repr__()


class BaseCaseRecordHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def emit(self, record):
        """a hook method, will be called in TestResult.callRecordHandlers"""
        pass


# FIXME: there is a circular reference between result and handler
class ShelveResultHandler(BaseCaseRecordHandler):
    def __init__(self, shelve, result):
        self.shelve = shelve
        self.result = result

    def emit(self, record):
        shd = shelve.open(self.shelve, protocol=2, writeback=True)
        try:
            shd["result"] = self.result
            shd["result"].stoptime = datetime.datetime.now()
        finally:
            shd.close()


class ShelveCaseRecordHandler(BaseCaseRecordHandler):
    def __init__(self, filename):
        self._filename = filename
        shd = shelve.open(self._filename)
        if not "case_records" in shd:
            shd["case_records"] = []
        shd.close()

    def emit(self, record):
        shd = shelve.open(self._filename, protocol=2, writeback=True)
        try:
            shd["case_records"].append(record)
        finally:
            shd.close()


class HttpCaseRecordHandler(BaseCaseRecordHandler):
    def __init__(self, url):
        result = urlsplit(url)
        parts = (result.scheme, result.netloc, result.path.replace("//", "/"), result.query, result.fragment)
        self._url = urlunsplit(parts)

    def emit(self, record):
        logger.debug("emit case record: %s", record.__dict__)
        try:
            request = urllib2.Request(self._url, json.dumps(record.__dict__), headers={"Content-Type": "application/json"})
            urllib2.urlopen(request)
        except urllib2.URLError as err:
            logger.error("error emit case record: %s", str(err))

    def __repr__(self):
        return "<HttpRecordHandler(%s)>" % self._url

    def __str__(self):
        return self.__repr__()


class AmqpCaseRecordHandler(BaseCaseRecordHandler):
    def __init__(self, url, exchange_name="simg.test.record", exchange_type="fanout"):
        pass

    def emit(self, record):
        logger.debug("emit case record: %s", record.__dict__)
        json.dumps(record.__dict__)

