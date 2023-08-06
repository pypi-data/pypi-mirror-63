from ..util import Model


class ResponseWrapper(Model):
	def __init__(self):
		self.__fields = None
		self.__key_modified = dict()

	def get_fields(self):
		return self.__fields

	def set_fields(self, fields):
		self.__fields = fields
		self.__key_modified["fields"] = 1

	def is_key_modified(self, key):
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		self.__key_modified[key] = modification
