from __future__ import with_statement
import time
import unittest
from redis.client import Lock, LockError
import redis

class LockTestCase(unittest.TestCase):
    
    def setUp(self):
        self.client = redis.Redis(host='localhost', port=6379, db=9)
        self.client.flushdb()
        
    def tearDown(self):
        self.client.flushdb()
        
    def test_lock(self):
        lock = self.client.lock('foo')
        self.assert_(lock.acquire())
        self.assertEquals(self.client['foo'], str(Lock.LOCK_FOREVER).encode())
        lock.release()
        self.assertEquals(self.client.get('foo'), None)