import os
import unittest
import redis

class BlockingConnectionPoolTestCase(unittest.TestCase):
    def test_release(self):
        pool = self.get_pool()
        c1 = pool.get_connection('_')
        pool.release(c1)
        c2 = pool.get_connection('_')
        self.assertEquals(c1, c2)