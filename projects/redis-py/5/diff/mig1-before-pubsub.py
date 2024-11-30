import unittest
from redis._compat import b, next
from redis.exceptions import ConnectionError
import redis

class PubSubTestCase(unittest.TestCase):
    def test_channel_subscribe(self):
        # subscribe doesn't return anything
        self.assertEquals(
            self.pubsub.subscribe('foo'),
            None
        )
        # send a message
        self.assertEquals(self.client.publish('foo', 'hello foo'), 1)
        # there should be now 2 messages in the buffer, a subscribe and the
        # one we just published
        self.assertEquals(
            next(self.pubsub.listen()),
            {
                'type': 'subscribe',
                'pattern': None,
                'channel': 'foo',
                'data': 1
            }
        )
        self.assertEquals(
            next(self.pubsub.listen()),
            {
                'type': 'message',
                'pattern': None,
                'channel': 'foo',
                'data': b('hello foo')
            }
        )
        # unsubscribe
        self.assertEquals(
            self.pubsub.unsubscribe('foo'),
            None
        )
        # unsubscribe message should be in the buffer
        self.assertEquals(
            next(self.pubsub.listen()),
            {
                'type': 'unsubscribe',
                'pattern': None,
                'channel': 'foo',
                'data': 0
            }
        )
