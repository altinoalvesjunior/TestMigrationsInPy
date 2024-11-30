import unittest
import redis
import pytest
from redis import exceptions

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_groups_string_get(self):
        self.client['user:1'] = 'u1'
        self.client['user:2'] = 'u2'
        self.client['user:3'] = 'u3'
        self.make_list('a', '231')
        self.assertRaises(redis.DataError, self.client.sort, 'a',
                          get='user:*', groups=True)