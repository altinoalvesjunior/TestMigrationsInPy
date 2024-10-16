import pytest
from aiohttp.client import ClientSession
from aiohttp.multidict import CIMultiDict

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

def test_init_headers_list_of_tuples_with_duplicates(create_session):
    session = create_session(headers=[("h1", "header11"),
                                      ("h2", "header21"),
                                      ("h1", "header12")])
    assert session._default_headers == CIMultiDict([("H1", "header11"),
                                                    ("H2", "header21"),
                                                    ("H1", "header12")])