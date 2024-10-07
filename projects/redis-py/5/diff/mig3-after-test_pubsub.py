import pytest
import redis
from redis._compat import b, next
from redis.exceptions import ConnectionError

class TestPubSubRedisDown(object):
    def test_channel_subscribe(self, r):
        r = redis.Redis(host='localhost', port=6390)
        p = r.pubsub()
        with pytest.raises(ConnectionError):
            p.subscribe('foo')