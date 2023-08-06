try:
    import logging
    import os
    import json
    import traceback
    import threading
    from src.com.zoho.api.authenticator.store.token_store import TokenStore
    from src.com.zoho.api.exception.sdk_exception import SDKException
    from src.com.zoho.crm.api.user import User
    from src.com.zoho.crm.api.dc.data_center import DataCenter
except Exception:
    import logging
    import os
    import json
    import traceback
    import threading
    from ...api.authenticator.store.token_store import TokenStore
    from ...api.exception.sdk_exception import SDKException
    from ..api.user import User
    from ..api.dc.data_center import DataCenter


class Initializer(object):
    logger = logging.getLogger('client_lib')
    json_details = None
    environment = None
    user = None
    store = None
    token = None
    initializer = None
    LOCAL = threading.local()
    LOCAL.init = None

    @classmethod
    def initialize(cls, user, environment, token, store, log=None):
        error = {}
        try:
            from .logger import Log, SDKLogger
        except Exception:
            from src.com.zoho.crm.api.logger import Log, SDKLogger
        if log is not None:
            SDKLogger.initialize(log.level, log.path)
        else:
            SDKLogger.initialize(Log.Levels.INFO, os.path.join(os.getcwd(), 'sdk_logs.log'))
        try:
            from src.com.zoho.api.authenticator.token import Token
            if not isinstance(user, User):
                error['field'] = "user"
                error['expected-type'] = User.__name__
                raise SDKException("INITIALIZATION ERROR", None, details=error, cause=traceback.format_stack(limit=6))
            if not isinstance(environment, DataCenter.Environment):
                error['field'] = "environment"
                error['expected-type'] = DataCenter.Environment.__name__
                raise SDKException("INITIALIZATION ERROR", None, details=error, cause=traceback.format_stack(limit=6))
            if not isinstance(store, TokenStore):
                error['field'] = "store"
                error['expected-type'] = TokenStore.__name__
                raise SDKException("INITIALIZATION ERROR", None, details=error, cause=traceback.format_stack(limit=6))
            if not isinstance(token, Token):
                error['field'] = "token"
                error['expected-type'] = Token.__name__
                raise SDKException("INITIALIZATION ERROR", None, details=error, cause=traceback.format_stack(limit=6))
            cls.environment = environment
            cls.user = user
            cls.token = token
            cls.store = store
            cls.initializer = cls

        except SDKException as e:
            cls.logger.error("Error during Initialization" + e.__str__())
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '..', '..', '..', '..', 'json_details.json')
        with open(filename, mode='r') as JSON:
            cls.json_details = json.load(JSON)

    @classmethod
    def get_initializer(cls):
        if Initializer.LOCAL.init is not None:
            return Initializer.LOCAL.init
        return cls.initializer

    @classmethod
    def switch_user(cls, user, environment, token):
        cls.user = user
        cls.environment = environment
        cls.token = token
        cls.store = Initializer.initializer.store
        Initializer.LOCAL.init = cls.initializer

