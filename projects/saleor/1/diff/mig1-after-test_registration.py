
#mig=assert

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
URLENCODED_MIME_TYPE = 'application/x-www-form-urlencoded; charset=UTF-8'


class SessionMock(Mock):

    def __setitem__(self, key, value):
        pass
    
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


def test_parse_json():
    response = MagicMock()
    response.headers = {'Content-Type': JSON_MIME_TYPE}
    response.json.return_value = sentinel.json_content
    content = parse_response(response)
    assert content == sentinel.json_content


def test_parse_urlencoded():
    response = MagicMock()
    response.headers = {'Content-Type': URLENCODED_MIME_TYPE}
    response.text = 'key=value&multi=a&multi=b'
    content = parse_response(response)
    assert content == {'key': 'value', 'multi': ['a', 'b']}
    
class Client(OAuth2Client):
    """OAuth2Client configured for testing purposes."""
    service = sentinel.service

    client_id = sentinel.client_id
    client_secret = sentinel.client_secret

    auth_uri = sentinel.auth_uri
    token_uri = sentinel.token_uri
    user_info_uri = sentinel.user_info_uri

    scope = sentinel.scope

    def get_redirect_uri(self):
        return sentinel.redirect_uri

    def extract_error_from_response(self, response_content):
        return 'some error'

class AccessTokenTestCase(BaseCommunicationTestCase):
    """Tests obtaining access_token."""

    def setUp(self):
        super(AccessTokenTestCase, self).setUp()

        self.parse_mock.return_value = {'access_token': sentinel.access_token}

        self.access_token_response = MagicMock()
        self.requests_mock.post.return_value = self.access_token_response
    
    def test_token_is_obtained_on_construction(self):
        """OAuth2 client asks for access token if interim code is available"""
        self.access_token_response.status_code = sentinel.ok
        Client(local_host='http://localhost', code=sentinel.code)
        self.requests_mock.post.assert_called_once()

    def test_token_success(self):
        """OAuth2 client properly obtains access token"""
        client = Client(local_host='http://localhost')
        self.access_token_response.status_code = sentinel.ok
        access_token = client.get_access_token(code=sentinel.code)
        self.assertEquals(access_token, sentinel.access_token)
        self.requests_mock.post.assert_called_once_with(
            sentinel.token_uri,
            data={'grant_type': 'authorization_code',
                  'client_id': sentinel.client_id,
                  'client_secret': sentinel.client_secret,
                  'code': sentinel.code,
                  'redirect_uri': sentinel.redirect_uri,
                  'scope': sentinel.scope},
            auth=None)

    
    def test_token_failure(self):
        """OAuth2 client properly reacts to access token fetch failure"""
        client = Client(local_host='http://localhost')
        self.access_token_response.status_code = sentinel.fail
        self.assertRaises(ValueError, client.get_access_token,
                          code=sentinel.code)
    
    def test_user_info_success(self):
        """OAuth2 client properly fetches user info"""
        client = Client(local_host='http://localhost')
        self.parse_mock.return_value = sentinel.user_info
        self.user_info_response.status_code = sentinel.ok
        user_info = client.get_user_info()
        self.assertEquals(user_info, sentinel.user_info)

    def test_user_data_failure(self):
        """OAuth2 client reacts well to user info fetch failure"""
        client = Client(local_host='http://localhost')
        self.assertRaises(ValueError, client.get_user_info)