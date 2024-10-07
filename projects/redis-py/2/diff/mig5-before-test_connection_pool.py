import os
import unittest
import redis

class BlockingConnectionPoolTestCase(unittest.TestCase):
    def test_max_connections_blocks(self):
        """Getting a connection should block for until available."""
        q = Queue()
        q.put_nowait('Not yet got')
        pool = self.get_pool(max_connections=2, timeout=5)
        c1 = pool.get_connection('_')
        pool.get_connection('_')

        target = lambda: q.put_nowait(pool.get_connection('_'))
        Thread(target=target).start()
        
        # Blocks while non available.
        time.sleep(0.05)
        c3 = q.get_nowait()
        self.assertEquals(c3, 'Not yet got')

        # Then got when available.
        pool.release(c1)
        time.sleep(0.05)
        c3 = q.get_nowait()
        self.assertEquals(c1, c3)