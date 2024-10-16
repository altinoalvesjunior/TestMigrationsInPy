import pytest
from aiohttp.client import ClientSession

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

@pytest.fixture
def session(create_session):
    return create_session()

def test_close_flag_for_closed_connector(session):
    conn = session.connector
    assert not session.closed
    conn.close()
    assert session.closed