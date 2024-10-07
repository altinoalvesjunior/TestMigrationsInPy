import os
import unittest
import redis

class ConnectionPoolTestCase(unittest.TestCase):
    def test_multiple_connections(self):
        pool = self.get_pool()
        c1 = pool.get_connection('_')
        c2 = pool.get_connection('_')
        self.assert_(c1 != c2)