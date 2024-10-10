import asyncio
from unittest import mock
from yarl import URL
import pytest
import aiohttp
from aiohttp.client import ClientRequest
from aiohttp.test_utils import unused_port

@pytest.mark.asyncio
async def test_resolver_not_called_with_address_is_ip(loop):
    resolver = mock.MagicMock()
    connector = aiohttp.TCPConnector(resolver=resolver)

    req = ClientRequest('GET',
                        URL('http://127.0.0.1:{}'.format(unused_port())),
                        loop=loop,
                        response_class=mock.Mock())

    with pytest.raises(OSError):
        await connector.connect(req)

    resolver.resolve.assert_not_called()