import unittest
from aiohttp.web import StreamResponse

def test_last_modified_initial(self):
    resp = StreamResponse()
    assert resp.last_modified is None