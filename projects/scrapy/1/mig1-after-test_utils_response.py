import unittest
from time import process_time

import pytest

from scrapy.settings.default_settings import DOWNLOAD_MAXSIZE

from scrapy.utils.response import (
    get_base_url,
    get_meta_refresh,
    open_in_browser,
    response_httprepr,
    response_status_message,
)

class ResponseUtilsTest(unittest.TestCase):
    @pytest.mark.slow
    def test_open_in_browser_redos_comment():
        MAX_CPU_TIME = 30
        # Exploit input from
        # https://makenowjust-labs.github.io/recheck/playground/
        # for /<!--.*?-->/ (old pattern to remove comments).
        body = b"-><!--\x00" * (int(DOWNLOAD_MAXSIZE / 7) - 10) + b"->\n<!---->"
        response = HtmlResponse("https://example.com", body=body)

        start_time = process_time()

        open_in_browser(response, lambda url: True)

        end_time = process_time()
        assert (end_time - start_time) < MAX_CPU_TIME