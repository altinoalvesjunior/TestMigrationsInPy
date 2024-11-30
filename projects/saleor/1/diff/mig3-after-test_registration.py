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

def test_parse_json():
    response = MagicMock()
    response.headers = {'Content-Type': JSON_MIME_TYPE}
    response.json.return_value = sentinel.json_content
    content = parse_response(response)
    assert content == sentinel.json_content