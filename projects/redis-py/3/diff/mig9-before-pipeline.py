from __future__ import with_statement
import unittest
import redis

from redis._compat import b

class PipelineTestCase(unittest.TestCase):
    def test_watch_succeed(self, r):
        r['a'] = 1
        r['b'] = 2
        with r.pipeline() as pipe:
            pipe.watch('a', 'b')
            assert pipe.watching
            a_value = pipe.get('a')
            b_value = pipe.get('b')
            assert a_value == b('1')
            assert b_value == b('2')
            pipe.multi()
            pipe.set('c', 3)
            assert pipe.execute() == [True]
            assert not pipe.watching