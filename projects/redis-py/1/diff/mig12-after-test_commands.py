import pytest
import redis

class TestRedisCommands(object):
    def test_config_set(self, r):
        data = r.config_get()
        rdbname = data['dbfilename']
        try:
            assert r.config_set('dbfilename', 'redis_py_test.rdb')
            assert r.config_get()['dbfilename'] == 'redis_py_test.rdb'
        finally:
            assert r.config_set('dbfilename', rdbname)