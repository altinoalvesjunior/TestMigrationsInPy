from __future__ import with_statement
import pytest
import time
from redis.client import Lock, LockError

class TestLock(object):
    def test_float_timeout(self, r):
        lock1 = r.lock('foo', timeout=1.5)
        lock2 = r.lock('foo', timeout=1.5)
        assert lock1.acquire()
        assert not lock2.acquire(blocking=False)
        lock1.release()