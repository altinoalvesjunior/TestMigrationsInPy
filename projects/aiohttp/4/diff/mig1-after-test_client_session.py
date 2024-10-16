import pytest
from aiohttp.client import ClientSession

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

def test_init_headers_simple_dict(create_session):
    session = create_session(headers={"h1": "header1",
                                      "h2": "header2"})
    assert sorted(session._default_headers.items()) == [("H1", "header1"), ("H2", "header2")]