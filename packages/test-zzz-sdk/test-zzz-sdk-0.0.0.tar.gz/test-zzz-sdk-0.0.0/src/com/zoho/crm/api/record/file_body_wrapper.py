
from ..util import Model


class FileBodyWrapper(Model):
	def __init__(self):
		self.__file = None
		self.__key_modified = dict()

	def get_file(self):
		return self.__file

	def set_file(self, file):
		self.__file = file
		self.__key_modified["file"] = 1

	def is_key_modified(self, key):
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		self.__key_modified[key] = modification
