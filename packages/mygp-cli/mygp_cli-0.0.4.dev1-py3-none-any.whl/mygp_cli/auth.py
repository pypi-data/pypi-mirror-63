import datetime
import logging
import requests

# from common.infrastructure.decorators.logging import LogCall
from mygp_cli.auth_info import AuthInfo, ClientId

LOG = logging.getLogger(__name__)


class ApiAuthRequestFailed(Exception):
    """Request to API authentication resource failed"""
    pass


# get_token() {
#   TKN=$(curl -s \
#     -d "client_id=admin-cli" \
#     -d "username=$username" \
#     -d "password=$password" \
#     -d "grant_type=password" \
#     "$url/realms/master/protocol/openid-connect/token" \
#     | jq -r '.access_token')
# }


class BaseAdminApiAuth(object):

    def __init__(self, root_url, client_id: ClientId, realm='master'):
        self._root_url = root_url
        self._client_id = client_id
        self._access_token = None
        self._access_token_valid_until = None
        self._refresh_token = None
        self._refresh_token_valid_until = None
        self._realm = realm

    # @LogCall(logging.DEBUG)
    def get_token(self):
        dt_now = datetime.datetime.now()
        if (self._access_token is None) \
                or (dt_now >= self._access_token_valid_until):
            if (self._refresh_token_valid_until is not None) \
                    and (self._refresh_token_valid_until > dt_now):
                try:
                    self._get_refreshed_token()
                except ApiAuthRequestFailed:
                    LOG.info('reauth with refresh token failed; requesting '
                             'new access token')
                    self._get_new_tokens()
            else:
                self._get_new_tokens()
        return self._access_token

    # @LogCall(logging.DEBUG)
    def expire_access_token(self):
        self._access_token_valid_until = datetime.datetime.now()

    # @LogCall(logging.DEBUG)
    def _request_new_tokens(self, url):
        raise NotImplementedError()

    # @LogCall(logging.DEBUG)
    def _get_new_tokens(self):
        url = '%s/realms/%s/protocol/openid-connect/token' \
              % (self._root_url, self._realm)
        response = self._request_new_tokens(url)
        LOG.debug('auth response status code is %s', response.status_code)
        if response.status_code == 200:
            rjson = response.json()
            self._access_token_valid_until \
                = (datetime.datetime.now()
                   + datetime.timedelta(seconds=(rjson['expires_in'] - 60)))
            self._refresh_token_valid_until \
                = (datetime.datetime.now()
                   + datetime.timedelta(
                        seconds=(rjson['refresh_expires_in'] - 60)))
            self._access_token = rjson['access_token']
            self._refresh_token = rjson['refresh_token']
        else:
            LOG.warning('auth response: %s %s', response.status_code,
                        response.text)
            if response.status_code == 400:
                raise ApiAuthRequestFailed(
                    'API auth request rejected by server with status code 400')
            elif response.status_code == 401 or response.status_code == 403:
                raise ApiAuthRequestFailed(
                    'API auth request rejected by server because of '
                    'unfulfilled authorisation constraints')
            elif response.status_code == 404:
                raise ApiAuthRequestFailed(
                    'API auth request was probably sent to incorrect target '
                    'URL')
            else:
                raise ApiAuthRequestFailed(
                    'API auth request failed because of server error')

    # @LogCall(logging.DEBUG)
    def _get_refreshed_token(self):
        url = '%s/realms/%s/protocol/openid-connect/token' \
              % (self._root_url, self._realm)
        data = dict(
            grant_type='refresh_token',
            client_id=self._client_id.value,
            refresh_token=self._refresh_token
        )

        authrsp = requests.post(url, data=data)
        LOG.debug('reauth response status code is %s', authrsp.status_code)
        if authrsp.status_code != 200:
            LOG.warning(
                'auth response: %s %s', authrsp.status_code, authrsp.text)
            raise ApiAuthRequestFailed(
                'API reauth request with refresh token failed')
        rjson = authrsp.json()
        self._access_token_valid_until \
            = (datetime.datetime.now()
               + datetime.timedelta(seconds=(rjson['expires_in'] - 60)))
        self._access_token = rjson['access_token']


class ClientCredentialsAdminApiAuth(BaseAdminApiAuth):

    # @LogCall(logging.DEBUG)
    def __init__(self, root_url, auth_info: AuthInfo, realm='master'):
        super(ClientCredentialsAdminApiAuth, self)\
            .__init__(root_url, auth_info.client_id, realm)
        self._auth_info = auth_info

    # @LogCall(logging.DEBUG)
    def _request_new_tokens(self, url):
        data = dict(
            grant_type='client_credentials',
            client_id=self._client_id.value,
            client_secret=self._auth_info.client_secret.value
        )
        return requests.post(url, data=data)
