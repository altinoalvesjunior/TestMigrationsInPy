import unittest
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_init_headers_simple_dict(self):
        session = ClientSession(
            headers={
                "h1": "header1",
                "h2": "header2"
            }, loop=self.loop)
        self.assertEqual(
            sorted(session._default_headers.items()),
            ([("H1", "header1"),
              ("H2", "header2")]))
        session.close()