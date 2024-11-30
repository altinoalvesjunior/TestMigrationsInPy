import pytest
import redis

class TestRedisCommands(object):
    def test_sort_get_groups_two(self, r):
        r['user:1'] = 'u1'
        r['user:2'] = 'u2'
        r['user:3'] = 'u3'
        r.rpush('a', '2', '3', '1')
        assert r.sort('a', get=('user:*', '#'), groups=True) == \
            [(b('u1'), b('1')), (b('u2'), b('2')), (b('u3'), b('3'))]