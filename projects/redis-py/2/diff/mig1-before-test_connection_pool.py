import os
import unittest
import redis

class ConnectionPoolTestCase(unittest.TestCase):
    def test_connection_creation(self):
        connection_info = {'foo': 'bar', 'biz': 'baz'}
        pool = self.get_pool(connection_info=connection_info)
        connection = pool.get_connection('_')
        self.assertEquals(connection.kwargs, connection_info)