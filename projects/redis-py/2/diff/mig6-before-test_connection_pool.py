import os
import unittest
import redis

class BlockingConnectionPoolTestCase(unittest.TestCase):
    def test_max_connections_timeout(self):
        """Getting a connection raises ``ConnectionError`` after timeout."""

        pool = self.get_pool(max_connections=2, timeout=0.1)
        pool.get_connection('_')
        pool.get_connection('_')
        self.assertRaises(redis.ConnectionError, pool.get_connection, '_')