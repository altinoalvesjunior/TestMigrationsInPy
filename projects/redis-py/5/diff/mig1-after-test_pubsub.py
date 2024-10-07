import pytest
import redis
from redis._compat import b, next
from redis.exceptions import ConnectionError

class TestPubSub(object):
    def test_channel_subscribe(self, r):
        p = r.pubsub()
        # subscribe doesn't return anything
        assert p.subscribe('foo') is None
        # send a message
        assert r.publish('foo', 'hello foo') == 1
        # there should be now 2 messages in the buffer, a subscribe and the
        # one we just published
        assert next(p.listen()) == \
            {
                'type': 'subscribe',
                'pattern': None,
                'channel': 'foo',
                'data': 1
            }
        assert next(p.listen()) == \
            {
                'type': 'message',
                'pattern': None,
                'channel': 'foo',
                'data': b('hello foo')
            }
        # unsubscribe
        assert p.unsubscribe('foo') is None
        # unsubscribe message should be in the buffer
        assert next(p.listen()) == \
            {
                'type': 'unsubscribe',
                'pattern': None,
                'channel': 'foo',
                'data': 0
            }