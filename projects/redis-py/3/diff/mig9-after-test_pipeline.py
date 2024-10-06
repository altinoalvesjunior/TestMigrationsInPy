from __future__ import with_statement
import pytest

import redis
from redis._compat import b

class TestPipeline(object):
    def test_watch_succeed(self):
        self.client.set('a', 1)
        self.client.set('b', 2)
        with self.client.pipeline() as pipe:
            pipe.watch('a', 'b')
            self.assertEquals(pipe.watching, True)
            a_value = pipe.get('a')
            b_value = pipe.get('b')
            self.assertEquals(a_value, b('1'))
            self.assertEquals(b_value, b('2'))
            pipe.multi()
            pipe.set('c', 3)
            self.assertEquals(pipe.execute(), [True])
            self.assertEquals(pipe.watching, False)