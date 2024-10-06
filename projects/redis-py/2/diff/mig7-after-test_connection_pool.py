import os
import pytest

import redis
import time

from threading import Thread
from redis._compat import Queue

class TestBlockingConnectionPool(object):
    def test_reuse_previously_released_connection(self):
        pool = self.get_pool()
        c1 = pool.get_connection('_')
        pool.release(c1)
        c2 = pool.get_connection('_')
        assert c1 == c2