import pytest
from unittest import mock
from aiohttp import parsers

@pytest.fixture
def lines_parser():
    return parsers.LinesParser()

def test_set_parser_unset_prev(loop, lines_parser):
    stream = parsers.StreamParser(loop=loop)
    stream.set_parser(lines_parser)
    unset = stream.unset_parser = mock.Mock()
    stream.set_parser(lines_parser)
    assert unset.called