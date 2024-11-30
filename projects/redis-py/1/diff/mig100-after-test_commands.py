import pytest
import redis

class TestRedisCommands(object):
    def test_sort_all_options(self, r):
        r['user:1:username'] = 'zeus'
        r['user:2:username'] = 'titan'
        r['user:3:username'] = 'hermes'
        r['user:4:username'] = 'hercules'
        r['user:5:username'] = 'apollo'
        r['user:6:username'] = 'athena'
        r['user:7:username'] = 'hades'
        r['user:8:username'] = 'dionysus'
        r['user:1:favorite_drink'] = 'yuengling'
        r['user:2:favorite_drink'] = 'rum'
        r['user:3:favorite_drink'] = 'vodka'
        r['user:4:favorite_drink'] = 'milk'
        r['user:5:favorite_drink'] = 'pinot noir'
        r['user:6:favorite_drink'] = 'water'
        r['user:7:favorite_drink'] = 'gin'
        r['user:8:favorite_drink'] = 'apple juice'
        r.rpush('gods', '1', '2', '3', '4', '5', '6', '7', '8')
        num = r.sort(
            'gods', start=2, num=4, by='user:*:username',
            get='user:*:favorite_drink', desc=True, alpha=True, store='sorted')
        assert num == 4
        assert r.lrange('sorted', 0, 10) == \
            [b('vodka'), b('milk'), b('gin'), b('apple juice')]