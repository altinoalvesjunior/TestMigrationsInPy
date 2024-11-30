import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_groups_three_gets(self):
        self.client['user:1'] = 'u1'
        self.client['user:2'] = 'u2'
        self.client['user:3'] = 'u3'
        self.client['door:1'] = 'd1'
        self.client['door:2'] = 'd2'
        self.client['door:3'] = 'd3'
        self.make_list('a', '231')
        self.assertEquals(
            self.client.sort('a', get=('user:*', 'door:*', '#'), groups=True),
            [
                (b('u1'), b('d1'), b('1')),
                (b('u2'), b('d2'), b('2')),
                (b('u3'), b('d3'), b('3'))
            ]
        )