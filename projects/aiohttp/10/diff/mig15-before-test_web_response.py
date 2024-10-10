import unittest
from aiohttp.web import StreamResponse
import datetime

def test_last_modified_datetime(self):
    resp = StreamResponse()

    dt = datetime.datetime(2001, 2, 3, 4, 5, 6, 0, datetime.timezone.utc)
    resp.last_modified = dt
    assert resp.last_modified == dt