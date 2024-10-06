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
    
    def test_basicauth_with_netrc(self):
        auth = ('user', 'pass')
        wrong_auth = ('wronguser', 'wrongpass')
        url = httpbin('basic-auth', 'user', 'pass')

        def get_netrc_auth_mock(url):
            return auth
        requests.sessions.get_netrc_auth = get_netrc_auth_mock

        # Should use netrc and work.
        r = requests.get(url)
        assert r.status_code == 200

        # Given auth should override and fail.
        r = requests.get(url, auth=wrong_auth)
        assert r.status_code == 401

        s = requests.session()

        # Should use netrc and work.
        r = s.get(url)
        assert r.status_code == 200

        # Given auth should override and fail.
        s.auth = wrong_auth
        r = s.get(url)
        assert r.status_code == 401