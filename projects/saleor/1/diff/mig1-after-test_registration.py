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

def test_facebook_login_url():
    facebook_client = FacebookClient(local_host='localhost')
    facebook_login_url = URL(facebook_client.get_login_uri())
    query = facebook_login_url.query_params()
    callback_url = URL(query['redirect_uri'][0])
    func, _args, kwargs = resolve(callback_url.path())
    assert func is oauth_callback
    assert kwargs['service'] == FACEBOOK
    assert query['scope'][0] == FacebookClient.scope
    assert query['client_id'][0] == str(FacebookClient.client_id)