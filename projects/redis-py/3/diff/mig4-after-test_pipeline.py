from __future__ import with_statement
import pytest

import redis
from redis._compat import b

class TestPipeline(object):
    def test_pipeline_no_transaction_watch(self, r):
        r['a'] = 0
        with r.pipeline(transaction=False) as pipe:
            pipe.watch('a')
            a = pipe.get('a')
            pipe.multi()
            pipe.set('a', int(a) + 1)
            assert pipe.execute() == [True]