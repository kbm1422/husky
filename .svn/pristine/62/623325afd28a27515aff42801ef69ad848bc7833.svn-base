#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import sys
from .loader import TestTargetLoader


class NativeTestTarget(object):
    def __init__(self, target, casedir, failfast=False, context=None, defines=None):
        from simg.test.framework import TestRunner

        sys.path.append(casedir)
        self.runner = TestRunner(failfast=failfast, context=context)

        for suite in TestTargetLoader(target).build_suites(defines):
            self.runner.add_suite(suite)

    def run(self):
        self.runner.start()
        try:
            while self.runner.is_alive():
                self.runner.join(1.0)
        except KeyboardInterrupt:
            logger.warn("KeyboardInterrupt. The runner will be stopped after current running test case finished.")
            self.runner.abort()
            self.runner.join()


class RemoteTestTarget(object):
    def __init__(self, target, baseurl, amqpurl, failfast=False, context=None, defines=None):
        import uuid
        from simg.net.xmlrpc import XMLRPCClient
        from simg.test.framework import XMLRPCTestRunnerProxy, TestRunnerAMQPLogConsumer

        self.__baseurl = baseurl
        self.__amqpurl = amqpurl

        uid = str(uuid.uuid1())
        proxy = XMLRPCClient(self.__baseurl, allow_none=True)

        kwargs = {"uid": uid, "failfast": failfast, "context": context.__dict__}
        proxy.newTestRunner(kwargs, False)
        self.runner = XMLRPCTestRunnerProxy("%s/%s" % (self.__baseurl, kwargs["uid"]), allow_none=True)
        self.runner.log_consumer = TestRunnerAMQPLogConsumer(self.__amqpurl, uid)
        for suite_dict in TestTargetLoader(target).to_suite_dicts(defines):
            self.runner.add_suite(suite_dict)

    def run(self):
        import time
        import socket
        from xmlrpclib import ProtocolError

        self.runner.log_consumer.start()
        self.runner.register()

        try:
            while not self.runner.is_stopped():
                time.sleep(1.0)
        except (socket.error, RuntimeError, ProtocolError):
            logger.exception("")
        except KeyboardInterrupt:
            logger.warn("KeyboardInterrupt. The runner will be stopped after current running test case finished")
            try:
                self.runner.abort()
                self.runner.join()
            except socket.error:
                logger.exception("")
        finally:
            self.runner.log_consumer.stop()

if __name__ == "__main__":
    pass