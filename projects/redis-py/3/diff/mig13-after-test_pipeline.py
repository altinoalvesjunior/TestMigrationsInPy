from __future__ import with_statement
import pytest

import redis
from redis._compat import b

class TestPipeline(object):
    def test_exec_error_in_no_transaction_pipeline(self, r):
        r['a'] = 1
        with r.pipeline(transaction=False) as pipe:
            pipe.llen('a')
            pipe.expire('a', 100)
            with pytest.raises(redis.ResponseError):
                pipe.execute()
        assert r['a'] == b('1')