from __future__ import with_statement
import unittest
import redis

from redis._compat import b

class PipelineTestCase(unittest.TestCase):
    def test_exec_error_raised(self):
        self.client['c'] = 'a'
        with self.client.pipeline() as pipe:
            pipe.set('a', 1).set('b', 2).lpush('c', 3).set('d', 4)
            self.assertRaises(redis.ResponseError, pipe.execute)
            # make sure the pipe was restored to a working state
            self.assertEquals(pipe.set('z', 'zzz').execute(), [True])
            self.assertEquals(self.client['z'], b('zzz'))