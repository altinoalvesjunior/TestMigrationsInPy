import pytest
import datetime
import time
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.0')
class TestRedisCommands(object):
    def test_pexpireat_datetime(self, r):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        r['a'] = 'foo'
        assert r.pexpireat('a', expire_at)
        assert 0 < r.pttl('a') <= 60000

    def test_pexpireat_no_key(self, r):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        assert not r.pexpireat('a', expire_at)

    def test_pexpireat_unixtime(self, r):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        r['a'] = 'foo'
        expire_at_seconds = int(time.mktime(expire_at.timetuple())) * 1000
        assert r.pexpireat('a', expire_at_seconds)
        assert 0 < r.pttl('a') <= 60000