import pytest
from aiohttp.client import ClientSession
from aiohttp.multidict import CIMultiDict

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

def test_init_headers_list_of_tuples(create_session):
    session = create_session(headers=[("h1", "header1"),
                                      ("h2", "header2"),
                                      ("h3", "header3")])
    assert session._default_headers == CIMultiDict([("h1", "header1"),
                                                    ("h2", "header2"),
                                                    ("h3", "header3")])