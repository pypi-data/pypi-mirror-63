class Constants(object):
    '''
    This module holds the constants required for the client library
    '''
    ERROR = "error"
    REQUEST_METHOD_GET = "GET"
    REQUEST_METHOD_POST = "POST"
    REQUEST_METHOD_PUT = "PUT"
    REQUEST_METHOD_DELETE = "DELETE"

    OAUTH_HEADER_PREFIX = "Zoho-oauthtoken "
    AUTHORIZATION = "Authorization"

    API_NAME = "api_name"
    INVALID_ID_MSG = "The given id seems to be invalid."
    API_MAX_RECORDS_MSG = "Cannot process more than 100 records at a time."
    INVALID_DATA = "INVALID_DATA"

    CODE_SUCCESS = "SUCCESS"

    STATUS_SUCCESS = "success"
    STATUS_ERROR = "error"
    TAG = "tags"
    LEADS = "Leads"
    ACCOUNTS = "Accounts"
    CONTACTS = "Contacts"
    DEALS = "Deals"
    QUOTES = "Quotes"
    SALESORDERS = "SalesOrders"
    INVOICES = "Invoices"
    PURCHASEORDERS = "PurchaseOrders"

    PER_PAGE = "per_page"
    PAGE = "page"
    COUNT = "count"
    MORE_RECORDS = "more_records"

    MESSAGE = "message"
    CODE = "code"
    STATUS = "status"
    DETAILS = "details"
    TAXES = "taxes"
    DATA = "data"
    INFO = "info"
    FIELDS = 'fields'
    LAYOUTS = 'layouts'
    CUSTOM_VIEWS = 'custom_views'
    MODULES = 'modules'
    RELATED_LISTS = 'related_lists'
    ORG = 'org'
    ROLES = 'roles'
    PROFILES = 'profiles'
    USERS = 'users'

    RESPONSECODE_OK = 200
    RESPONSECODE_CREATED = 201
    RESPONSECODE_ACCEPTED = 202
    RESPONSECODE_NO_CONTENT = 204
    RESPONSECODE_MOVED_PERMANENTLY = 301
    RESPONSECODE_MOVED_TEMPORARILY = 302
    RESPONSECODE_NOT_MODIFIED = 304
    RESPONSECODE_BAD_REQUEST = 400
    RESPONSECODE_AUTHORIZATION_ERROR = 401
    RESPONSECODE_FORBIDDEN = 403
    RESPONSECODE_NOT_FOUND = 404
    RESPONSECODE_METHOD_NOT_ALLOWED = 405
    RESPONSECODE_REQUEST_ENTITY_TOO_LARGE = 413
    RESPONSECODE_UNSUPPORTED_MEDIA_TYPE = 415
    RESPONSECODE_TOO_MANY_REQUEST = 429
    RESPONSECODE_INTERNAL_SERVER_ERROR = 500
    RESPONSECODE_INVALID_INPUT = 0

    DOWNLOAD_FILE_PATH = "../../../../../../resources"

    USER_EMAIL_ID = "user_email_id"
    CURRENT_USER_EMAIL = "currentUserEmail"
    API_BASEURL = "apiBaseUrl"
    API_VERSION = "apiVersion"
    APPLICATION_LOGFILE_PATH = "applicationLogFilePath"
    ACTION = "action"
    DUPLICATE_FIELD = "duplicate_field"
    NO_CONTENT = "No Content"
    FAULTY_RESPONSE_CODES = [RESPONSECODE_NO_CONTENT, RESPONSECODE_NOT_FOUND, RESPONSECODE_AUTHORIZATION_ERROR,
                             RESPONSECODE_BAD_REQUEST, RESPONSECODE_FORBIDDEN, RESPONSECODE_INTERNAL_SERVER_ERROR,
                             RESPONSECODE_METHOD_NOT_ALLOWED, RESPONSECODE_MOVED_PERMANENTLY,
                             RESPONSECODE_MOVED_TEMPORARILY, RESPONSECODE_REQUEST_ENTITY_TOO_LARGE,
                             RESPONSECODE_TOO_MANY_REQUEST, RESPONSECODE_UNSUPPORTED_MEDIA_TYPE]
    ATTACHMENT_URL = "attachmentUrl"

    ACCESS_TOKEN_EXPIRY = "X-ACCESSTOKEN-RESET"
    CURR_WINDOW_API_LIMIT = "X-RATELIMIT-LIMIT"
    CURR_WINDOW_REMAINING_API_COUNT = "X-RATELIMIT-REMAINING"
    CURR_WINDOW_RESET = "X-RATELIMIT-RESET"
    API_COUNT_REMAINING_FOR_THE_DAY = "X-RATELIMIT-DAY-REMAINING"
    API_LIMIT_FOR_THE_DAY = "X-RATELIMIT-DAY-LIMIT"

    GRANT_TYPE = "grant_type"
    GRANT_TYPE_AUTH_CODE = "authorization_code"
    ACCESS_TOKEN = "access_token"
    EXPIRES_IN = "expires_in"
    EXPIRES_IN_SEC = "expires_in_sec"
    REFRESH_TOKEN = "refresh_token"
    CLIENT_ID = "client_id"
    CLIENT_SECRET = "client_secret"
    REDIRECT_URL = "redirect_uri"
    TYPE_VS_DATATYPE = {
        "String": str,
        "List": list,
        "Integer": int,
        "HashMap": dict,
        "Map": dict,
        "Long": float
    }
    ZOHO_SDK = "X-ZOHO-SDK"
    SDK_VERSION = "3.0.0"
    CONTENT_DISPOSITION = "Content-Disposition"
