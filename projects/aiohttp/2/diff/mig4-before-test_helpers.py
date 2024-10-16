import unittest
from aiohttp import helpers

class TestHelpers(unittest.TestCase):

    def test_reify(self):
        class A:
            @helpers.reify
            def prop(self):
                return 1
        a = A()
        self.assertEqual(1, a.prop)

    def test_reify_class(self):
        class A:
            @helpers.reify
            def prop(self):
                """Docstring."""
                return 1
        self.assertIsInstance(A.prop, helpers.reify)
        self.assertEqual('Docstring.', A.prop.__doc__)

    def test_reify_assignment(self):
        class A:
            @helpers.reify
            def prop(self):
                return 1
        a = A()
        with self.assertRaises(AttributeError):
            a.prop = 123