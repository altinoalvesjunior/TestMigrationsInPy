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
    
    def test_unicode_multipart_post(self):
        r = requests.post(httpbin('post'),
                          data={'stuff': u'ëlïxr'},
                          files={'file': ('test_requests.py', open(__file__, 'rb'))})
        self.assertEqual(r.status_code, 200)

        r = requests.post(httpbin('post'),
                          data={'stuff': u'ëlïxr'.encode('utf-8')},
                          files={'file': ('test_requests.py', open(__file__, 'rb'))})
        self.assertEqual(r.status_code, 200)

        r = requests.post(httpbin('post'),
                          data={'stuff': 'elixr'},
                          files={'file': ('test_requests.py', open(__file__, 'rb'))})
        self.assertEqual(r.status_code, 200)

        r = requests.post(httpbin('post'),
                          data={'stuff': 'elixr'.encode('utf-8')},
                          files={'file': ('test_requests.py', open(__file__, 'rb'))})
        self.assertEqual(r.status_code, 200)