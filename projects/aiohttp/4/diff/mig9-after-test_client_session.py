import pytest
from aiohttp.client import ClientSession
from aiohttp.multidict import CIMultiDict

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

def test_merge_headers_with_list_of_tuples_duplicated_names(create_session):
    session = create_session(headers={"h1": "header1",
                                      "h2": "header2"})
    headers = session._prepare_headers([("h1", "v1"),
                                        ("h1", "v2")])
    assert isinstance(headers, CIMultiDict)
    assert headers == CIMultiDict([("H2", "header2"),
                                   ("H1", "v1"),
                                   ("H1", "v2")])