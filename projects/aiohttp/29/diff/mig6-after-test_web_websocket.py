import pytest
from aiohttp import WebSocketResponse

def test_write_non_prepared():
    ws = WebSocketResponse()
    with pytest.raises(RuntimeError):
        ws.write(b'data')