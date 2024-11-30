import pytest
import redis

class TestResponseCallbacks(object):
    def test_response_callbacks(self, r):
        assert r.response_callbacks == redis.Redis.RESPONSE_CALLBACKS
        assert id(r.response_callbacks) != id(redis.Redis.RESPONSE_CALLBACKS)
        r.set_response_callback('GET', lambda x: 'static')
        r['a'] = 'foo'
        assert r['a'] == 'static'