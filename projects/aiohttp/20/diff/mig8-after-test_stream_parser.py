import pytest
from aiohttp import parsers

@pytest.fixture
def lines_parser():
    return parsers.LinesParser()

def test_set_parser_exception(loop, lines_parser):
    stream = parsers.StreamParser(loop=loop)
    exc = ValueError()
    stream.set_exception(exc)
    s = stream.set_parser(lines_parser)
    assert s.exception() is exc