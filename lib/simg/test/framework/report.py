#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import collections
"""
<TestReport>
    <Summary></Summary>
    <Comment></Comment>
    <ConfigFile></ConfigFile>
    <OverallTime></OverallTime>
    <TestSuite>
        <Name>New WVAN name Test Suite (SUITE_1)</Name>
        <TotalTests></TotalTests>
        <Failures></Failures>
        <Warnings></Warnings>
        <Errors></Errors>
        <Summary>Total Tests:100. Passed:78. Failures:22. Warnings:0. Suite Fail Rate: 22.0%. Suite Warning Rate: 0.0%</Summary>
        <SINK1_SW_VERSION/>
        <SRC1_SW_VERSION/>
        <SSSERVER_SW_VERSION/>
        <RepeatedTestStatistics>
            <Name></Name>
            <TotalTests></TotalTests>
            <Failures></Failures>
            <Warnings></Warnings>
            <AverageStatistics>associa
            <FailRate></FailRate>te time</AverageStatistics>
            <AverageStatistics>connect time</AverageStatistics>
            <AverageStatistics>total time</AverageStatistics>
        </RepeatedTestStatistics>
        <Test>
            <Number></Number>
            <Name></Name>
            <Title></Title>
            <TestLog></TestLog>
            <UevnetLog></UevnetLog>
            <Comment></Comment>
            <Comment></Comment>
            <Comment></Comment>
            <Result></Result>
        </Test>
    </TestSuite>
</TestReport>
"""
import os
import re

from xml.etree import ElementTree
from simg import fs
from simg.xml import transform
from simg.xml.dom import minidom

from .result import TestCaseResultRecord, TestSuiteResultRecord


class Template(object):
    """
    Forked from https://pypi.python.org/pypi/HTMLTestRunner/0.8.0

    Define a HTML template for report customerization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    DEFAULT_TITLE = 'Test Report'
    DEFAULT_DESCRIPTION = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    %(stylesheet)s
</head>
<body>
<script language="javascript" type="text/javascript"><!--
output_list = Array();

/* level - 0:Summary; 1:Failed; 2:All */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level < 1) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level > 1) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
    }
}


function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        tid0 = 't' + cid.substr(1) + '.' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        if (toHide) {
            document.getElementById('div_'+tid).style.display = 'none'
            document.getElementById(tid).className = 'hiddenRow';
        }
        else {
            document.getElementById(tid).className = '';
        }
    }
}


function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
}


function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}
--></script>

%(heading)s
%(report)s
%(ending)s

</body>
</html>
"""  # variables: (title, generator, stylesheet, heading, report, ending)

    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">
    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
table       { font-size: 100%; }
pre         { }

/* -- heading ---------------------------------------------------------------------- */
h1 {
    font-size: 16pt;
    color: gray;
}
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .attribute {
    margin-top: 1ex;
    margin-bottom: 0;
}

.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}

/* -- css div popup ------------------------------------------------------------------------ */
a.popup_link {
}

a.popup_link:hover {
    color: red;
}

