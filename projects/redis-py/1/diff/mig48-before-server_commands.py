import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_type(self):
        self.assertEquals(self.client.type('a'), b('none'))
        self.client['a'] = '1'
        self.assertEquals(self.client.type('a'), b('string'))
        del self.client['a']
        self.client.lpush('a', '1')
        self.assertEquals(self.client.type('a'), b('list'))
        del self.client['a']
        self.client.sadd('a', '1')
        self.assertEquals(self.client.type('a'), b('set'))
        del self.client['a']
        self.client.zadd('a', **{'1': 1})
        self.assertEquals(self.client.type('a'), b('zset'))