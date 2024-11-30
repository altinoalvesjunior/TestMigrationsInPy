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
    
def test_google_login_url():
    google_client = GoogleClient(local_host='local_host')
    google_login_url = URL(google_client.get_login_uri())
    params = google_login_url.query_params()
    callback_url = URL(params['redirect_uri'][0])
    func, _args, kwargs = resolve(callback_url.path())
    assert func is oauth_callback
    assert kwargs['service'] == GOOGLE
    assert params['scope'][0] == GoogleClient.scope
    assert params['client_id'][0] == str(GoogleClient.client_id)