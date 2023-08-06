try:
    from .converter import Converter
    import importlib
    import logging
    import re
    import traceback
    import json

except Exception:
    import importlib
    import traceback
    from .converter import Converter
    import logging
    import re


class XMLConverter(Converter):

    logger = logging.getLogger('client_lib')

    def __init__(self, common_api_handler):

        self.unique_dict = {}

        self.count = 0

        self.common_api_handler = common_api_handler

    def form_request(self, request_instance, class_path, instance_no):

        return None

    def append_to_request(self, request_base, request_object):

        return None

    def get_wrapped_response(self, response, class_name):

        return None

    def get_response(self, response, class_path):

        return None
