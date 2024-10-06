import os
import pytest

import redis
import time

from threading import Thread
from redis._compat import Queue

class TestBlockingConnectionPool(object):
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
        assert c3 == 'Not yet got'

        # Then got when available.
        pool.release(c1)
        time.sleep(0.05)
        c3 = q.get_nowait()
        assert c1 == c3
        