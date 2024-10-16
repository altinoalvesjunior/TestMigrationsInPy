import pytest
from aiohttp.client import ClientSession

@pytest.fixture
def connector(loop):
    conn = BaseConnector(loop=loop)
    transp = mock.Mock()
    conn._conns['a'] = [(transp, 'proto', 123)]
    return conn

def test_context_manager(connector, loop):
    with ClientSession(loop=loop, connector=connector) as session:
        pass

    assert session.closed