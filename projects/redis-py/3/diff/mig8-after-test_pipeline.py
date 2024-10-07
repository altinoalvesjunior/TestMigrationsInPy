from __future__ import with_statement
import pytest

import redis
from redis._compat import b

class TestPipeline(object):
    def test_parse_error_raised(self, r):
        with r.pipeline() as pipe:
            # the zrem is invalid because we don't pass any keys to it
            pipe.set('a', 1).zrem('b').set('b', 2)
            with pytest.raises(redis.ResponseError):
                pipe.execute()
            # make sure the pipe was restored to a working state
            assert pipe.set('z', 'zzz').execute() == [True]
            assert r['z'] == b('zzz')