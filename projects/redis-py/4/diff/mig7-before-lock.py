from __future__ import with_statement
import time
import unittest
from redis.client import Lock, LockError
import redis

class LockTestCase(unittest.TestCase):
    def test_high_sleep_raises_error(self):
        "If sleep is higher than timeout, it should raise an error"
        self.assertRaises(
            LockError,
            self.client.lock, 'foo', timeout=1, sleep=2
        )