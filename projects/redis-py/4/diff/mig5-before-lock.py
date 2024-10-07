from __future__ import with_statement
import time
import unittest
from redis.client import Lock, LockError
import redis

class LockTestCase(unittest.TestCase):
    def test_context_manager(self):
        with self.client.lock('foo'):
            self.assertEquals(
                self.client['foo'],
                str(Lock.LOCK_FOREVER).encode())
        self.assertEquals(self.client.get('foo'), None)