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
    
    def test_cookie_removed_on_expire(self):
        s = requests.session()
        s.get(httpbin('cookies/set?foo=bar'))
        assert s.cookies['foo'] == 'bar'
        s.get(
            httpbin('response-headers'),
            params={
                'Set-Cookie':
                    'foo=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT'
            }
        )
        assert 'foo' not in s.cookies