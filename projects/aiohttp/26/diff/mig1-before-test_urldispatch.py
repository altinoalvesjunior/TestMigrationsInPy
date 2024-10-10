import asyncio
import os
import pathlib
import re
import unittest
from collections.abc import Sized, Container, Iterable, Mapping, MutableMapping
from urllib.parse import unquote
import aiohttp.web
from aiohttp import hdrs
from aiohttp.web import (UrlDispatcher, Response,
                         HTTPMethodNotAllowed, HTTPNotFound)
from aiohttp.web_urldispatcher import (_defaultExpectHandler,
                                       DynamicRoute,
                                       PlainRoute,
                                       SystemRoute,
                                       ResourceRoute,
                                       AbstractResource,
                                       View)
from aiohttp.test_utils import make_mocked_request


class TestUrlDispatcher(unittest.TestCase):
    def test_register_route(self):
        handler = self.make_handler()
        route = PlainRoute('GET', handler, 'test', '/handler/to/path')
        self.router.register_route(route)
        req = self.make_request('GET', '/handler/to/path')
        info = self.loop.run_until_complete(self.router.resolve(req))
        self.assertIsNotNone(info)
        self.assertEqual(0, len(info))
        self.assertIs(route, info.route)
        self.assertIs(handler, info.handler)
        self.assertEqual(info.route.name, 'test')