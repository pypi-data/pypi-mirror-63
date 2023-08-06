import base64
import platform
import sys
from threading import Timer

import requests

try:  # py3
    import urllib.parse as urlparse
except:  # py2
    import urlparse


class RestClient(object):
    def __init__(self, client_id, client_secret, server):
        self.client_id = client_id
        self.client_secret = client_secret
        self.server = server
        self._token = None
        self._timer = None
        self.auto_refresh = False
        self.debug = False

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        if self._timer:
            self._timer.cancel()
            self._timer = None
        if self.auto_refresh and value:
            self._timer = Timer(value['expires_in'] - 120, self.refresh)

            self._timer.start()

    def authorize(self,
                  username=None,
                  extension=None,
                  password=None,
                  auth_code=None,
                  redirect_uri=None):
        if auth_code:
            data = {
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': redirect_uri,
            }
        else:
            data = {
                'grant_type': 'password',
                'username': username,
                'extension': extension,
                'password': password,
            }
        r = self.post('/restapi/oauth/token', data=data)
        self.token = r.json()
        return r

    def refresh(self):
        if self.token is None:
            return
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.token['refresh_token'],
        }
        self.token = None
        r = self.post('/restapi/oauth/token', data=data)
        self.token = r.json()
        return r

    def revoke(self):
        '''
            Revokes access/refresh token.
            Requests to this endpoint must be authenticated with HTTP Basic scheme
            using client ID and client secret as login and password, correspondingly.
        '''
        if self.token is None:
            return None
        data = {'token': self.token['access_token']}
        self.token = None
        return self.post('/restapi/oauth/revoke', data=data)

    def authorize_uri(self, redirect_uri, state=''):
        '''
            TODO: why i need this?
            The authorization code is obtained by using an authorization server as an
            intermediary between the client and resource owner.
            Returns link to a login page location.
            Web applications are higly advised to use the Proof Key for
            Code Exchange scheme (PKCE) for security concerns.
        '''
        url = urlparse.urljoin(self.server, '/restapi/oauth/authorize')
        params = {
            'response_type': 'code',
            'state': state,
            'redirect_uri': redirect_uri,
            'client_id': self.client_id
        }
        req = requests.PreparedRequest()
        req.prepare_url(url, params=params)
        return req.url

    def get(self, endpoint, params=None):
        return self._request('GET', endpoint, params)

    def post(self, *args, **kwargs):
        return self._request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._request('PUT', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._request('PATCH', *args, **kwargs)

    def delete(self, endpoint, params=None):
        return self._request('DELETE', endpoint, params)

    def _autorization_header(self):
        if self.token:
            return 'Bearer {access_token}'.format(
                access_token=self.token['access_token'])
        return 'Basic {basic_key}'.format(basic_key=self._basic_key())

    def _basic_key(self):
        return base64.b64encode('{client_id}:{client_secret}'.format(
            client_id=self.client_id,
            client_secret=self.client_secret).encode('utf-8')).decode('utf-8')

    def _request(self,
                 method,
                 endpoint,
                 params=None,
                 json=None,
                 data=None,
                 files=None,
                 multipart_mixed=False):
        url = urlparse.urljoin(self.server, endpoint)
        user_agent_header = '{name} Python {major_lang_version}.{minor_lang_version} {platform}'.format(
            name='RCV DevOps RC SDK',
            major_lang_version=sys.version_info[0],
            minor_lang_version=sys.version_info[1],
            platform=platform.platform(),
        )
        headers = {
            'Authorization': self._autorization_header(),
            'User-Agent': user_agent_header,
            'RC-User-Agent': user_agent_header,
            'X-User-Agent': user_agent_header,
        }
        req = requests.Request(method,
                               url,
                               params=params,
                               data=data,
                               json=json,
                               files=files,
                               headers=headers)
        prepared = req.prepare()
        if multipart_mixed:
            prepared.headers['Content-Type'] = prepared.headers[
                'Content-Type'].replace('multipart/form-data;',
                                        'multipart/mixed;')
        if self.debug:
            pretty_print_POST(prepared)
        s = requests.Session()
        r = s.send(prepared)
        try:
            r.raise_for_status()
        except:
            raise Exception(
                'HTTP Status: {s} RCRequestId\n{h} Body: {t}'.format(
                    s=r.status_code,
                    t=r.text,
                    h=r.headers.get('RCRequestId', None)))
        return r


# Blow is for debugging:


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
