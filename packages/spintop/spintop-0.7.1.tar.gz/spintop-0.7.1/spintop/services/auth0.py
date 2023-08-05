
import json
import jwt
import requests
import time

from json.decoder import JSONDecodeError

from simple_memory_cache import GLOBAL_CACHE

from ..errors import AuthUnauthorized, ExpiredAccessToken

class Auth0Error(AuthUnauthorized):
    def __init__(self, content):
        self.content = content
        desc = self.error_description
        if not desc:
            desc = str(content)
        super().__init__(desc)

    @property
    def error(self):
        return self.content.get('error', None)

    @property
    def error_description(self):
        return self.content.get('error_description', None)

class Auth0Provider(object):
    def __init__(self, domain, audience, client_id, jwks_url, user_info_url):
        self.domain = domain
        self.audience = audience
        self.client_id = client_id
        self.jwks_url = jwks_url
        self.user_info_url = user_info_url

        self.cached_jwks = GLOBAL_CACHE.MemoryCachedVar('auth_jwks')
        self.cached_jwks.on_first_access(self._retrieve_jwks)

    def _retrieve_jwks(self):
        return requests.get(self.jwks_url).json()
    
    def get_user_info(self, access_token):
        return requests.get(self.user_info_url, headers=self.get_auth_headers(access_token)).json()

    def get_auth_headers(self, access_token):
        return {'Authorization': 'Bearer ' + access_token}

    def authenticate(self, username, password, scopes=[]):
        return self._execute_request('/oauth/token',
            grant_type = 'password',
            username = username,
            password = password,
            audience = self.audience,
            client_id = self.client_id,
            scope = 'offline_access ' + ' '.join(scopes) # Special scope to receive a refresh token
        )

    def DeviceAuthorizationFlow(self):
        return DeviceAuthorizationFlow(self)

    def request_device_code(self, scopes=[]):
        return self._execute_request('/oauth/device/code',
            audience = self.audience,
            client_id = self.client_id,
            scope = 'offline_access ' + ' '.join(scopes) # Special scope to receive a refresh token
        )

    def check_device_code_approval(self, device_code):
        return self._execute_request('/oauth/token',
            grant_type = 'urn:ietf:params:oauth:grant-type:device_code',
            device_code = device_code,
            client_id = self.client_id
        )
    
    def _execute_request(self, url_path, **data):
        URL = 'https://' + self.domain  + url_path
        resp = requests.post(URL, data = data)
        content = self._handle_errors_in_content(resp)
        return content
    
    def _handle_errors_in_content(self, resp):
        try:
            content = resp.json()
        except JSONDecodeError:
            content = {}
            
        if resp.status_code >= 400:
            raise Auth0Error(content)
    
        return content
    
    def refresh_access_token(self, refresh_token):
        return self._execute_request('/oauth/token',
            grant_type = 'refresh_token',
            client_id = self.client_id,
            refresh_token = refresh_token
        )

    def revoke_refresh_token(self, refresh_token):
        self._execute_request('/oauth/revoke',
            client_id = self.client_id,
            token = refresh_token
        )
    
    def get_jwks_key(self, access_token):
        jwks = self.cached_jwks.get()
        public_keys = {}
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
            
        kid = jwt.get_unverified_header(access_token)['kid']
        key = public_keys[kid]
        return key

    def jwt_verify(self, access_token):
        try:
            payload = self.decode(access_token)
        except jwt.ExpiredSignatureError:
            raise ExpiredAccessToken("Token Expired")
        except jwt.PyJWTError:
            # invalidate jwks cache and try ONCE more.
            self.cached_jwks.invalidate()
            payload = self.decode(access_token)
        return payload
    
    def decode(self, access_token):
        key = self.get_jwks_key(access_token)
        return jwt.decode(access_token, key=key, algorithms=['RS256'], audience=[self.client_id, self.audience])

class DeviceAuthorizationFlow(object):
    def __init__(self, auth0_provider):
        self.auth0 = auth0_provider
        self.device_code_response = None

    def request_verification_url(self, scopes=[]):
        self.device_code_response = self.auth0.request_device_code(scopes=scopes)
        return self.device_code_response["verification_uri_complete"]

    def wait_for_approval(self):
        interval = self.device_code_response["interval"]
        expires_in = self.device_code_response["expires_in"]
        device_code = self.device_code_response["device_code"]

        start = time.time()

        response = None

        while time.time() - start < expires_in:
            try:
                response = self.auth0.check_device_code_approval(device_code)
                break
            except Auth0Error as e:
                if e.error == "expired_token":
                    raise AuthUnauthorized("Did not receive an access token in time.")
                elif e.error == "access_denied":
                    raise AuthUnauthorized("User did not accept access.")
                elif e.error == "slow_down":
                    interval = interval + 2
                else:
                    # authorization_pending
                    pass
                    
                time.sleep(interval)
        
        if not response:
            raise AuthUnauthorized("No access token received.")
            
        return response
    
    
