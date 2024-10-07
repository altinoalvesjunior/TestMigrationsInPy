import os
import pytest

import redis
import time

from threading import Thread
from redis._compat import Queue

class TestBlockingConnectionPool(object):
    def test_max_connections_timeout(self):
        """Getting a connection raises ``ConnectionError`` after timeout."""

        pool = self.get_pool(max_connections=2, timeout=0.1)
        pool.get_connection('_')
        pool.get_connection('_')
        with pytest.raises(redis.ConnectionError):
            pool.get_connection('_')
