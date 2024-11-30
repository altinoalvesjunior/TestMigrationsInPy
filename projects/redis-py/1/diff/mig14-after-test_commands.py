import pytest
import redis

class TestRedisCommands(object):
    def test_echo(self, r):
        assert r.echo('foo bar') == b('foo bar')