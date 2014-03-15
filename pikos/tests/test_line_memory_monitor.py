import unittest

from pikos.monitors.line_memory_monitor import LineMemoryMonitor
from pikos.recorders.list_recorder import ListRecorder
from pikos.filters.on_value import OnValue
from pikos.tests.test_assistant import TestAssistant
from pikos.tests.compat import TestCase


class TestLineMemoryMonitor(TestCase, TestAssistant):

    def setUp(self):
        self.filename = __file__.replace('.pyc', '.py')
        self.maxDiff = None
        self.recorder = ListRecorder(
            filter_=OnValue('filename', self.filename))
        self.logger = LineMemoryMonitor(self.recorder)

    def test_function(self):
        logger = self.logger

        @logger.attach
        def gcd(x, y):
            while x > 0:
                x, y = y % x, x
            return y

        def boo():
            pass

        boo()
        result = gcd(12, 3)
        boo()
        self.assertEqual(result, 3)

        filename = self.filename

        # note the index depends on this file layout
        expected = [
            "0 gcd 24             while x > 0: {0}".format(filename),
            "1 gcd 25                 x, y = y % x, x {0}".format(filename),
            "2 gcd 24             while x > 0: {0}".format(filename),
            "3 gcd 25                 x, y = y % x, x {0}".format(filename),
            "4 gcd 24             while x > 0: {0}".format(filename),
            "5 gcd 26             return y {0}".format(filename)]
        records = self.get_records(self.recorder)
        self.assertEqual(records, expected)

    def test_recursive(self):
        logger = self.logger

        @logger.attach
        def gcd(x, y):
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            return gcd(7, 12)

        result = boo()
        self.assertEqual(result, 1)

        filename = self.filename

        expected = [
            "0 gcd 54             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "8 gcd 54             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "16 gcd 54             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "24 gcd 54             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "32 gcd 54             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "40 gcd 54             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename)]  # noqa
        records = self.get_records(self.recorder)
        self.assertEqual(records, expected)

    def test_generator(self):
        logger = self.logger
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)

        @logger.attach
        def fibonacci(items):
            x, y = 0, 1
            for i in range(items):
                yield x
                x, y = y, x + y

        def boo():
            pass

        boo()
        result = [value for value in fibonacci(10)]
        boo()
        self.assertSequenceEqual(result, output)
        filename = self.filename

        expected = [
            "0 fibonacci 80             x, y = 0, 1 {0}".format(filename),
            "1 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "2 fibonacci 82                 yield x {0}".format(filename),
            "11 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "12 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "13 fibonacci 82                 yield x {0}".format(filename),
            "22 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "23 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "24 fibonacci 82                 yield x {0}".format(filename),
            "33 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "34 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "35 fibonacci 82                 yield x {0}".format(filename),
            "44 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "45 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "46 fibonacci 82                 yield x {0}".format(filename),
            "55 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "56 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "57 fibonacci 82                 yield x {0}".format(filename),
            "66 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "67 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "68 fibonacci 82                 yield x {0}".format(filename),
            "77 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "78 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "79 fibonacci 82                 yield x {0}".format(filename),
            "88 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "89 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "90 fibonacci 82                 yield x {0}".format(filename),
            "99 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "100 fibonacci 81             for i in range(items): {0}".format(filename),  # noqa
            "101 fibonacci 82                 yield x {0}".format(filename),
            "110 fibonacci 83                 x, y = y, x + y {0}".format(filename),  # noqa
            "111 fibonacci 81             for i in range(items): {0}".format(filename)]  # noqa

        records = self.get_records(self.recorder)
        self.assertEqual(records, expected)

    def test_function_using_tuples(self):
        filename = self.filename
        # tuple records are not compatible with the default OnValue filters.
        recorder = ListRecorder(filter_=lambda x: x[-1] == filename)
        logger = LineMemoryMonitor(recorder, record_type=tuple)

        @logger.attach
        def gcd(x, y):
            while x > 0:
                x, y = y % x, x
            return y

        def boo():
            pass

        boo()
        result = gcd(12, 3)
        boo()
        self.assertEqual(result, 3)
        expected = [
            "0 gcd 139             while x > 0: {0}".format(filename),
            "1 gcd 140                 x, y = y % x, x {0}".format(filename),
            "2 gcd 139             while x > 0: {0}".format(filename),
            "3 gcd 140                 x, y = y % x, x {0}".format(filename),
            "4 gcd 139             while x > 0: {0}".format(filename),
            "5 gcd 141             return y {0}".format(filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)

    def test_issue2(self):
        """ Test for issue #2.

        The issues is reported in `https://github.com/sjagoe/pikos/issues/2`_
        """
        logger = self.logger

        FOO = """
def foo():
    a = []
    for i in range(20):
        a.append(i+sum(a))

foo()
"""

        @logger.attach
        def boo():
            code = compile(FOO, 'foo', 'exec')
            exec code in globals(), {}

        try:
            boo()
        except TypeError:
            msg = ("Issue #2 -- line monitor fails when exec is used"
                   " on code compiled from a string -- exists.")
            self.fail(msg)

    def get_records(self, recorder):
        """ Remove the memory related fields.
        """
        records = []
        for record in recorder.records:
            filtered = record[:3] + record[5:]
            records.append(
                ' '.join([str(item).rstrip() for item in filtered]))
        return records


if __name__ == '__main__':
    unittest.main()
