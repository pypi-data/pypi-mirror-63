from ..util import Model


class BodyWrapper(Model):
	def __init__(self):
		self.__data = None
		self.__key_modified = dict()

	def get_data(self):
		return self.__data

	def set_data(self, data):
		self.__data = data
		self.__key_modified["data"] = 1

	def is_key_modified(self, key):
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		self.__key_modified[key] = modification
