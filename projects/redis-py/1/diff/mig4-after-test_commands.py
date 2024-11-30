import pytest
import redis

class TestBinarySave(object):
    def test_binary_get_set(self, r):
        assert r.set(' foo bar ', '123')
        assert r.get(' foo bar ') == b('123')
        assert r.set(' foo\r\nbar\r\n ', '456')
        assert r.get(' foo\r\nbar\r\n ') == b('456')
        assert r.set(' \r\n\t\x07\x13 ', '789')
        assert r.get(' \r\n\t\x07\x13 ') == b('789')
        assert sorted(r.keys('*')) == \
            [b(' \r\n\t\x07\x13 '), b(' foo\r\nbar\r\n '), b(' foo bar ')]
        assert r.delete(' foo bar ')
        assert r.delete(' foo\r\nbar\r\n ')
        assert r.delete(' \r\n\t\x07\x13 ')