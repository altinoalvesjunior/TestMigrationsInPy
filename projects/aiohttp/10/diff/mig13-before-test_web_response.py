import unittest
from aiohttp.web import StreamResponse
import datetime

def test_last_modified_string(self):
    resp = StreamResponse()

    dt = datetime.datetime(1990, 1, 2, 3, 4, 5, 0, datetime.timezone.utc)
    resp.last_modified = 'Mon, 2 Jan 1990 03:04:05 GMT'
    assert resp.last_modified == dt