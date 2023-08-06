from ..util import Model


class ResponseWrapper(Model):
	def __init__(self):
		self.__modules = None
		self.__key_modified = dict()

	def get_modules(self):
		return self.__modules

	def set_modules(self, modules):
		self.__modules = modules
		self.__key_modified["modules"] = 1

	def is_key_modified(self, key):
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		self.__key_modified[key] = modification
