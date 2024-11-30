"""Tests for Requests."""

from __future__ import division
import json
import os
import pickle
import unittest

import requests
import pytest
from requests.adapters import HTTPAdapter
from requests.auth import HTTPDigestAuth
from requests.compat import (
    Morsel, cookielib, getproxies, str, urljoin, urlparse)
from requests.cookies import cookiejar_from_dict, morsel_to_cookie

class TestMorselToCookieExpires(unittest.TestCase):

    """Tests for morsel_to_cookie when morsel contains expires."""
    
    def test_expires_invalid_int(self):
        """Test case where an invalid type is passed for expires."""

        morsel = Morsel()
        morsel['expires'] = 100
        with pytest.raises(TypeError):
            morsel_to_cookie(morsel)