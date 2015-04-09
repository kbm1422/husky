#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import inspect
import argparse
import pkgutil
import importlib

import common


def generate_suite_xml(source, output):
    from simg.test.framework import TestModuleLoader
    if isinstance(source, str):
        module = importlib.import_module(source)
    elif inspect.ismodule(source):
        module = source
    else:
        raise ValueError

    parts = module.__name__.split(".")
    imploader = pkgutil.get_loader(module)
    if imploader.is_package(module.__name__):
        for module_loader, name, ispkg in pkgutil.iter_modules(path=module.__path__):
            sub_module = importlib.import_module(module.__name__ + "." + name)
            generate_suite_xml(sub_module, output)
    else:
        if parts[-1].startswith("test"):
            loader = TestModuleLoader(module)
            parts[-1] = "%s.xml" % parts[-1]
            filename = os.path.join(output, *parts[1:])
            loader.save_as_xml(filename)


def generate_report_from_shelve(source):
    import shelve
    from simg.test.framework import TestReport

    runner_log_dir = os.path.dirname(source)

    shd = shelve.open(source, protocol=2)
    try:
        report = TestReport(shd["result"])
        xmlrpt = os.path.join(runner_log_dir, "report.xml")
        htmlrpt = os.path.join(runner_log_dir, "report.html")
        report.genXMLReport(xmlrpt)
        report.genHTMLReport(xmlrpt, htmlrpt)
    finally:
        shd.close()


def main():
    parser = argparse.ArgumentParser(add_help=True)
    subparsers = parser.add_subparsers(dest="utils")

    gsx_subparser = subparsers.add_parser("generate_suite_xml")
    gsx_subparser.add_argument('--module', action='store', dest="module", default="cases")
    gsx_subparser.add_argument('--output', action='store', default=os.path.join(common.bindir, "suites"))

    grs_subparser = subparsers.add_parser("generate_report_from_shelve")
    grs_subparser.add_argument('--shelve', action='store', dest="shelve")
    args = parser.parse_args()

    if args.utils == "generate_suite_xml":
        generate_suite_xml(args.module, args.output)
    elif args.utils == "generate_report_from_shelve":
        generate_report_from_shelve(args.shelve)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )
    main()

