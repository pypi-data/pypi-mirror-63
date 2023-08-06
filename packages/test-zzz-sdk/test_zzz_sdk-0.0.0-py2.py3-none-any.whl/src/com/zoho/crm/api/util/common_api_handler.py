try:

    from .api_http_connector import APIHTTPConnector
    from .json_converter import JSONConverter
    from .xml_converter import XMLConverter
    from .form_data_converter import FormDataConverter
    from .downloader import Downloader
    from .constants import Constants
    import json
    import platform
    from .api_response import APIResponse

except Exception:

    from .api_http_connector import APIHTTPConnector
    from .json_converter import JSONConverter
    from .constants import Constants
    import json
    import platform
    from .api_response import APIResponse


class CommonAPIHandler(object):

    def __init__(self):

        self.api_path = None

        self.header = {}

        self.param = {}

        self.request = None

        self.http_method = None

        self.response = None

        self.module_api_name = None

        self.content_type = None

    def add_param(self, param_name, param_value):

        self.param[param_name] = param_value

    def add_header(self, header_name, header_value):

        self.header[header_name] = header_value

    def api_call(self, class_name, encode_type):

        import src.com.zoho.crm.api.initializer as Init

        connector = APIHTTPConnector()

        connector.url = Init.Initializer.get_initializer().environment.url + self.api_path

        connector.headers = self.header

        connector.req_method = self.http_method

        connector.params = self.param

        convert_instance = None

        if self.http_method == 'POST' or self.http_method == 'PUT':

            convert_instance = self.get_converter_class_instance(self.content_type)

            request = convert_instance.form_request(self.request, self.request.__class__.__module__, 1)

            connector.req_body = request

        Init.Initializer.get_initializer().token.authenticate(connector)

        connector.headers[Constants.ZOHO_SDK] = platform.system() + "/" + platform.release() + " python/" + platform.python_version() + ":" + Constants.SDK_VERSION

        response = connector.fire_request(convert_instance)

        status_code = response.status_code

        headers = response.headers

        content_type = response.headers['Content-Type']

        if ";" in content_type:

            content_type = content_type.rpartition(";")[0]

        convert_instance = self.get_converter_class_instance(content_type)

        class_name = str(class_name).replace("src.", "")

        return_object = convert_instance.get_wrapped_response(response, class_name)

        return APIResponse(headers, status_code, return_object)

    def get_converter_class_instance(self, encode_type):

        switcher = {

            "application/json": JSONConverter(self),

            "text/plain": JSONConverter(self),

            "application/xml": XMLConverter(self),

            "text/xml": XMLConverter(self),

            "multipart/form-data": FormDataConverter(self),

            "application/x-download": Downloader(self),

            "image/png": Downloader(self),

            "image/jpeg": Downloader(self),

            "application/zip": Downloader(self),

            "image/gif": Downloader(self),

            "text/csv": Downloader(self),

            "image/tiff": Downloader(self),
        }

        return switcher.get(encode_type, None)
