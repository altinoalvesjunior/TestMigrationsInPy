from __future__ import with_statement
import time
import unittest
from redis.client import Lock, LockError
import redis

class LockTestCase(unittest.TestCase):
    def test_timeouts(self):
        lock1 = self.client.lock('foo', timeout=1)
        lock2 = self.client.lock('foo')
        self.assert_(lock1.acquire())
        self.assertEquals(lock1.acquired_until, float(int(time.time())) + 1)
        self.assertEquals(lock1.acquired_until, float(self.client['foo']))
        self.assertFalse(lock2.acquire(blocking=False))
        time.sleep(2)  # need to wait up to 2 seconds for lock to timeout
        self.assert_(lock2.acquire(blocking=False))
        lock2.release()