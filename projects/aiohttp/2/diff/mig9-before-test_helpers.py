import unittest
from aiohttp import helpers

class TestHelpers(unittest.TestCase):

    def test_reify_class(self):
        class A:
            @helpers.reify
            def prop(self):
                """Docstring."""
                return 1
        self.assertIsInstance(A.prop, helpers.reify)
        self.assertEqual('Docstring.', A.prop.__doc__)