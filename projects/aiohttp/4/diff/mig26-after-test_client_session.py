import pytest
import gc
from unittest import mock
from aiohttp.client import ClientSession

def test_del(connector, loop):
    session = ClientSession(connector=connector, loop=loop)
    loop.set_exception_handler(lambda loop, ctx: None)

    with pytest.warns(ResourceWarning):
        del session
        gc.collect()