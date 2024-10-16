import pytest
from aiohttp.client import ClientSession
from aiohttp.connector import TCPConnector

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

def test_connector(create_session, loop):
    connector = TCPConnector(loop=loop)
    session = create_session(connector=connector)
    assert session.connector is connector