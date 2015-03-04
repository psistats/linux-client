#! /usr/bin/env python
"""
Code taken from:

http://jeetworks.org/adding-test-code-coverage-analysis-to-a-python-projects-setup-command/
Thanks :-)
"""

import unittest
import shutil
import sys
import os
from psistats.testing import get_test_suite
import distutils.cmd
import coverage

class CoverageAnalysis(distutils.cmd.Command):
    """
    Code coverage analysis command.
    """
    PATH_PROJECT = os.path.abspath(os.path.dirname(__file__) + "/../..")
    PATH_TESTS    = os.path.abspath(os.path.dirname(__file__) + "/../../tests")
    PATH_REPORTS  = PATH_PROJECT + "/reports"
    PATH_ANNOTATED_TESTS = PATH_REPORTS + "/annotations"
    PATH_HTML_REPORT = PATH_REPORTS + "/html"
    PATH_XML_REPORT = PATH_REPORTS + "/xml"

    FILTERS = [
        'psistats/testing/*',
        '*/mock*',
        '*/pika/*',
        'tests/*'
    ]

    description = "run test coverage analysis"

    user_options = [
        ('erase', None, "remove all existing coverage results"),
        ('branch', 'b', 'measure branch coverage in addition to statement coverage'),
        ('test-module=', 't', "explicitly specify a module to test (e.g. 'dendropy.test.test_containers')"),
        ('no-annotate', None, "do not create annotated source code files"),
        ('no-html', None, "do not create HTML report files"),
        ('no-xml', None, "do not create XML report files"),
        ('html-dir=', None, "dir of HTML reports"),
        ('xml-dir=', None, "dir of XML reports"),
        ('annotations-dir=', None, "dir of annotated classes")
    ]

    def initialize_options(self):
        """
        Initialize options to default values.
        """
        self.test_module = None
        self.branch = False
        self.erase = False
        self.no_annotate = False
        self.no_html = False
        self.no_xml = False
        self.html_dir = self.PATH_HTML_REPORT
        self.xml_dir = self.PATH_XML_REPORT
        self.annotations_dir = self.PATH_ANNOTATED_TESTS

    def finalize_options(self):
        pass

    def run(self):
        """
        Main command implementation.
        """

        if self.erase:
            try:
                shutil.rmtree(self.html_dir)
                shutil.rmtree(self.xml_dir)
                shutil.rmtree(self.annotation_dir)
            except:
                pass

        try:
            os.makedirs(self.html_dir)
            os.makedirs(self.xml_dir)
            os.makedirs(self.annotation_dir)
        except:
            pass

        if self.test_module is None:
            test_suite = get_test_suite()
        else:
            test_suite = get_test_suite([self.test_module])

        runner = unittest.TextTestRunner()
        cov = coverage.coverage(branch=self.branch, omit=self.FILTERS)
        cov.start()
        runner.run(test_suite)
        cov.stop()

        if not self.no_annotate:
            cov.annotate(
                omit=self.FILTERS,
                directory=self.annotations_dir
            )

        if not self.no_html:
            cov.html_report(
                omit=self.FILTERS,
                directory=self.html_dir
            )

        if not self.no_xml:
            cov.xml_report(
                omit=self.FILTERS,
                outfile=self.xml_dir + "/coverage.xml"
            )
