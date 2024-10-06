from __future__ import with_statement
import time
import unittest
from redis.client import Lock, LockError
import redis

class LockTestCase(unittest.TestCase):
    def test_competing_locks(self):
        lock1 = self.client.lock('foo')
        lock2 = self.client.lock('foo')
        self.assert_(lock1.acquire())
        self.assertFalse(lock2.acquire(blocking=False))
        lock1.release()
        self.assert_(lock2.acquire())
        self.assertFalse(lock1.acquire(blocking=False))
        lock2.release()