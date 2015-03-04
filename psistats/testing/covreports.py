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
    PATH_COVERAGE = os.path.abspath(os.path.dirname(__file__) + "/../../coverage")
    PATH_TESTS    = os.path.abspath(os.path.dirname(__file__) + "/../../tests")
    PATH_ANNOTATED_TESTS = PATH_COVERAGE + "/annotations"
    PATH_REPORTS  = PATH_PROJECT + "/reports"
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
        ('no-xml', None, "do not create XML report files")
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

    def finalize_options(self):
        pass

    def run(self):
        """
        Main command implementation.
        """

        if self.erase:
            try:
                shutil.rmtree(self.PATH_COVERAGE)
            except:
                pass

        try:
            os.makedirs(self.PATH_COVERAGE)
            os.makedirs(self.PATH_ANNOTATED_TESTS)
            os.makedirs(self.PATH_HTML_REPORT)
            os.makedirs(self.PATH_XML_REPORT)
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
                directory=self.PATH_ANNOTATED_TESTS
            )

        if not self.no_html:
            cov.html_report(
                omit=self.FILTERS,
                directory=self.PATH_HTML_REPORT
            )

        if not self.no_xml:
            cov.xml_report(
                omit=self.FILTERS,
                outfile=self.PATH_XML_REPORT + "/coverage.xml"
            )
