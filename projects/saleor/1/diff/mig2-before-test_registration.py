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

class LoginUrlsTestCase(TestCase):
    """Tests login url generation."""
    
    def test_google_login_url(self):
        """Google login url is properly generated"""
        google_client = GoogleClient(local_host='local_host')
        google_login_url = URL(google_client.get_login_uri())
        params = google_login_url.query_params()
        callback_url = URL(params['redirect_uri'][0])
        func, _args, kwargs = resolve(callback_url.path())
        self.assertEquals(func, oauth_callback)
        self.assertEquals(kwargs['service'], GOOGLE)
        self.assertTrue(params['scope'][0] in GoogleClient.scope)
        self.assertEqual(params['client_id'][0], str(GoogleClient.client_id))