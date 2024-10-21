import unittest
from aiohttp import helpers

class TestAtoms(unittest.TestCase):

    def test_get_seconds_and_milliseconds(self):
        response = dict(status=200, output_length=1)
        request_time = 321.012345678901234
        atoms = helpers.atoms(None, None, response, None, request_time)
        self.assertEqual(atoms['T'], '321')
        self.assertEqual(atoms['D'], '012345')