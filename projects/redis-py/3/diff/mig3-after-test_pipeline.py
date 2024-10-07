from __future__ import with_statement
import pytest

import redis
from redis._compat import b

class TestPipeline(object):
    def test_pipeline_no_transaction(self, r):
        with r.pipeline(transaction=False) as pipe:
            pipe.set('a', 'a1').set('b', 'b1').set('c', 'c1')
            assert pipe.execute() == [True, True, True]
            assert r['a'] == b('a1')
            assert r['b'] == b('b1')
            assert r['c'] == b('c1')