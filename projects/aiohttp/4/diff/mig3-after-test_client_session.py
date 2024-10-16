import pytest
from aiohttp.client import ClientSession
from aiohttp.multidict import CIMultiDict, MultiDict

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

def test_init_headers_MultiDict(create_session):
    session = create_session(headers=MultiDict([("h1", "header1"),
                                                ("h2", "header2"),
                                                ("h3", "header3")]))
    assert session._default_headers == CIMultiDict([("H1", "header1"),
                                                    ("H2", "header2"),
                                                    ("H3", "header3")])