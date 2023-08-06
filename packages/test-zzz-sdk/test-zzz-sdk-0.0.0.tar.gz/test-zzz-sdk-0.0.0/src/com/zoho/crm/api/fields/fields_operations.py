from ..util import APIResponse
from ..util import CommonAPIHandler

class FieldsOperations(object):
	def __init__(self,module_api_name):
		self.__module_api_name = module_api_name


	def get_fields(self):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/fields"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.add_param("module", self.__module_api_name)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def get_field(self, id):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/fields/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.add_param("module", self.__module_api_name)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")
