import pytest
from aiohttp.client import ClientSession

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

def test_init_cookies_with_simple_dict(create_session):
    session = create_session(cookies={"c1": "cookie1",
                                      "c2": "cookie2"})
    assert set(session.cookies) == {'c1', 'c2'}
    assert session.cookies['c1'].value == 'cookie1'
    assert session.cookies['c2'].value == 'cookie2'