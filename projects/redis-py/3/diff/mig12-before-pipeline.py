from __future__ import with_statement
import unittest
import redis

from redis._compat import b

class PipelineTestCase(unittest.TestCase):
    def test_transaction_callable(self):
        self.client.set('a', 1)
        self.client.set('b', 2)
        has_run = []
        
        def my_transaction(pipe):
            a_value = pipe.get('a')
            self.assert_(a_value in (b('1'), b('2')))
            b_value = pipe.get('b')
            self.assertEquals(b_value, b('2'))
            # silly run-once code... incr's a so WatchError should be raised
            # forcing this all to run again
            if not has_run:
                self.client.incr('a')
                has_run.append('it has')
            pipe.multi()
            pipe.set('c', int(a_value) + int(b_value))
        result = self.client.transaction(my_transaction, 'a', 'b')
        self.assertEquals(result, [True])
        self.assertEquals(self.client.get('c'), b('4'))