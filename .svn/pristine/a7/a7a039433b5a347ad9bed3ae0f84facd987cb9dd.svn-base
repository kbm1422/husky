#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import time
import argparse
import logging.config

from simg import fs
from simg.test.framework import TestContext
from simg.test.framework import NativeTestTarget, RemoteTestTarget
from bench import TestBenchConfiguration

import common


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--target', dest="target", required=True)
    parser.add_argument('--bench', dest="bench", required=True)
    parser.add_argument('--failfast', action='store_true', dest="failfast", default=False)

    subparsers = parser.add_subparsers(dest="mode")
    native_parser = subparsers.add_parser("native")
    native_parser.add_argument('--logdir', dest="logdir", default=os.path.join(common.logdir,
                                                                               time.strftime("%Y-%m-%d_%H-%M-%S")))
    native_parser.add_argument('--casedir', dest="casedir", default=common.casedir)

    remote_parser = subparsers.add_parser("remote")
    remote_parser.add_argument('--host', dest="host", default="127.0.0.1")
    remote_parser.add_argument('--port', dest="port", type=int, default=5389)
    remote_parser.add_argument('--amqpurl', dest="amqpurl", default="amqp://guest:guest@localhost:5672")
    args, unknown = parser.parse_known_args()

    defines = dict()
    for value in unknown:
        tup = value.replace("-", "").partition("=")
        defines[tup[0]] = tup[2]

    if args.mode == "native":
        fs.mkpath(args.logdir)
        logconf = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '%(asctime)-15s - %(thread)-5d [%(levelname)-8s] - %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'verbose'
                },
                'file_debug': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'filename': os.path.join(args.logdir, "debug.log"),
                    'maxBytes': 50000000,
                    'backupCount': 10
                },
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['console', 'file_debug'],
            }
        }
        logging.config.dictConfig(logconf)
        context = TestContext()
        context.logdir = args.logdir
        context.resource = TestBenchConfiguration(common.resconf).buildTestBenchByName(args.bench)
        target = NativeTestTarget(args.target, args.casedir, args.failfast, context, defines)
        target.run()
    elif args.mode == "remote":
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)-15s - %(thread)-5d [%(levelname)-8s] - %(message)s',
        )
        context = TestContext()
        context.rsrcname = args.bench
        baseurl = "http://%s:%s/husky/xmlrpc/testrunners" % (args.host, args.port)
        target = RemoteTestTarget(args.target, baseurl, args.amqpurl, args.failfast, context, defines)
        target.run()
    else:
        raise ValueError

if __name__ == "__main__":
    main()