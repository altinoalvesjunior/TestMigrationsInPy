import pytest
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.0')
class TestRedisCommands(object):
    def test_pexpire(self, r):
        assert not r.pexpire('a', 60000) # Usando 60000 para consistência com outros testes after
        r['a'] = 'foo'
        assert r.pexpire('a', 60000)
        assert 0 < r.pttl('a') <= 60000
        assert r.persist('a')
        assert r.pttl('a') is None