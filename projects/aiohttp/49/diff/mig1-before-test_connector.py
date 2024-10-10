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

def test_ip_addresses(self):
        ip_addresses = [
            '0.0.0.0',
            '127.0.0.1',
            '255.255.255.255',
            '0:0:0:0:0:0:0:0',
            'FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF',
            '00AB:0002:3008:8CFD:00AB:0002:3008:8CFD',
            '00ab:0002:3008:8cfd:00ab:0002:3008:8cfd',
            'AB:02:3008:8CFD:AB:02:3008:8CFD',
            'AB:02:3008:8CFD::02:3008:8CFD',
            '::',
            '1::1',
        ]
        for address in ip_addresses:
            assert helpers.is_ip_address(address) is True