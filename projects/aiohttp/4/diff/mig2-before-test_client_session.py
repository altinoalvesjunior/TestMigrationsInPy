import unittest
from aiohttp.client import ClientSession
from aiohttp.multidict import CIMultiDict

class TestClientSession(unittest.TestCase):

    def test_init_headers_list_of_tuples(self):
        session = ClientSession(
            headers=[("h1", "header1"),
                     ("h2", "header2"),
                     ("h3", "header3")],
            loop=self.loop)
        self.assertEqual(
            session._default_headers,
            CIMultiDict([("h1", "header1"),
                         ("h2", "header2"),
                         ("h3", "header3")]))
        session.close()