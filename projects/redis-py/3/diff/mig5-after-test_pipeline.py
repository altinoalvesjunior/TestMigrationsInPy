from __future__ import with_statement
import pytest

import redis
from redis._compat import b

class TestPipeline(object):
    def test_pipeline_no_transaction_watch_failure(self, r):
        r['a'] = 0
        with r.pipeline(transaction=False) as pipe:
            pipe.watch('a')
            a = pipe.get('a')
            r['a'] = 'bad'
            pipe.multi()
            pipe.set('a', int(a) + 1)
            with pytest.raises(redis.WatchError):
                pipe.execute()
            assert r['a'] == b('bad')
