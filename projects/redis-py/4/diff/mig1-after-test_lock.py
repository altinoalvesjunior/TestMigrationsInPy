from __future__ import with_statement
import pytest
import time
from redis.client import Lock, LockError

class TestLock(object):
    def test_lock(self, r):
        lock = r.lock('foo')
        assert lock.acquire()
        assert r['foo'] == str(Lock.LOCK_FOREVER).encode()
        lock.release()
        assert r.get('foo') is None