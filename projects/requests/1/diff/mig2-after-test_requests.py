"""Tests for Requests."""

from __future__ import division
import json
import os
import unittest
import pickle

import requests
import pytest
from requests.auth import HTTPDigestAuth
from requests.adapters import HTTPAdapter
from requests.compat import str, cookielib, getproxies, urljoin, urlparse
from requests.cookies import cookiejar_from_dict
from requests.exceptions import InvalidURL, MissingSchema
from requests.structures import CaseInsensitiveDict

try:
    import StringIO
except ImportError:
    import io as StringIO

HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
# Issue #1483: Make sure the URL always has a trailing slash
HTTPBIN = HTTPBIN.rstrip('/') + '/'


def httpbin(*suffix):
    """Returns url for HTTPBIN resource."""
    return urljoin(HTTPBIN, '/'.join(suffix))


class RequestsTestCase(unittest.TestCase):

    _multiprocess_can_split_ = True

    def setUp(self):
        """Create simple data set with headers."""
        pass

    def tearDown(self):
        """Teardown."""
        pass
    
    def test_no_content_length(self):
        get_req = requests.Request('GET', httpbin('get')).prepare()
        assert 'Content-Length' not in get_req.headers
        head_req = requests.Request('HEAD', httpbin('head')).prepare()
        assert 'Content-Length' not in head_req.headers