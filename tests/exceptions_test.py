import unittest
import mock
import traceback
from psistats import exceptions

class ExceptionTest(unittest.TestCase):
    
    def _stacktrace():
        return "foobar"

    @mock.patch('traceback.format_exc', side_effect=_stacktrace)
    def test_causeAppended(self, mock_format_exc):
        e = exceptions.PsistatsException("first", "second")
        self.assertEquals(e.cause, "second")
        self.assertEquals(e.message, "first, caused by:\nfoobar")

        e = exceptions.PsistatsException("first")
        self.assertEquals(e.message, "first")

