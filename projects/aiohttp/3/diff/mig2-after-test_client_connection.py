import gc
import pytest
from unittest import mock
from aiohttp.connector import Connection

def test_del(connector, key, request, transport, protocol, loop):
    conn = Connection(connector, key, request,
                      transport, protocol, loop)
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)
    with pytest.warns(ResourceWarning):
        del conn
        gc.collect()
    connector._release.assert_called_with(key,
                                          request,
                                          transport,
                                          protocol,
                                          should_close=True)
    msg = {'client_connection': mock.ANY,  # conn was deleted
           'message': 'Unclosed connection'}
    if loop.get_debug():
        msg['source_traceback'] = mock.ANY
    exc_handler.assert_called_with(loop, msg)