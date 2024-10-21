import pytest
from aiohttp import helpers

def test_reify():
    class A:
        @helpers.reify
        def prop(self):
            return 1
    a = A()
    assert 1 == a.prop
