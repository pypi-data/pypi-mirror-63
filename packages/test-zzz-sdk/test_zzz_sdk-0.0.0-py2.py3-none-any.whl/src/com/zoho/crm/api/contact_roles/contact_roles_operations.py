from ..header import Header
from ..header_map import HeaderMap
from ..util import APIResponse
from ..util import CommonAPIHandler

class ContactRolesOperations(object):
	def __init__(self,param):
		self.__param = param


	def get_contact_roles(self):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.add_param("param", self.__param)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def create_contact_roles(self, request, header_instance):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		handler_instance.header=header_instance
		handler_instance.add_param("param", self.__param)
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def update_contact_roles(self, request):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles"
		handler_instance.api_path=api_path
		handler_instance.http_method="PUT"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		handler_instance.add_param("param", self.__param)
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def get_contact_role(self, header_instance, id):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.header=header_instance
		handler_instance.add_param("param", self.__param)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def update_contact_role(self, request, id):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="PUT"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		handler_instance.add_param("param", self.__param)
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def delete_contact_role(self, id):
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="DELETE"
		handler_instance.add_param("param", self.__param)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")
class CreateContactRolesHeader(object):
	header = Header("header")



class GetContactRoleHeader(object):
	header = Header("header")


