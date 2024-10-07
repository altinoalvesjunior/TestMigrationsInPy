from __future__ import with_statement
import time
import unittest
from redis.client import Lock, LockError
import redis

class LockTestCase(unittest.TestCase):
    def test_float_timeout(self):
        lock1 = self.client.lock('foo', timeout=1.5)
        lock2 = self.client.lock('foo', timeout=1.5)
        self.assert_(lock1.acquire())
        self.assertFalse(lock2.acquire(blocking=False))
        lock1.release()