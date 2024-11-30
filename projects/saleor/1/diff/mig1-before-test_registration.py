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
    
    def test_facebook_login_url(self):
        """Facebook login url is properly generated"""
        facebook_client = FacebookClient(local_host='localhost')
        facebook_login_url = URL(facebook_client.get_login_uri())
        query = facebook_login_url.query_params()
        callback_url = URL(query['redirect_uri'][0])
        func, _args, kwargs = resolve(callback_url.path())
        self.assertEquals(func, oauth_callback)
        self.assertEquals(kwargs['service'], FACEBOOK)
        self.assertEqual(query['scope'][0], FacebookClient.scope)
        self.assertEqual(query['client_id'][0], str(FacebookClient.client_id))