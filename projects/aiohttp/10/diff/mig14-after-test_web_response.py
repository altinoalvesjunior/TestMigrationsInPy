from aiohttp.web import StreamResponse
import datetime

def test_last_modified_timestamp():
    resp = StreamResponse()

    dt = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

    resp.last_modified = 0
    assert resp.last_modified == dt

    resp.last_modified = 0.0
    assert resp.last_modified == dt