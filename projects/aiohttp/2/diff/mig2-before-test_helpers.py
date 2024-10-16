import unittest
from aiohttp import helpers

class TestHelpers(unittest.TestCase):

    def test_basic_auth(self):
        # missing password here
        self.assertRaises(
            ValueError, helpers.BasicAuth, None)
        self.assertRaises(
            ValueError, helpers.BasicAuth, 'nkim', None)
        auth = helpers.BasicAuth('nkim')
        self.assertEqual(auth.login, 'nkim')
        self.assertEqual(auth.password, '')
        auth = helpers.BasicAuth('nkim', 'pwd')
        self.assertEqual(auth.login, 'nkim')
        self.assertEqual(auth.password, 'pwd')
        self.assertEqual(auth.encode(), 'Basic bmtpbTpwd2Q=')