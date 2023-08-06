
try:
    import logging
    import enum
    import traceback
    import json
    import time
    import requests
    from .token import Token
    from src.com.zoho.crm.api  import Initializer
    from ...crm.api.util import APIHTTPConnector
    from ..exception import SDKException
    from ...crm.api.util.constants import Constants

except Exception as e:
    import logging
    import enum
    import traceback
    import json
    import time
    import requests
    from .token import Token
    from src.com.zoho.crm.api import Initializer
    from ...crm.api.util import APIHTTPConnector
    from ..exception import SDKException
    from ...crm.api.util.constants import Constants


class TokenType(enum.Enum):
    grant = "GRANT"
    refresh = "REFRESH"


class OauthToken(Token):
    logger = logging.getLogger('client_lib')
    def __init__(self, clientid, clientsecret, redirecturl, token, tokentype):
        error = {}
        try:
            if not isinstance(clientid, str):
                error['field']="clientid"
                error['expected_type']="String"
                error['class']=OauthToken.__name__
                raise SDKException("TOKEN ERROR", None, details=error, cause=traceback.format_stack(limit=6))
            if not isinstance(clientsecret, str):
                error['field'] = "clientsecret"
                error['expected-type'] = "String"
                error['class']=OauthToken.__name__
                raise SDKException("TOKEN ERROR",
                                   None, details=error, cause=traceback.format_stack(limit=6))
            if not isinstance(redirecturl, str):
                error['field'] = "redirecturl"
                error['expected-type'] = "String"
                error['class']=OauthToken.__name__
                raise SDKException("TOKEN ERROR",
                                   None, details=error, cause=traceback.format_stack(limit=6))
            if not isinstance(token, str):
                error['field'] = "token"
                error['expected-type'] = "String"
                error['class']=OauthToken.__name__
                raise SDKException("TOKEN ERROR",
                                   None, details=error, cause=traceback.format_stack(limit=6))
            if not isinstance(tokentype, TokenType):
                error['field'] = "tokentype"
                error['expected-type'] = TokenType.__members__.keys()
                error['class']=OauthToken.__name__
                raise SDKException("TOKEN ERROR",
                                   None, details=error, cause=traceback.format_stack(limit=6))
            self.client_id = clientid
            self.client_secret = clientsecret
            self.redirect_url = redirecturl
            self.grant_token = token if (tokentype == TokenType.grant) else None
            self.refresh_token = token if (tokentype == TokenType.refresh) else None
            self.access_token = None
            self.expires_in = None
        except SDKException as e:
            OauthToken.logger.error('Exception in __init__() ' + e.__str__())

    def authenticate(self, http_instance):
        try:
            initializer = Initializer.get_initializer()
            store = initializer.store
            user  = initializer.user
            oauth_token = initializer.store.get_token(initializer.user, self)
            if oauth_token is None:
                token = self.generate_access_token(user,store).access_token if (self.refresh_token is None) else self.refresh_access_token(user,store).access_token
            elif int(oauth_token.expires_in) - int(time.time() * 1000) < 5000:
                token = self.refresh_access_token(user,store).access_token
            else:
                token = self.access_token
            zoho_oauth = Constants.OAUTH_HEADER_PREFIX + token
            http_instance.headers[Constants.AUTHORIZATION]=zoho_oauth
        except SDKException as e:
            OauthToken.logger.error('Exception in authenticate() ' + e.__str__())
            raise

    def refresh_access_token(self,user,store):
        try:
            url = Initializer.get_initializer().environment.accounts_url
            body = {
                Constants.REFRESH_TOKEN: self.refresh_token,
                Constants.CLIENT_ID: self.client_id,
                Constants.CLIENT_SECRET: self.client_secret,
                Constants.GRANT_TYPE: Constants.REFRESH_TOKEN
            }
            response = requests.post(url, data=body, params=None, headers=None, allow_redirects=False).json()
            self.parse_response(response_json=response)
            store.save_token(user, self)
        except SDKException as e:
            OauthToken.logger.error('Exception in refreshing access token - OAuthToken' + e.__str__())
            raise

        return self

    def generate_access_token(self,user,store):
        try:
            url = Initializer.get_initializer().environment.accounts_url
            body = {
                Constants.GRANT_TYPE: Constants.GRANT_TYPE_AUTH_CODE,
                Constants.CLIENT_ID: self.client_id,
                Constants.CLIENT_SECRET: self.client_secret,
                Constants.REDIRECT_URL: self.redirect_url,
                Constants.CODE: self.grant_token
            }
            response = requests.post(url, data=body, params=None, headers=None, allow_redirects=True).json()
            self.parse_response(response_json=response)
            store.save_token(user, self)
        except SDKException as e:
            OauthToken.logger.error('Exception in generating access token - OAuthToken' + e.__str__())

        return self

    def parse_response(self,response_json):
        response_json = dict(response_json)
        if not response_json.__contains__(Constants.ACCESS_TOKEN):
            raise SDKException(code="INVALID CLIENT ERROR", message=str(response_json.get('error')))
        self.access_token = response_json.get(Constants.ACCESS_TOKEN)
        if response_json.__contains__(Constants.REFRESH_TOKEN):
            self.refresh_token = response_json.get(Constants.REFRESH_TOKEN)
        self.expires_in = str(int(time.time() * 1000) + self.get_token_expires_in(response=response_json))  # expires in

    def get_token_expires_in(self, response):
        return int(response[Constants.EXPIRES_IN]) if Constants.EXPIRES_IN_SEC in response else int(response[Constants.EXPIRES_IN]) * 1000