.popup_window {
    display: none;
    position: relative;
    left: 0px;
    top: 0px;
    /*border: solid #627173 1px; */
    padding: 10px;
    background-color: #E6E6D6;
    font-family: "Lucida Console", "Courier New", Courier, monospace;
    text-align: left;
    font-size: 8pt;
    width: 600px;
}

}
/* -- report ------------------------------------------------------------------------ */
#show_detail_line {
    margin-top: 3ex;
    margin-bottom: 1ex;
}
#result_table {
    width: 80%;
    border-collapse: collapse;
    border: 1px solid #777;
}
#header_row {
    font-weight: bold;
    color: white;
    background-color: #777;
}
#result_table td {
    border: 1px solid #777;
    padding: 2px;
}
#total_row  { font-weight: bold; }
.passClass  { background-color: #66cc66; }
.warnClass  { background-color: #ffcc00; }
.failClass  { background-color: #cc6600; }
.errorClass { background-color: #cc0000; }
.skipClass { background-color: #d9d9d9; }
.passCase   { color: #66cc66; }
.warnCase  { color: #ffcc00; font-weight: bold; }
.failCase   { color: #cc6600; font-weight: bold; }
.errorCase  { color: #cc0000; font-weight: bold; }
.skipCase  { color: #d9d9d9; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }


/* -- ending ---------------------------------------------------------------------- */
#ending {
}

</style>
"""

    # ------------------------------------------------------------------------
    # Heading

    HEADING_TMPL = """<div class='heading'>
<h1>%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>
"""     # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
"""     # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #
    REPORT_TMPL = """
<p id='show_detail_line'>Show
<a href='javascript:showCase(2)'>All</a>
<a href='javascript:showCase(0)'>Summary</a>
<a href='javascript:showCase(1)'>Failed</a>
<a href='javascript:showCase(3)'>Warning</a>
<a href='javascript:showCase(4)'>Skipped</a>

</p>
<table id='result_table'>
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>Test Suites</td>
    <td>Count</td>
    <td>Pass</td>
    <td>Warn</td>
    <td>Fail</td>
    <td>Error</td>
    <td>Skip</td>
    <td>View</td>
</tr>
%(test_list)s
<tr id='total_row'>
    <td>Total</td>
    <td>%(Count)s</td>
    <td>%(Pass)s</td>
    <td>%(Warn)s</td>
    <td>%(Fail)s</td>
    <td>%(Error)s</td>
    <td>%(Skip)s</td>
    <td>&nbsp;</td>
</tr>
</table>
"""     # variables: (test_list, Count, Pass, Warn, Fail, Error, Skip)

    REPORT_SUITE_TMPL = r"""
<tr class='%(Style)s'>
    <td>%(Name)s</td>
    <td>%(Count)s</td>
    <td>%(Pass)s</td>
    <td>%(Warn)s</td>
    <td>%(Fail)s</td>
    <td>%(Error)s</td>
    <td>%(Skip)s</td>
    <td><a href="javascript:showClassDetail('%(cid)s',%(Count)s)">Detail</a></td>
</tr>
"""

    REPORT_CASE_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(Style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='7' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
        %(status)s</a>

    <div id='div_%(tid)s' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_%(tid)s').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        %(script)s
        </pre>
    </div>
    <!--css div popup end-->
    </td>
</tr>
"""

    REPORT_CASE_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(Style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>%(status)s</td>
</tr>
"""     # variables: (tid, Class, style, desc, status)

    REPORT_CASE_OUTPUT_TMPL = r"""
%(id)s: %(output)s
"""     # variables: (id, output)

    # ------------------------------------------------------------------------
    # ENDING
    #
    ENDING_TMPL = """<div id='ending'>&nbsp;</div>"""

# -------------------- The end of the Template class -------------------


from xml.sax import saxutils
from result import TestResult


class HTMLTestReport(Template):
    STATUS = {TestCaseResultRecord.Status.PASSED: "Pass",
              TestCaseResultRecord.Status.WARNING: "Warn",
              TestCaseResultRecord.Status.FAILED: "Fail",
              TestCaseResultRecord.Status.ERRONEOUS: "Error",
              TestCaseResultRecord.Status.SKIPPED: "Skip"}

    def __init__(self, result, title=None, description=None):
        if not isinstance(result, TestResult):
            raise TypeError("%s is not an instance of TestResult" % result)
        self._result = result
        self._title = title or Template.DEFAULT_TITLE
        self._description = description or Template.DEFAULT_DESCRIPTION

    def _get_case_states_in_suite(self, suite_record):
        states = {"Pass": 0, "Warn": 0, "Fail": 0, "Error": 0, "Skip": 0}
        for record in suite_record.subrecords:
            if isinstance(record, TestCaseResultRecord):
                states[self.STATUS[record.status]] += 1
        return states

    def _generate_report(self):
        rows = []
        for cid, suite_record in enumerate(self._result.suite_records):
            states = self._get_case_states_in_suite(suite_record)
            row = self.REPORT_SUITE_TMPL % dict(
                Style=states["Error"] > 0 and 'errorClass'
                      or states["Fail"] > 0 and 'failClass'
                      or states["Warn"] > 0 and 'warnClass'
                      or states["Skip"] > 0 and 'skipClass'
                      or 'passClass',
                Name=suite_record.name,
                Count=sum(states.values()),
                cid='c%s' % (cid+1),
                **states
            )
            rows.append(row)
            for tid, record in enumerate(suite_record.subrecords):
                if isinstance(record, TestCaseResultRecord):
                    rows.append(self._generate_case_report(cid, tid, record))
                elif isinstance(record, TestSuiteResultRecord):
                    rows.append(self._generate_suite_report(record))
                else:
                    pass

        report = self.REPORT_TMPL % dict(
            test_list=''.join(rows),
            Count=self._result.testsRun,
            Pass=len(self._result.successes),
            Warn=len(self._result.warnings),
            Fail=len(self._result.failures),
            Error=len(self._result.errors),
            Skip=len(self._result.skipped),
        )
        return report

    def _generate_suite_report(self, suite_record):
        pass

    def _generate_case_report(self, cid, tid, case_record):
        tid = (case_record.status == TestCaseResultRecord.Status.PASSED and 'p' or 'f') + 't%s.%s' % (cid+1, tid+1)
        output = case_record.error[2] if case_record.error else ""

        script = self.REPORT_CASE_OUTPUT_TMPL % dict(
            id=tid,
            output=saxutils.escape(output)
        )
        row = self.REPORT_CASE_WITH_OUTPUT_TMPL % dict(
            tid=tid,
            Class=case_record.status == TestCaseResultRecord.Status.PASSED and 'hiddenRow' or 'none',
            Style=case_record.status == TestCaseResultRecord.Status.ERRONEOUS and 'errorCase'
                  or case_record.status == TestCaseResultRecord.Status.FAILED and 'failCase'
                  or case_record.status == TestCaseResultRecord.Status.WARNING and 'warnCase'
                  or case_record.status == TestCaseResultRecord.Status.SKIPPED and 'skipCase'
                  or 'none',
            desc=case_record.name,
            script=script,
            status=self.STATUS[case_record.status]
        )
        return row

    def _generate_heading(self):
        counts = list()
        counts.append('All %s' % self._result.testsRun)
        counts.append('Pass %s' % len(self._result.successes))
        counts.append('Warn %s' % len(self._result.warnings))
        counts.append('Fail %s' % len(self._result.failures))
        counts.append('Error %s' % len(self._result.errors))
        counts.append('Skip %s' % len(self._result.skipped))
        summary = ', '.join(counts)

        starttime = str(self._result.starttime)[:19]
        duration = str(self._result.stoptime - self._result.starttime)

        a_lines = []
        for name, value in [('Summary', summary), ('Start Time', starttime), ('Duration', duration)]:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value)
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(self._title),
            parameters=''.join(a_lines),
            description=saxutils.escape(self._description),
        )
        return heading

    def to_string(self):
        stylesheet = self.STYLESHEET_TMPL
        heading = self._generate_heading()
        report = self._generate_report()
        ending = self.ENDING_TMPL
        output = self.HTML_TMPL % dict(
            title=saxutils.escape(self._title),
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
        )
        return output

    def save_as_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.to_string())


class JUnit4XMLTestReport(object):
    def __init__(self, result):
        self.__result = result

    def to_etree_element(self):
        testsuites_element = ElementTree.Element("testsuites")
        for suite_record in self.__result.suite_records:
            testsuites_element.append(self.__class__.__generate_testsuite_element(suite_record))
        return testsuites_element

    def save(self, filename):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            fs.mkpath(dirname)
        s = ElementTree.tostring(self.to_etree_element())
        with open(filename, "w") as fdst:
            fdst.write(minidom.parseString(s).toprettyxml())

    @classmethod
    def __generate_testsuite_element(cls, suite_record):
        testsuite_element = ElementTree.Element("testsuite")
        testsuite_element.set("name", suite_record.name)
        for case_record in suite_record.subrecords:
            testsuite_element.append(cls.__generate_testcase_element(case_record))

    @classmethod
    def __generate_testcase_element(cls, case_record):
        testcase_element = ElementTree.Element("testcase")
        testcase_element.set("name", case_record.name)
        testcase_element.set("classname", case_record.clsname)
        testcase_element.set("status", case_record.STATUS_MAPPER[case_record.status])
        testcase_element.set("time", case_record.duration)
        if case_record.status == case_record.Status.SKIPPED:
            skipped_element = ElementTree.Element("skipped")
            skipped_element.text = case_record.skipreason
            testcase_element.append(skipped_element)


class TestReport(object):
    def __init__(self, result):
        self.results = {"1": "PASSED",
          "2": "WARNING",
          "3": "FAILED",
          "4": "SKIPPED",
          "5": "ERRONEOUS"}
        self._runner_result = result
        self._suiteresults = []
        if not result.suite_records:
            raise NameError

        for record in self.to_listed_suite_records(result.suite_records):
            fail_count = 0
            warn_count = 0
            suiteresult = {"suitename": record.name, "testresults": []}
            if not record.subrecords:
                continue
            name = ""
            index = 1
            #record.subrecords = sorted(record.subrecords,key = lambda x:x.name)
            for subrecord in record.subrecords:
                #print subrecord.__dict__
                testresult = dict()
                testresult["title"] = subrecord.name + " #" + str(subrecord.cycleindex)
                testresult["name"] = subrecord.name
                if not name:
                    name = testresult["name"]
                if name == testresult["name"]:
                    index += 1
                else:
                    index = 1
                testresult["result"] = self.results[str(subrecord.status)]

                comments = []
                for checkpoint in subrecord.checkpoints:
                    comment = "CheckPoint: %s, Result: %s" % (checkpoint["name"],
                                                              self.results[str(checkpoint["status"])])
                    comments.append(comment)

                if subrecord.skipreason is not None:
                    comments.append("SkipReason: %s" % subrecord.skipreason)

                if subrecord.error is not None:
                    comments.append("FailReason: %s %s" % (subrecord.error[0].__name__, subrecord.error[1]))
                testresult["comments"] = comments

                for concern_name, concern_value in subrecord.concerns.items():
                    comments.append("%s: %s" % (concern_name, concern_value))

                if testresult["result"] == "FAILED":
                    fail_count += 1
                elif testresult["result"] == "WARNING":
                    warn_count += 1
                else:
                    pass
                suiteresult["testresults"].append(testresult)
            self._suiteresults.append(suiteresult)

    @staticmethod
    def to_listed_suite_records(suite_records):
        l = []

        def expand(suite_record):
            need_removed_subrecords = []
            for subrecord in suite_record.subrecords:
                if isinstance(subrecord, TestSuiteResultRecord):
                    l.append(subrecord)
                    expand(subrecord)
                    need_removed_subrecords.append(subrecord)
            for need_removed_subrecord in need_removed_subrecords:
                suite_record.subrecords.remove(need_removed_subrecord)

        for suite_record in suite_records:
            l.append(suite_record)
            expand(suite_record)
        return l

    def genXMLReport(self, dstFilename):
        self._dom = minidom.getDOMImplementation()
        self._doc = self._dom.createDocument(None, "TestReport", None)
        self._rootelement = self._doc.documentElement
        all_totaltests = 0
        all_failures = 0
        all_warnings = 0
        tests_number = 0
        for suiteresult in self._suiteresults:
            suite_totaltests = 0
            suite_failures = 0
            suite_warnings = 0
            suiteName = suiteresult["suitename"]
            suiteElement = self._rootelement.addSubElement("TestSuite")
            suiteElement.addSubElement("Name").addTextNode(suiteName)
            
            repeatedTestStatistics = collections.OrderedDict()
            for testresult in suiteresult["testresults"]:
                suite_totaltests += 1
                
                if testresult["name"] not in repeatedTestStatistics:
                    repeatedTestStatistics[testresult["name"]] = {"case_totaltests": 1,
                                                                  "statistics": collections.OrderedDict(),
                                                                  "case_failures": 0,
                                                                  "case_warnings": 0
                                                                  }
                else:
                    repeatedTestStatistics[testresult["name"]]["case_totaltests"] += 1
                
                testElement = suiteElement.addSubElement("Test")
                #match = re.search("(\d+)$", testresult["title"])
                #if match:
                #    number = match.group(1)
                tests_number += 1
                testElement.addSubElement("Number").addTextNode(str(tests_number))
                
                testElement.addSubElement("Title").addTextNode(testresult["title"])
                testElement.addSubElement("Name").addTextNode(testresult["name"])
                
                for comment in testresult["comments"]:
                    testElement.addSubElement("Comment").addTextNode(comment)
                
                if testresult["result"] == "FAILED":
                    suite_failures += 1
                    repeatedTestStatistics[testresult["name"]]["case_failures"] += 1
                elif testresult["result"] == "WARNING":
                    suite_warnings += 1
                    repeatedTestStatistics[testresult["name"]]["case_warnings"] += 1
                else:
                    pass
                
                testElement.addSubElement("Result").addTextNode(testresult["result"].upper())

            for key, value in repeatedTestStatistics.items():
                if value["case_totaltests"] == 1:
                    continue
                statisticsElement = suiteElement.addSubElement("RepeatedTestStatistics")
                statisticsElement.addSubElement("Name").addTextNode(key)
                statisticsElement.addSubElement("TotalTests").addTextNode(str(value["case_totaltests"]))
                statisticsElement.addSubElement("Failures").addTextNode(str(value["case_failures"]))
                statisticsElement.addSubElement("Warnings").addTextNode(str(value["case_warnings"]))
            
                failrate = round(float(value["case_failures"]) / float(value["case_totaltests"]), 3) * 100
                statisticsElement.addSubElement("FailRate").addTextNode(str(failrate) + "%")
                
                for stakey, stavalue in repeatedTestStatistics[key]["statistics"].items():
                    if stavalue:
                        statisticsElement.addSubElement("AverageStatistics").addTextNode("%s: %s" % (stakey, sum(stavalue) / len(stavalue)))
                
            
            suiteElement.addSubElement("TotalTests").addTextNode(str(suite_totaltests))
            suiteElement.addSubElement("Failures").addTextNode(str(suite_failures))
            suiteElement.addSubElement("Warnings").addTextNode(str(suite_warnings))

            failrate = round(float(suite_failures) / float(suite_totaltests), 3) * 100
            warnrate = round(float(suite_warnings) / float(suite_totaltests), 3) * 100
            summary = "Total Tests:%s. Failures:%s. Warnings:%s. Fail Rate: %s%%. Warning Rate: %s%%" % (suite_totaltests, suite_failures, suite_warnings, failrate, warnrate)
            suiteElement.addSubElement("Summary").addTextNode(summary)
            
            all_totaltests += suite_totaltests
            all_failures += suite_failures
            all_warnings += suite_warnings

        failrate = round(float(all_failures) / float(all_totaltests), 3) * 100
        warnrate = round(float(all_warnings) / float(all_totaltests), 3) * 100
        summary = "Total Tests:%s. Failures:%s. Warnings:%s. Suite Fail Rate: %s%%. Suite Warning Rate: %s%%" % (all_totaltests, all_failures, all_warnings, failrate, warnrate)            
        self._rootelement.addSubElement("Summary").addTextNode(summary)
        self._rootelement.addSubElement("OverallTime").addTextNode(str(self._runner_result.stoptime-self._runner_result.starttime))
        
        with open(dstFilename, "w") as fdst:
            fdst.write(self._doc.toprettyxml())
    

    def genHTMLReport(self, srcFilename, dstFilename):
        dirname = os.path.dirname(__file__)
        transformer = transform.TransformerFactory.netTransformer(os.path.join(dirname, "report.xsl"))
        transformer.applyStylesheetOnFile(srcFilename)
        transformer.saveResultToFilename(dstFilename)
        pass


import simg.util.text as Text
class BADriverTestReport(object):    
    def __init__(self):
        self._suiteresults = []
        self._txteditor = Text.TextEditor()
        self._statisticsCommentPrefixes = {
            "B&A driver off to mhl mode test": ["mode change from mhl to off", "mode change from off to mhl"],
            "B&A driver off to wihd mode test": ["mode change from wihd to off", "mode change from off to wihd"],
            "B&A driver associated to off mode test": ["mode change from wihd associated to off"],
            "B&A driver associated to mhl mode test": ["mode change from wihd associated to mhl"],
            "B&A driver connected to mhl mode test": ["associate duration time", "connect duration time"],
            "B&A driver connected to off mode test": ["mode change from wihd connect to off"],
            "B&A driver wihd mode idle to mhl mode test": ["mode change from wihd idle to mhl", "mode change from mhl to wihd idle"],
            "B&A driver wvan_scan to off mode test": ["mode change from wihd scan to off"],
            "B&A driver wvan_scan to mhl mode test": ["mode change from wihd scan to mhl"],
            
            # TODO:
            "B&A driver interval scan from idle test": ["scan start uevent send out after command issued"],
            "B&A driver interval scan from scan test": [],
            "B&A driver scan from idle test": ["unit scan duration", "scan start uevent send out after command issued"],
            "B&A driver scan from scan test": [],
            "B&A driver scan stop test": [],
            
            # TODO:
            "B&A driver search between connect disconnect test": [],
            "B&A driver search from associated test": [],
            
            "B&A driver join from idle test": ["associate duration"],
            "B&A driver join from period scan test": [],

            "B&A driver connect/disconnect remote read test": ["connect duration time"],
            "B&A driver mac address connect/disassociate test": ["associate duration time", "connect duration time"],
            "B&A A1 driver mac address connect/disconnect test" : ["connect duration time"],
            "B&A driver mac address connect/disconnect and disassociate test": ["associate duration time", "connect duration time"],
            "B&A driver connected remote read test": ["connect duration time"],

            "B&A driver factory test": ["associate time", "temperature_a", "connect time", "temperature_b", "the time cost between fm_test_mode and connected", "hr link quality"],
            "B&A driver get associate and connect time test": ["associate time", "connect time"],
            "B&A driver get reconnect time test": ["reconnect time"],
        }
        
    def addLogForParsing(self, logfile, suitename):
        suiteExists = False
        suiteResult = {"suitename": suitename, "testresults": []}
        
        for result in self._suiteresults:
            if result["suitename"] == suitename:
                suiteExists = True
                suiteResult = result
                break

        fail_count = 0
        warn_count = 0
        
        self._txteditor.load(logfile)
        titlelines = self._txteditor.search(r"TEST_TITLE: ")

        for titleline in titlelines:
            testresult = {}
            match = re.search(r"TEST_TITLE: ((.*test).*)", titleline)
            testresult["title"] = match.group(1).strip()
            testresult["name"] = match.group(2).strip()

            resultlines = self._txteditor.search(r"%s_TEST_RESULT: " % testresult["title"])
            match = re.search(r"%s_TEST_RESULT: (.*)" % testresult["title"], resultlines[0])
            testresult["result"] = match.group(1).strip()
            
            if testresult["result"] == "failed":
                fail_count += 1
            elif testresult["result"] == "warning":
                warn_count += 1
            else:
                pass
            
            commentlines = self._txteditor.search(r"%s_TEST_COMMENT: " % testresult["title"])
            comments = []
            for commentline in commentlines:
                match = re.search(r"%s_TEST_COMMENT: (.*)\r?" % testresult["title"], commentline)
                comment = match.group(1)
                if comment[0] == "[" and comment[-1] == "]":
                    comms = eval(comment)
                    for comm in comms:
                        comments.append(str(comm))
                else:
                    comments.append(comment)
            testresult["comments"] = comments
            
            suiteResult["testresults"].append(testresult)

        if not suiteExists:
            self._suiteresults.append(suiteResult)

    
    def genXMLReport(self, dstFilename):
        self._dom = minidom.getDOMImplementation()
        self._doc = self._dom.createDocument(None, "TestReport", None)
        self._rootelement = self._doc.documentElement
        all_totaltests = 0
        all_failures = 0
        all_warnings = 0
        for suiteresult in self._suiteresults:
            suite_totaltests = 0
            suite_failures = 0
            suite_warnings = 0
            suiteName = suiteresult["suitename"]
            suiteElement = self._rootelement.addSubElement("TestSuite")
            suiteElement.addSubElement("Name").addTextNode(suiteName)
            
            repeatedTestStatistics = collections.OrderedDict()
            for testresult in suiteresult["testresults"]:
                suite_totaltests += 1
                
                if testresult["name"] not in repeatedTestStatistics:
                    repeatedTestStatistics[testresult["name"]] = {"case_totaltests": 1,
                                                                  "statistics": collections.OrderedDict(),
                                                                  "case_failures": 0,
                                                                  "case_warnings": 0
                                                                  }
                else:
                    repeatedTestStatistics[testresult["name"]]["case_totaltests"] += 1
                
                testElement = suiteElement.addSubElement("Test")
                match = re.search("(\d+)$", testresult["title"])
                if match:
                    number = match.group(1)
                    testElement.addSubElement("Number").addTextNode(number)
                
                testElement.addSubElement("Title").addTextNode(testresult["title"])
                testElement.addSubElement("Name").addTextNode(testresult["name"])
                
                for comment in testresult["comments"]:
                    testElement.addSubElement("Comment").addTextNode(comment)
                    if testresult["name"] in self._statisticsCommentPrefixes:
                        filtercomments = self._statisticsCommentPrefixes[testresult["name"]]
                    else:
                        filtercomments = []
                    if testresult["result"] != "failed" and filter(lambda x: x in comment, filtercomments):
                        if "issued" in comment:
                            if "[" in comment and "]" in comment:
                                match = re.search(r"(.* issued) (\[[\.\d,]+\])s", comment)
                                name = match.group(1)
                                values = eval(match.group(2))
                                value = sum(values) / len(values)
                            else:
                                match = re.search(r"(.* issued) ([\.\d]+)", comment)
                                name = match.group(1)
                                value = match.group(2)
                        else:
                            match = re.search(r"(.*)(?: is|[ ]?:) ([\.\d]+)", comment)
                            name = match.group(1)
                            value = match.group(2)
                        if name in repeatedTestStatistics[testresult["name"]]["statistics"]:
                            repeatedTestStatistics[testresult["name"]]["statistics"][name].append(float(value))
                        else:
                            repeatedTestStatistics[testresult["name"]]["statistics"][name] = list()
                
                if testresult["result"] == "failed":
                    suite_failures += 1
                    repeatedTestStatistics[testresult["name"]]["case_failures"] += 1
                elif testresult["result"] == "warning":
                    suite_warnings += 1
                    repeatedTestStatistics[testresult["name"]]["case_warnings"] += 1
                else:
                    pass
                
                testElement.addSubElement("Result").addTextNode(testresult["result"].upper())

            for key, value in repeatedTestStatistics.items():
                if value["case_totaltests"] == 1:
                    continue
                statisticsElement = suiteElement.addSubElement("RepeatedTestStatistics")
                statisticsElement.addSubElement("Name").addTextNode(key)
                statisticsElement.addSubElement("TotalTests").addTextNode(str(value["case_totaltests"]))
                statisticsElement.addSubElement("Failures").addTextNode(str(value["case_failures"]))
                statisticsElement.addSubElement("Warnings").addTextNode(str(value["case_warnings"]))
            
                failrate = round(float(value["case_failures"]) / float(value["case_totaltests"]), 3) * 100
                statisticsElement.addSubElement("FailRate").addTextNode(str(failrate) + "%")
                
                for stakey, stavalue in repeatedTestStatistics[key]["statistics"].items():
                    if stavalue:
                        statisticsElement.addSubElement("AverageStatistics").addTextNode("%s: %s" % (stakey, sum(stavalue) / len(stavalue)))
                
            
            suiteElement.addSubElement("TotalTests").addTextNode(str(suite_totaltests))
            suiteElement.addSubElement("Failures").addTextNode(str(suite_failures))
            suiteElement.addSubElement("Warnings").addTextNode(str(suite_warnings))

            failrate = round(float(suite_failures) / float(suite_totaltests), 3) * 100
            warnrate = round(float(suite_warnings) / float(suite_totaltests), 3) * 100
            summary = "Total Tests:%s. Failures:%s. Warnings:%s. Fail Rate: %s%%. Warning Rate: %s%%" % (suite_totaltests, suite_failures, suite_warnings, failrate, warnrate)
            suiteElement.addSubElement("Summary").addTextNode(summary)
            
            all_totaltests += suite_totaltests
            all_failures += suite_failures
            all_warnings += suite_warnings

        failrate = round(float(all_failures) / float(all_totaltests), 3) * 100
        warnrate = round(float(all_warnings) / float(all_totaltests), 3) * 100
        summary = "Total Tests:%s. Failures:%s. Warnings:%s. Suite Fail Rate: %s%%. Suite Warning Rate: %s%%" % (all_totaltests, all_failures, all_warnings, failrate, warnrate)            
        self._rootelement.addSubElement("Summary").addTextNode(summary)

        
        with open(dstFilename, "w") as fdst:
            fdst.write(self._doc.toprettyxml())
    

    def genHTMLReport(self, srcFilename, dstFilename):
        dirname = os.path.dirname(__file__)
        transformer = transform.TransformerFactory.netTransformer(os.path.join(dirname, "report.xsl"))
        transformer.applyStylesheetOnFile(srcFilename)
        transformer.saveResultToFilename(dstFilename)

    
if __name__ == "__main__":
    tr = BADriverTestReport()
#     tr.addLogForParsing(r"W:\SQA\TestReports\B&A\Android\SVN49318\2014-01-13_17-49-12\factory.log", "factory")
#     tr.addLogForParsing(r"Y:\logs\2014-01-20_09-40-46\flash_sink_fw.log", "ota")
    
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\install.log", "install")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\reinstall.log", "reinstall")
 
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\idle_to_mhl.log", "mode")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\off_to_mhl.log", "mode")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\off_to_wihd.log", "mode")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\connected_to_mhl.log", "mode")    
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\connected_to_off.log", "mode") 
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\associated_to_off.log", "mode")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\associated_to_mhl.log", "mode")
 
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\intervscan_from_idle.log", "scan")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\intervscan_from_scan.log", "scan")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\scan_from_idle.log", "scan")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\scan_from_scan.log", "scan")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\scan_stop.log", "scan")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\scan_to_mhl.log", "scan")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\scan_to_off.log", "scan")
 
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\search_between_connect_disconnect.log", "search")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\search_from_associated.log", "search") 
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\search_from_connected.log", "search") 
 
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\join_from_idle.log", "join")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\join_from_periodscan.log", "join") 
 
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\connect_disconnect_remote_read.log", "connect")
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\connect_mac_disassoc.log", "connect")    
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\connect_mac_disconnect_A1.log", "connect") 
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\connect_mac_disconnect_disassoc.log", "connect") 
    tr.addLogForParsing(r"D:\2013-12-03_15-40-07\connected_remote_read.log", "connect")


    tr.genXMLReport("d:/testreport.xml")
    tr.genHTMLReport("d:/testreport.xml", "d:/testreport.html")



