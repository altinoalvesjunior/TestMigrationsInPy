from __future__ import with_statement
import unittest

import redis
from redis._compat import b

class PipelineTestCase(unittest.TestCase):     
    def test_pipeline(self):
        with self.client.pipeline() as pipe:
            pipe.set('a', 'a1').get('a').zadd('z', z1=1).zadd('z', z2=4)
            pipe.zincrby('z', 'z1').zrange('z', 0, 5, withscores=True)
            self.assertEquals(
                pipe.execute(),
                [
                    True,
                    b('a1'),
                    True,
                    True,
                    2.0,
                    [(b('z1'), 2.0), (b('z2'), 4)],
                ]
            )