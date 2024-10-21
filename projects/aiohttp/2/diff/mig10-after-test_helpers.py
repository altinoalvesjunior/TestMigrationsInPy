import pytest
from aiohttp import helpers

def test_reify_assignment():
    class A:
        @helpers.reify
        def prop(self):
            return 1
    a = A()
    with pytest.raises(AttributeError):
        a.prop = 123