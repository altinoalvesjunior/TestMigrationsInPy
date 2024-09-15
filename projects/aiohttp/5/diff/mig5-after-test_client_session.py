import contextlib

import pytest

@pytest.fixture
def connector(loop):
    conn = BaseConnector(loop=loop)
    transp = mock.Mock()
    conn._conns['a'] = [(transp, 'proto', 123)]
    return conn

