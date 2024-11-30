import pytest
import redis

class TestRedisCommands(object):
    def test_sort_groups_three_gets(self, r):
        r['user:1'] = 'u1'
        r['user:2'] = 'u2'
        r['user:3'] = 'u3'
        r['door:1'] = 'd1'
        r['door:2'] = 'd2'
        r['door:3'] = 'd3'
        r.rpush('a', '2', '3', '1')
        assert r.sort('a', get=('user:*', 'door:*', '#'), groups=True) == \
            [
                (b('u1'), b('d1'), b('1')),
                (b('u2'), b('d2'), b('2')),
                (b('u3'), b('d3'), b('3'))
            ]