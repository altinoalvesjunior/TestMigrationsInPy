from __future__ import with_statement
import pytest

import redis
from redis._compat import b

class TestPipeline(object):
    def test_exec_error_raised(self, r):
        r['c'] = 'a'
        with r.pipeline() as pipe:
            pipe.set('a', 1).set('b', 2).lpush('c', 3).set('d', 4)
            with pytest.raises(redis.ResponseError):
                pipe.execute()
            # make sure the pipe was restored to a working state
            assert pipe.set('z', 'zzz').execute() == [True]
            assert r['z'] == b('zzz')