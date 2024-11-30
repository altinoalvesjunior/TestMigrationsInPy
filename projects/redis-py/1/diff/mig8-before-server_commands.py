import unittest
from redis._compat import ascii_letters
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_large_responses(self):
        "The PythonParser has some special cases for return values > 1MB"
        # load up 5MB of data into a key
        data = []
        for i in range(5000000 // len(ascii_letters)):
            data.append(ascii_letters)
        data = ''.join(data)
        self.client.set('a', data)
        self.assertEquals(self.client.get('a'), data) #No original não tinha b()