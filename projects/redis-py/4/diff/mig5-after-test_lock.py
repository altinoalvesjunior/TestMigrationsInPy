from __future__ import with_statement
import pytest
import time
from redis.client import Lock, LockError

class TestLock(object):
    def test_context_manager(self, r):
        with r.lock('foo'):
            assert r['foo'] == str(Lock.LOCK_FOREVER).encode()
        assert r.get('foo') is None