import pytest
from aiohttp import helpers

def test_requote_uri_with_unquoted_percents():
    # Ensure we handle unquoted percent signs in redirects.
    bad_uri = 'http://example.com/fiz?buz=%ppicture'
    quoted = 'http://example.com/fiz?buz=%25ppicture'
    assert quoted == helpers.requote_uri(bad_uri)

def test_requote_uri_properly_requotes():
    # Ensure requoting doesn't break expectations.
    quoted = 'http://example.com/fiz?buz=%25ppicture'
    assert quoted == helpers.requote_uri(quoted)