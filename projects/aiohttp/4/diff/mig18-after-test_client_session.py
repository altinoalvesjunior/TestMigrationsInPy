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

def test_closed(session):
    assert not session.closed
    session.close()
    assert session.closed