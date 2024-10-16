import pytest
import asyncio
from aiohttp.client import ClientSession
from aiohttp.connector import TCPConnector

def test_connector_loop(loop):
    another_loop = asyncio.new_event_loop()
    connector = TCPConnector(loop=another_loop)
    with pytest.raises(ValueError, match="loop argument must agree with connector"):
        ClientSession(connector=connector, loop=loop)
    connector.close()
    another_loop.close()