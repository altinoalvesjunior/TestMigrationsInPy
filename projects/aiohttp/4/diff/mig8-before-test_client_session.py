import unittest
from aiohttp.client import ClientSession
from aiohttp.multidict import CIMultiDict

class TestClientSession(unittest.TestCase):

    def test_merge_headers_with_list_of_tuples(self):
        session = ClientSession(
            headers={
                "h1": "header1",
                "h2": "header2"
            }, loop=self.loop)
        headers = session._prepare_headers([("h1", "h1")])
        self.assertIsInstance(headers, CIMultiDict)
        self.assertEqual(headers, CIMultiDict([
            ("h2", "header2"),
            ("h1", "h1")
        ]))
        session.close()