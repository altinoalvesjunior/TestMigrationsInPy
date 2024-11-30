from __future__ import with_statement
import unittest
import redis

from redis._compat import b

class PipelineTestCase(unittest.TestCase):
    def test_parse_error_raised(self):
        with self.client.pipeline() as pipe:
            # the zrem is invalid because we don't pass any keys to it
            pipe.set('a', 1).zrem('b').set('b', 2)
            self.assertRaises(redis.ResponseError, pipe.execute)
            # make sure the pipe was restored to a working state
            self.assertEquals(pipe.set('z', 'zzz').execute(), [True])
            self.assertEquals(self.client['z'], b('zzz'))