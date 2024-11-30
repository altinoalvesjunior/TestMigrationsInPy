import pytest
import redis

class TestBinarySave(object):
    def test_floating_point_encoding(self, r):
        """
        High precision floating point values sent to the server should keep
        precision.
        """
        timestamp = 1349673917.939762
        r.zadd('a', 'a1', timestamp)
        assert r.zscore('a', 'a1') == timestamp