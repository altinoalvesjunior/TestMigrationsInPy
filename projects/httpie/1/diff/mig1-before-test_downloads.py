import os
import time
from unittest import TestCase

from requests.structures import CaseInsensitiveDict

from httpie.compat import urlopen
from httpie.downloads import (
    parse_content_range,
    filename_from_content_disposition,
    filename_from_url,
    get_unique_filename,
    ContentRangeError,
    Download,
)
from tests import httpbin, http, TestEnvironment

class DownloadUtilsTest(TestCase):
    def test_Content_Range_parsing(self):
        parse = parse_content_range

        assert parse('bytes 100-199/200', 100) == 200
        assert parse('bytes 100-199/*', 100) == 200

        # missing
        self.assertRaises(ContentRangeError, parse, None, 100)

        # syntax error
        self.assertRaises(ContentRangeError, parse, 'beers 100-199/*', 100)

        # unexpected range
        self.assertRaises(ContentRangeError, parse, 'bytes 100-199/*', 99)

        # invalid instance-length
        self.assertRaises(ContentRangeError, parse, 'bytes 100-199/199', 100)

        # invalid byte-range-resp-spec
        self.assertRaises(ContentRangeError, parse, 'bytes 100-99/199', 100)

        # invalid byte-range-resp-spec
        self.assertRaises(ContentRangeError, parse, 'bytes 100-100/*', 100)
