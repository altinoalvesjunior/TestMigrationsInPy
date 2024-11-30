import pytest
import redis
from redis._compat import iteritems, b

class TestBinarySave(object):
    def test_binary_lists(self, r):
        mapping = {
            b('foo bar'): [b('1'), b('2'), b('3')],
            b('foo\r\nbar\r\n'): [b('4'), b('5'), b('6')],
            b('foo\tbar\x07'): [b('7'), b('8'), b('9')],
        }
        # fill in lists
        for key, value in iteritems(mapping):
            r.rpush(key, *value)
        # check that KEYS returns all the keys as they are
        assert sorted(r.keys('*')) == sorted(list(iterkeys(mapping))) #No original usa iterkeys
        # check that it is possible to get list content by key name
        for key, value in iteritems(mapping):
            assert r.lrange(key, 0, -1) == value