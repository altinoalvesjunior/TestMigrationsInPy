from __future__ import with_statement
import unittest
import redis

from redis._compat import b

class PipelineTestCase(unittest.TestCase):
    def test_pipeline_length(self):
        with self.client.pipeline() as pipe:
            # Initially empty.
            self.assertEquals(len(pipe), 0)
            self.assertFalse(pipe)
            # Fill 'er up!
            pipe.set('a', 'a1').set('b', 'b1').set('c', 'c1')
            self.assertEquals(len(pipe), 3)
            self.assertTrue(pipe)
            # Execute calls reset(), so empty once again.
            pipe.execute()
            self.assertEquals(len(pipe), 0)
            self.assertFalse(pipe)