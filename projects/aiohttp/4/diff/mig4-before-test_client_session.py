import unittest
from aiohttp.client import ClientSession
from aiohttp.multidict import CIMultiDict

class TestClientSession(unittest.TestCase):

    def test_init_headers_list_of_tuples_with_duplicates(self):
        session = ClientSession(
            headers=[("h1", "header11"),
                     ("h2", "header21"),
                     ("h1", "header12")],
            loop=self.loop)
        self.assertEqual(
            session._default_headers,
            CIMultiDict([("H1", "header11"),
                         ("H2", "header21"),
                         ("H1", "header12")]))
        session.close()