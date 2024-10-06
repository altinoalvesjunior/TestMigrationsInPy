import os
import pytest

import redis
import time

from threading import Thread
from redis._compat import Queue

class TestConnectionPoolCase(object):
    def test_connection_creation(self):
        connection_info = {'foo': 'bar', 'biz': 'baz'}
        pool = self.get_pool(connection_info=connection_info)
        connection = pool.get_connection('_')
        assert connection.kwargs == connection_info