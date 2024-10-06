from __future__ import with_statement
import unittest
import redis

from redis._compat import b

class PipelineTestCase(unittest.TestCase):
    def setUp(self):
        self.client = redis.Redis(host='localhost', port=6379, db=9)
        self.client.flushdb()
        
    def tearDown(self):
        self.client.flushdb()
        
    def test_watch_failure(self):
        self.client.set('a', 1)
        self.client.set('b', 2)
        with self.client.pipeline() as pipe:
            pipe.watch('a', 'b')
            self.client.set('b', 3)
            pipe.multi()
            pipe.get('a')
            self.assertRaises(redis.WatchError, pipe.execute)
            self.assertEquals(pipe.watching, False)