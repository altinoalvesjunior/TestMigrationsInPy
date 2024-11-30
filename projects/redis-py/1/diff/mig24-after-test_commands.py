import pytest
import datetime
import time
import redis

class TestRedisCommands(object):
    def test_expireat_datetime(self, r):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        r['a'] = 'foo'
        assert r.expireat('a', expire_at)
        assert 0 < r.ttl('a') <= 60

    def test_expireat_no_key(self, r):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        assert not r.expireat('a', expire_at)

    def test_expireat_unixtime(self, r):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        r['a'] = 'foo'
        expire_at_seconds = int(time.mktime(expire_at.timetuple()))
        assert r.expireat('a', expire_at_seconds)
        assert 0 < r.ttl('a') <= 60