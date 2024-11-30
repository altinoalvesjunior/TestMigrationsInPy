import unittest
from redis._compat import b, next
from redis.exceptions import ConnectionError
import redis

class PubSubTestCase(unittest.TestCase):
    def test_pattern_subscribe(self):
        # psubscribe doesn't return anything
        self.assertEquals(
            self.pubsub.psubscribe('f*'),
            None
        )
        # send a message
        self.assertEquals(self.client.publish('foo', 'hello foo'), 1)
        # there should be now 2 messages in the buffer, a subscribe and the
        # one we just published
        self.assertEquals(
            next(self.pubsub.listen()),
            {
                'type': 'psubscribe',
                'pattern': None,
                'channel': 'f*',
                'data': 1
            }
        )
        self.assertEquals(
            next(self.pubsub.listen()),
            {
                'type': 'pmessage',
                'pattern': 'f*',
                'channel': 'foo',
                'data': b('hello foo')
            }
        )
        # unsubscribe
        self.assertEquals(
            self.pubsub.punsubscribe('f*'),
            None
        )
        # unsubscribe message should be in the buffer
        self.assertEquals(
            next(self.pubsub.listen()),
            {
                'type': 'punsubscribe',
                'pattern': None,
                'channel': 'f*',
                'data': 0
            }
        )