from ..util import Model


class Field(Model):
	def __init__(self):
		self.__id = None
		self.__api_name = None
		self.__data_type = None
		self.__key_modified = dict()

	def get_id(self):
		return self.__id

	def set_id(self, id):
		self.__id = id
		self.__key_modified["id"] = 1

	def get_api_name(self):
		return self.__api_name

	def set_api_name(self, api_name):
		self.__api_name = api_name
		self.__key_modified["api_name"] = 1

	def get_data_type(self):
		return self.__data_type

	def set_data_type(self, data_type):
		self.__data_type = data_type
		self.__key_modified["data_type"] = 1

	def is_key_modified(self, key):
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		self.__key_modified[key] = modification
