import pytest
from aiohttp.client import ClientSession
from aiohttp.multidict import CIMultiDict

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

def test_merge_headers(create_session):
    # Check incoming simple dict
    session = create_session(headers={"h1": "header1",
                                      "h2": "header2"})
    headers = session._prepare_headers({"h1": "h1"})
    assert isinstance(headers, CIMultiDict)
    assert headers == CIMultiDict([("h2", "header2"),
                                   ("h1", "h1")])