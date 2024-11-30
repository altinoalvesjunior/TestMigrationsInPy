import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_all_options(self):
        self.client['user:1:username'] = 'zeus'
        self.client['user:2:username'] = 'titan'
        self.client['user:3:username'] = 'hermes'
        self.client['user:4:username'] = 'hercules'
        self.client['user:5:username'] = 'apollo'
        self.client['user:6:username'] = 'athena'
        self.client['user:7:username'] = 'hades'
        self.client['user:8:username'] = 'dionysus'
        self.client['user:1:favorite_drink'] = 'yuengling'
        self.client['user:2:favorite_drink'] = 'rum'
        self.client['user:3:favorite_drink'] = 'vodka'
        self.client['user:4:favorite_drink'] = 'milk'
        self.client['user:5:favorite_drink'] = 'pinot noir'
        self.client['user:6:favorite_drink'] = 'water'
        self.client['user:7:favorite_drink'] = 'gin'
        self.client['user:8:favorite_drink'] = 'apple juice'
        self.make_list('gods', '12345678')
        num = self.client.sort(
            'gods', start=2, num=4, by='user:*:username',
            get='user:*:favorite_drink', desc=True, alpha=True, store='sorted')
        self.assertEquals(num, 4)
        self.assertEquals(
            self.client.lrange('sorted', 0, 10),
            [b('vodka'), b('milk'), b('gin'), b('apple juice')])