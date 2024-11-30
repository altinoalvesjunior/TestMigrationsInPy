import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_config_set(self):
        data = self.client.config_get()
        rdbname = data['dbfilename']
        self.assert_(self.client.config_set('dbfilename', 'redis_py_test.rdb'))
        self.assertEquals(
            self.client.config_get()['dbfilename'],
            'redis_py_test.rdb'
        )
        self.assert_(self.client.config_set('dbfilename', rdbname))
        self.assertEquals(self.client.config_get()['dbfilename'], rdbname)