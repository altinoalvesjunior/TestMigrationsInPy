from __future__ import with_statement
import time
import unittest
from redis.client import Lock, LockError
import redis

class LockTestCase(unittest.TestCase):
    def test_non_blocking(self):
        lock1 = self.client.lock('foo')
        self.assert_(lock1.acquire(blocking=False))
        self.assert_(lock1.acquired_until)
        lock1.release()
        self.assert_(lock1.acquired_until is None)