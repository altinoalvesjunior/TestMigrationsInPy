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


JSON_MIME_TYPE = 'application/json; charset=UTF-8'

class ResponseParsingTestCase(TestCase):
    def setUp(self):
        self.response = MagicMock()
        
    def test_parse_json(self):
        """OAuth2 client is able to parse json response"""
        self.response.headers = {'Content-Type': JSON_MIME_TYPE}
        self.response.json.return_value = sentinel.json_content
        content = parse_response(self.response)
        self.assertEquals(content, sentinel.json_content)