import os
import pytest

import redis
import time

from threading import Thread
from redis._compat import Queue

class TestConnectionPoolCase(object):
    def test_max_connections(self):
        pool = self.get_pool(max_connections=2)
        pool.get_connection('_')
        pool.get_connection('_')
        with pytest.raises(redis.ConnectionError):
            pool.get_connection('_')