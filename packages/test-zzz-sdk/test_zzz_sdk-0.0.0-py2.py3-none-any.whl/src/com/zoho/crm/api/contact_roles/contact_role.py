from ..util import Model


class ContactRole(Model):
	def __init__(self):
		self.__id = None
		self.__name = None
		self.__sequence_number = None
		self.__key_modified = dict()

	def get_id(self):
		return self.__id

	def set_id(self, id):
		self.__id = id
		self.__key_modified["id"] = 1

	def get_name(self):
		return self.__name

	def set_name(self, name):
		self.__name = name
		self.__key_modified["name"] = 1

	def get_sequence_number(self):
		return self.__sequence_number

	def set_sequence_number(self, sequence_number):
		self.__sequence_number = sequence_number
		self.__key_modified["sequence_number"] = 1

	def is_key_modified(self, key):
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		self.__key_modified[key] = modification
