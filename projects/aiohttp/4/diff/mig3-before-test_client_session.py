import unittest
from aiohttp.client import ClientSession
from aiohttp.multidict import CIMultiDict, MultiDict

class TestClientSession(unittest.TestCase):

    def test_init_headers_MultiDict(self):
        session = ClientSession(
            headers=MultiDict(
                [("h1", "header1"),
                 ("h2", "header2"),
                 ("h3", "header3")]),
            loop=self.loop)
        self.assertEqual(
            session._default_headers,
            CIMultiDict([("H1", "header1"),
                         ("H2", "header2"),
                         ("H3", "header3")]))
        session.close()