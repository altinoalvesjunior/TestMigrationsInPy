from __future__ import with_statement
import pytest

import redis
from redis._compat import b

class TestPipeline(object):
    def test_transaction_callable(self, r):
        r['a'] = 1
        r['b'] = 2
        has_run = []
        
        def my_transaction(pipe):
            a_value = pipe.get('a')
            assert a_value in (b('1'), b('2'))
            b_value = pipe.get('b')
            assert b_value == b('2')
            # silly run-once code... incr's "a" so WatchError should be raised
            # forcing this all to run again. this should incr "a" once to "2"
            if not has_run:
                r.incr('a')
                has_run.append('it has')
            pipe.multi()
            pipe.set('c', int(a_value) + int(b_value))
        result = r.transaction(my_transaction, 'a', 'b')
        assert result == [True]
        assert r['c'] == b('4')