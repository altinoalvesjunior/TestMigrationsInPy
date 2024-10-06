import os
import pytest

import redis
import time

from threading import Thread
from redis._compat import Queue

class TestBlockingConnectionPool(object):
    def test_multiple_connections(self):
        pool = self.get_pool()
        c1 = pool.get_connection('_')
        c2 = pool.get_connection('_')
        assert c1 != c2