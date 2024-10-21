import unittest
from aiohttp import helpers, MultiDict

class TestSafeAtoms(unittest.TestCase):

    def test_get_non_existing(self):
        atoms = helpers.SafeAtoms(
            {}, MultiDict(), MultiDict())
        self.assertEqual(atoms['unknown'], '-')

    def test_get_lower(self):
        i_headers = MultiDict([('test', '123')])
        o_headers = MultiDict([('TEST', '123')])
        atoms = helpers.SafeAtoms({}, i_headers, o_headers)
        self.assertEqual(atoms['{test}i'], '123')
        self.assertEqual(atoms['{test}o'], '-')
        self.assertEqual(atoms['{TEST}o'], '123')
        self.assertEqual(atoms['{UNKNOWN}o'], '-')
        self.assertEqual(atoms['{UNKNOWN}'], '-')