from __future__ import with_statement
import pytest

import redis
from redis._compat import b

class TestPipeline(object):
    def test_unwatch(self, r):
        r['a'] = 1
        r['b'] = 2
        with r.pipeline() as pipe:
            pipe.watch('a', 'b')
            r['b'] = 3
            pipe.unwatch()
            assert not pipe.watching
            pipe.get('a')
            assert pipe.execute() == [b('1')]