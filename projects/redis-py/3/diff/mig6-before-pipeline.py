from __future__ import with_statement
import unittest
import redis

from redis._compat import b

class PipelineTestCase(unittest.TestCase):
    def test_exec_error_in_response(self):
        # an invalid pipeline command at exec time adds the exception instance
        # to the list of returned values
        self.client['c'] = 'a'
        with self.client.pipeline() as pipe:
            pipe.set('a', 1).set('b', 2).lpush('c', 3).set('d', 4)
            result = pipe.execute(raise_on_error=False)
            self.assertEquals(result[0], True)
            self.assertEquals(self.client['a'], b('1'))
            self.assertEquals(result[1], True)
            self.assertEquals(self.client['b'], b('2'))
            # we can't lpush to a key that's a string value, so this should
            # be a ResponseError exception
            self.assert_(isinstance(result[2], redis.ResponseError))
            self.assertEquals(self.client['c'], b('a'))
            self.assertEquals(result[3], True)
            self.assertEquals(self.client['d'], b('4'))
            # make sure the pipe was restored to a working state
            self.assertEquals(pipe.set('z', 'zzz').execute(), [True])
            self.assertEquals(self.client['z'], b('zzz'))