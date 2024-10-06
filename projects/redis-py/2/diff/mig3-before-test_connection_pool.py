import os
import unittest
import redis

class ConnectionPoolTestCase(unittest.TestCase):
    def test_max_connections(self):
        pool = self.get_pool(max_connections=2)
        pool.get_connection('_')
        pool.get_connection('_')
        self.assertRaises(redis.ConnectionError, pool.get_connection, '_')