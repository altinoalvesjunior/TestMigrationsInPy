import pytest
from aiohttp import helpers

def test_reify_class():
    class A:
        @helpers.reify
        def prop(self):
            """Docstring."""
            return 1
    assert isinstance(A.prop, helpers.reify)
    assert 'Docstring.' == A.prop.__doc__