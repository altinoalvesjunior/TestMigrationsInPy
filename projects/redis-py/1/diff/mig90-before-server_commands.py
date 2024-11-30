import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_by(self):
        self.client['score:1'] = 8
        self.client['score:2'] = 3
        self.client['score:3'] = 5
        self.make_list('a_values', '123') # No original, a chave é 'a_values'
        self.assertEquals(
            self.client.sort('a_values', by='score:*'),
            [b('2'), b('3'), b('1')])