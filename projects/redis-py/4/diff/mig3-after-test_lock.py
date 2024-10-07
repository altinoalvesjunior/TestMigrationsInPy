from __future__ import with_statement
import pytest
import time
from redis.client import Lock, LockError

class TestLock(object):
    def test_timeouts(self, r):
        lock1 = r.lock('foo', timeout=1)
        lock2 = r.lock('foo')
        assert lock1.acquire()
        now = time.time()
        assert now < lock1.acquired_until < now + 1
        assert lock1.acquired_until == float(r['foo'])
        assert not lock2.acquire(blocking=False)
        time.sleep(2)  # need to wait up to 2 seconds for lock to timeout
        assert lock2.acquire(blocking=False)
        lock2.release()