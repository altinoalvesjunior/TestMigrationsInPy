from __future__ import with_statement
import pytest
import time
from redis.client import Lock, LockError

class TestLock(object):
    def test_competing_locks(self, r):
        lock1 = r.lock('foo')
        lock2 = r.lock('foo')
        assert lock1.acquire()
        assert not lock2.acquire(blocking=False)
        lock1.release()
        assert lock2.acquire()
        assert not lock1.acquire(blocking=False)
        lock2.release()