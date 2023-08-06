try:

    import sys
    import traceback
    import zlib
    import base64
    import re

except Exception:

    import sys
    import traceback
    import zlib
    import base64
    import re

if sys.version > '3':

    from abc import ABC, abstractmethod

    class Converter(ABC):

        def __init__(self, common_api_handler):

            self.common_api_handler = common_api_handler

        @abstractmethod
        def get_response(self, response_json, class_path):

            pass

        @abstractmethod
        def form_request(self, request_instance, class_path, instance_no):

            pass

        @abstractmethod
        def append_to_request(self, request_base, request_object):

            pass

        @abstractmethod
        def get_wrapped_response(self, response, status_code):
            pass

        def value_checker(self, class_name, member_name, key_details, value, unique_values_map, instance_number):

            from src.com.zoho.api.exception import SDKException

            from .constants import Constants

            error = {}

            # Data Type Validation
            if key_details['type'] != 'com.zoho.crm.api.util.StreamWrapper':
                if not isinstance(value, Constants.TYPE_VS_DATATYPE.get(key_details['type'])):

                    error['index'] = instance_number

                    error['class_name'] = class_name

                    error['member_name'] = key_details['name']

                    error['accepted_type'] = key_details['type']

                    raise SDKException("TYPE ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('values'):

                if value not in key_details['values']:

                    error['index'] = instance_number

                    error['class'] = class_name

                    error['field'] = member_name

                    error['accepted_values'] = key_details['values']

                    raise SDKException("UNACCEPTED VALUES ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('min-length'):

                if len(str(value)) < key_details['min-length']:

                    error['index'] = instance_number

                    error['class'] = class_name

                    error['field'] = member_name

                    error['minimum_length'] = key_details['min-length']

                    raise SDKException("MIN-LENGTH ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('max-length'):

                if len(str(value)) > key_details['max-length']:

                    error['index'] = instance_number

                    error['class'] = class_name

                    error['field'] = member_name

                    error['maximum_length'] = key_details['max-length']

                    raise SDKException("MAX-LENGTH ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('regex'):

                if re.search(value, key_details['regex']) is None:

                    error['index'] = instance_number

                    error['class'] = class_name

                    error['field'] = member_name

                    raise SDKException("REGEX MISMATCH ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('unique'):

                if key_details['unique']:

                    if key_details['name'] not in unique_values_map:

                        unique_values_map[key_details['name']] = []

                    if value in unique_values_map[key_details['name']]:

                        error['first-index'] = unique_values_map[key_details['name']].index(value) + 1

                        error['next-index'] = instance_number

                        error['class'] = class_name

                        error['field'] = member_name

                        raise SDKException("UNIQUE KEY ERROR", None, details=error, cause=traceback.format_stack(limit=6))

                    unique_values_map[key_details['name']].append(value)

            return True

        def get_record_json_file_path(self):

            import src.com.zoho.crm.api.initializer as Init

            file_name = Init.Initializer.get_initializer().user.email

            file_name = file_name.split("@", 1)[0] + Init.Initializer.get_initializer().environment.url

            input_bytes = file_name.encode("UTF-8")
            #
            # zobj = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
            #
            # zdata = zobj.compress(input_bytes)
            #
            # zdata += zobj.flush()

            encode_string = base64.b64encode(input_bytes)

            # encode_string = re.sub('[^a-zA-Z0-9]', '', str(encode_string))

            encode_string = str(encode_string.decode("UTF-8"))

            record_field_details_path = "/Users/raja-7453/Documents/AutomateSDK/python/GitLab/zohocrm-python-sdk/src/" + encode_string + ".json"

            return record_field_details_path
else:

    from abc import ABCMeta, abstractmethod

    class Converter:

        __metaclass__ = ABCMeta

        @abstractmethod
        def get_response(self, response_json, class_path):

            pass

        @abstractmethod
        def form_request(self, request_instance, class_path, instance_no):

            pass

        @abstractmethod
        def get_wrapped_response(self, response, status_code):

            pass

        def value_checker(self, class_name, member_name, key_details, value, unique_values_map, instance_number):

            from src.com.zoho.api.exception import SDKException

            from .constants import Constants

            error = {}

            # Data Type Validation
            if not isinstance(value, Constants.TYPE_VS_DATATYPE.get(key_details['type'])):

                error['index'] = instance_number

                error['class_name'] = class_name

                error['member_name'] = key_details['name']

                error['accepted_type'] = key_details['type']

                raise SDKException("TYPE ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('values'):

                if value not in key_details['values']:

                    error['index'] = instance_number

                    error['class'] = class_name

                    error['field'] = member_name

                    error['accepted_values'] = key_details['values']

                    raise SDKException("UNACCEPTED VALUES ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('min-length'):

                if len(str(value)) < key_details['min-length']:

                    error['index'] = instance_number

                    error['class'] = class_name

                    error['field'] = member_name

                    error['minimum_length'] = key_details['min-length']

                    raise SDKException("MIN-LENGTH ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('max-length'):

                if len(str(value)) > key_details['max-length']:

                    error['index'] = instance_number

                    error['class'] = class_name

                    error['field'] = member_name

                    error['maximum_length'] = key_details['max-length']

                    raise SDKException("MAX-LENGTH ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('regex'):

                if re.search(value, key_details['regex']) is None:

                    error['index'] = instance_number

                    error['class'] = class_name

                    error['field'] = member_name

                    raise SDKException("REGEX MISMATCH ERROR", None, details=error, cause=traceback.format_stack(limit=6))

            if key_details.__contains__('unique'):

                if key_details['unique']:

                    if key_details['name'] not in unique_values_map:

                        unique_values_map[key_details['name']] = []

                    if value in unique_values_map[key_details['name']]:

                        error['first-index'] = unique_values_map[key_details['name']].index(value) + 1

                        error['next-index'] = instance_number

                        error['class'] = class_name

                        error['field'] = member_name

                        raise SDKException("UNIQUE KEY ERROR", None, details=error, cause=traceback.format_stack(limit=6))

                    unique_values_map[key_details['name']].append(value)

            return True

        def get_record_json_file_path(self):

            import src.com.zoho.crm.api.initializer as Init

            file_name = Init.Initializer.get_initializer().user.email

            file_name = file_name.split("@", 1)[0] + Init.Initializer.get_initializer().environment.url

            input_bytes = file_name.encode("UTF-8")

            encode_string = base64.b64encode(input_bytes)

            encode_string = str(encode_string.decode("UTF-8"))

            record_field_details_path = "/Users/raja-7453/Documents/AutomateSDK/python/GitLab/zohocrm-python-sdk/src/" + encode_string + ".json"

            return record_field_details_path
