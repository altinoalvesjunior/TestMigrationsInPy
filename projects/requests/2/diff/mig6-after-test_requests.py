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

class TestMorselToCookieMaxAge(unittest.TestCase):

    """Tests for morsel_to_cookie when morsel contains max-age."""
    
    def test_max_age_invalid_str(self):
        """Test case where a invalid max age is passed."""

        morsel = Morsel()
        morsel['max-age'] = 'woops'
        with pytest.raises(TypeError):
            morsel_to_cookie(morsel)