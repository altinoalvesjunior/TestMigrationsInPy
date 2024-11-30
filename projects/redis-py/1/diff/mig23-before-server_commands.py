import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_expire(self):
        self.assertEquals(self.client.expire('a', 10), False)
        self.client['a'] = 'foo'
        self.assertEquals(self.client.expire('a', 10), True)
        self.assertEquals(self.client.ttl('a'), 10)
        self.assertEquals(self.client.persist('a'), True)
        self.assertEquals(self.client.ttl('a'), None)