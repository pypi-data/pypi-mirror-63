from ..util import APIResponse
from ..util import CommonAPIHandler
from ..util import Utility

class RecordOperations(object):
	def __init__(self,module_api_name):
		self.__module_api_name = module_api_name


	def get_record(self, id):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name=self.__module_api_name
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def download_attachment(self, id, attachment_id):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/Attachments/"
		api_path = api_path + attachment_id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		from .file_body_wrapper import FileBodyWrapper
		return handler_instance.api_call(FileBodyWrapper.__module__, "application/x-download")

	def get_attachments(self, id):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/Attachments"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def upload_attachments(self, request, id):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/Attachments"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.content_type="multipart/form-data"
		handler_instance.request=request
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def get_records(self):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name=self.__module_api_name
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def create_records(self, request):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name=self.__module_api_name
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")
