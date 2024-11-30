import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    # ... (setUp, tearDown, get_client, make_zset - igual ao mig89-before) ...

    def test_zincrby(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(redis.ResponseError, self.client.zincrby, 'a', 'a1')
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3})
        self.assertEquals(self.client.zincrby('a', 'a2'), 3.0)
        self.assertEquals(self.client.zincrby('a', 'a3', amount=5), 8.0)
        self.assertEquals(self.client.zscore('a', 'a2'), 3.0)
        self.assertEquals(self.client.zscore('a', 'a3'), 8.0)