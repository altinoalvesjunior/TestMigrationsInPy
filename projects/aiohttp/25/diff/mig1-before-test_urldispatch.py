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
                         HTTPMethodNotAllowed, HTTPNotFound,
                         HTTPCreated)
from aiohttp.web_urldispatcher import (_defaultExpectHandler,
                                       DynamicRoute,
                                       PlainRoute,
                                       SystemRoute,
                                       ResourceRoute,
                                       AbstractResource,
                                       View)
from aiohttp.test_utils import make_mocked_request


class TestUrlDispatcher(unittest.TestCase):
     def test_system_route(self):
        route = SystemRoute(HTTPCreated(reason='test'))
        self.assertIsNone(route.match('any'))
        with self.assertRaises(RuntimeError):
            route.url()
        self.assertEqual("<SystemRoute 201: test>", repr(route))
        self.assertEqual(201, route.status)
        self.assertEqual('test', route.reason)