import logging
import re
import traceback

from src.com.zoho.api.exception.sdk_exception import SDKException


class User(object):

    logger = logging.getLogger('client_lib')

    regex = '^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$'

    def __init__(self, email):

        error = {}

        try:

            if re.search(User.regex, email) is None:

                error['field'] = "email"

                error["expected_type"] = "email"

                raise SDKException("USER ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            self.email = email

        except SDKException as e:

            User.logger.error("Error during User Initialization" + e.__str__())
