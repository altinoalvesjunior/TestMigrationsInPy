import pytest
from aiohttp import helpers

def test_parse_mimetype_1():
    assert helpers.parse_mimetype('') == ('', '', '', {})

def test_parse_mimetype_2():
    assert helpers.parse_mimetype('*') == ('*', '*', '', {})

def test_parse_mimetype_3():
    assert (helpers.parse_mimetype('application/json') ==
            ('application', 'json', '', {}))

def test_parse_mimetype_4():
    assert (
        helpers.parse_mimetype('application/json;  charset=utf-8') ==
        ('application', 'json', '', {'charset': 'utf-8'}))

def test_parse_mimetype_5():
    assert (
        helpers.parse_mimetype('''application/json; charset=utf-8;''') ==
        ('application', 'json', '', {'charset': 'utf-8'}))

def test_parse_mimetype_6():
    assert(
        helpers.parse_mimetype('ApPlIcAtIoN/JSON;ChaRseT="UTF-8"') ==
        ('application', 'json', '', {'charset': 'UTF-8'}))

def test_parse_mimetype_7():
    assert (
        helpers.parse_mimetype('application/rss+xml') ==
        ('application', 'rss', 'xml', {}))

def test_parse_mimetype_8():
    assert (
        helpers.parse_mimetype('text/plain;base64') ==
        ('text', 'plain', '', {'base64': ''}))