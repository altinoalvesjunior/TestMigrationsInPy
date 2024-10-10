import asyncio
import datetime
import http.cookies
import unittest
from unittest import mock

import pytest

from aiohttp import helpers, test_utils

def test_host_addresses():
    hosts = [
        'www.four.part.host'
        'www.python.org',
        'foo.bar',
        'localhost',
    ]
    for host in hosts:
        assert not helpers.is_ip_address(host)