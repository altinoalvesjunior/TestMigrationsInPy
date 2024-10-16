import pytest
from aiohttp import helpers

def test_reify():
    class A:
        @helpers.reify
        def prop(self):
            return 1
    a = A()
    assert 1 == a.prop

def test_reify_class():
    class A:
        @helpers.reify
        def prop(self):
            """Docstring."""
            return 1
    assert isinstance(A.prop, helpers.reify)
    assert 'Docstring.' == A.prop.__doc__

def test_reify_assignment():
    class A:
        @helpers.reify
        def prop(self):
            return 1
    a = A()
    with pytest.raises(AttributeError):
        a.prop = 123