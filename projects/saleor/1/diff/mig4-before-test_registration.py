from unittest import TestCase

from django.core.urlresolvers import resolve
from django.conf import settings
from django.http import HttpRequest
from mock import call, Mock, MagicMock, patch, sentinel
from purl import URL

from .forms import OAuth2CallbackForm
from .utils import (
    FACEBOOK,
    FacebookClient,
    GOOGLE,
    GoogleClient,
    OAuth2RequestAuthorizer,
    OAuth2Client,
    parse_response)
from .views import oauth_callback, change_email

URLENCODED_MIME_TYPE = 'application/x-www-form-urlencoded; charset=UTF-8'

class ResponseParsingTestCase(TestCase):
    def setUp(self):
        self.response = MagicMock()
    
    def test_parse_urlencoded(self):
        """OAuth2 client is able to parse urlencoded response"""
        self.response.headers = {'Content-Type': URLENCODED_MIME_TYPE}
        self.response.text = 'key=value&multi=a&multi=b'
        content = parse_response(self.response)
        self.assertEquals(content, {'key': 'value', 'multi': ['a', 'b']})
