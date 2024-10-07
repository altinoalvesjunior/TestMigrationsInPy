from __future__ import with_statement
import pytest
import time
from redis.client import Lock, LockError

class TestLock(object):
    def test_non_blocking(self, r):
        lock1 = r.lock('foo')
        assert lock1.acquire(blocking=False)
        assert lock1.acquired_until
        lock1.release()
        assert lock1.acquired_until is None