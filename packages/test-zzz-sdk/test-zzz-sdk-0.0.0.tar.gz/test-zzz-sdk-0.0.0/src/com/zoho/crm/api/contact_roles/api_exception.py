from ..util import Model

from .action_response import ActionResponse

class APIException(Model, ActionResponse):
	def __init__(self):
		self.__status = None
		self.__code = None
		self.__message = None
		self.__details = None
		self.__key_modified = dict()

	def get_status(self):
		return self.__status

	def set_status(self, status):
		self.__status = status
		self.__key_modified["status"] = 1

	def get_code(self):
		return self.__code

	def set_code(self, code):
		self.__code = code
		self.__key_modified["code"] = 1

	def get_message(self):
		return self.__message

	def set_message(self, message):
		self.__message = message
		self.__key_modified["message"] = 1

	def get_details(self):
		return self.__details

	def set_details(self, details):
		self.__details = details
		self.__key_modified["details"] = 1

	def is_key_modified(self, key):
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		self.__key_modified[key] = modification
