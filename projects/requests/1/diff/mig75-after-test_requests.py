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

class UtilsTestCase(unittest.TestCase):

    def test_super_len_io_streams(self):
        """ Ensures that we properly deal with different kinds of IO streams. """
        # uses StringIO or io.StringIO (see import above)
        from io import BytesIO
        from requests.utils import super_len

        assert super_len(StringIO.StringIO()) == 0
        assert super_len(StringIO.StringIO('with so much drama in the LBC')) == 29

        assert super_len(BytesIO()) == 0
        assert super_len(BytesIO(b"it's kinda hard bein' snoop d-o-double-g")) == 40

        try:
            import cStringIO
        except ImportError:
            pass
        else:
            assert super_len(cStringIO.StringIO('but some how, some way...')) == 25