import unittest
from aiohttp import helpers

class TestHelpers(unittest.TestCase):

    def test_reify_assignment(self):
        class A:
            @helpers.reify
            def prop(self):
                return 1
        a = A()
        with self.assertRaises(AttributeError):
            a.prop = 123