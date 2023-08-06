import json


class SDKException(Exception):
    '''
        This is the custom exception class for handling Client Library exceptions
        '''
    message = '{code} {message} {cause}'

    def __init__(self, code, message, details=None, cause=None):
        self.code = code
        self.cause = cause
        self.mess_dict = details
        self.error_message = "" if message is None else message
        if self.mess_dict is not None:
            self.error_message = self.error_message + json.dumps(self.mess_dict)
        if self.cause is not None:
            self.error_message = self.error_message + str(self.cause)
        Exception.__init__(self, code, message)

    def __str__(self):
        return self.message.format(code=self.code, message=self.error_message, cause=self.cause)
