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
    
    def test_pipeline_no_transaction(self):
        with self.client.pipeline(transaction=False) as pipe:
            pipe.set('a', 'a1').set('b', 'b1').set('c', 'c1')
            self.assertEquals(pipe.execute(), [True, True, True])
            self.assertEquals(self.client['a'], b('a1'))
            self.assertEquals(self.client['b'], b('b1'))
            self.assertEquals(self.client['c'], b('c1'))