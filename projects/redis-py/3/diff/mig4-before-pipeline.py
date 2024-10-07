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
        
    def test_pipeline_no_transaction_watch(self):
        self.client.set('a', 0)
        with self.client.pipeline(transaction=False) as pipe:
            pipe.watch('a')
            a = pipe.get('a')
            pipe.multi()
            pipe.set('a', int(a) + 1)
            result = pipe.execute()
            self.assertEquals(result, [True])
