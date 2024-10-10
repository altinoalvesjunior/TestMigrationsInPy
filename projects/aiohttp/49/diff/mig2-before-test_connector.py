import asyncio
import gc
import os.path
import shutil
import socket
import ssl
import tempfile
import unittest
from unittest import mock

import pytest

import aiohttp
from aiohttp import client, helpers, web
from aiohttp.client import ClientRequest
from aiohttp.connector import Connection
from aiohttp.test_utils import unused_port

def test_host_addresses(self):
        hosts = [
            'www.four.part.host'
            'www.python.org',
            'foo.bar',
            'localhost',
        ]
        for host in hosts:
            assert helpers.is_ip_address(host) is False