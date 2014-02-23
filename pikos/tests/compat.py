import sys

__all__ = ['TestCase']

if sys.version_info[:2] == (2, 6):
    import contextlib
    from unittest import TestCase as BaseTestCase

    class SkipException(Exception):
        pass

    class TestCase(BaseTestCase):

        def assertIs(self, a, b):
            self.assertTrue(a is b)

        def assertIsNot(self, a, b):
            self.assertTrue(a is not b)

        def assertIsNone(self, a):
            self.assertTrue(a is None)

        def assertIsNotNone(self, a):
            self.assertTrue(a is not None)

        def assertIn(self, a, b):
            self.assertTrue(a in b)

        def assertNotIn(self, a, b):
            self.assertTrue(a not in b)

        def assertIsInstance(self, a, b):
            self.assertTrue(isinstance(a, b))

        def assertNotIsInstance(self, a, b):
            self.assertTrue(not isinstance(a, b))

        def assertSequenceEqual(self, a, b, msg=None, seq_type=None):
            return self.assertEqual(tuple(a), tuple(b), msg=msg)

        def assertMultiLineEqual(self, a, b, msg=None):
            return self.assertEqual(a, b, msg=msg)

        @contextlib.contextmanager
        def failUnlessRaises(self, error, *args):
            if len(args) == 0:
                try:
                    yield
                except error:
                    pass
                else:
                    self.fail('{0} was not raised'.format(error))
            else:
                super(TestCase, self).failUnlessRaises(error, *args)
        assertRaises = failUnlessRaises

        def run(self, result=None):
            if result is None:
                error_count = 0
            else:
                error_count = len(result.errors)
            BaseTestCase.run(self, result)
            if result is not None:
                errors = result.errors
                skip_error = (
                    'in skipTest\n    raise SkipException(msg)'
                    '\nSkipException:')
                result.errors = [
                    error for error in errors
                    if skip_error not in error[1]]
            return result

        def skipTest(self, msg):
            raise SkipException(msg)

else:
    from unittest import TestCase
