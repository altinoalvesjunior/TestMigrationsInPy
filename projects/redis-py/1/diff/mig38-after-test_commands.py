import pytest
import redis
from redis._compat import iteritems

class TestRedisCommands(object):
    def test_mset(self, r):
        d = {'a': b('1'), 'b': b('2'), 'c': b('3')} #Convertendo valores para bytes
        assert r.mset(d)
        for k, v in iteritems(d):
            assert r[k] == v