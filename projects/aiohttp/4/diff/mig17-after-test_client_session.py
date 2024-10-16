import pytest
from aiohttp.client import ClientSession

@pytest.fixture
def connector(loop):
    conn = BaseConnector(loop=loop)
    transp = mock.Mock()
    conn._conns['a'] = [(transp, 'proto', 123)]
    return conn

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

def test_close(create_session, connector):
    session = create_session(connector=connector)
    session.close()
    assert session.connector is None
    assert connector.closed