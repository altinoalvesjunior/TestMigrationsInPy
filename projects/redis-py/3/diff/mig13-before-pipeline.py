from __future__ import with_statement
import unittest
import redis

from redis._compat import b

class PipelineTestCase(unittest.TestCase):
    def test_error_in_simple_pipeline(self):
        self.client.hmset('x', {'a': 'b'})
        with self.client.pipeline(transaction=False) as pipe:
            pipe.llen('x')
            pipe.expire('x', 100)
            try:
                pipe.execute()
            except redis.ResponseError:
                pass
            else:
                raise
        ret = self.client.hgetall('x')
        self.assertEqual(ret, {b('a'): b('b')})