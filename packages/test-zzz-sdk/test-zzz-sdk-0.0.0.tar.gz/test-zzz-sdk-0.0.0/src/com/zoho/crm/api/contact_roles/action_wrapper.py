from ..util import Model


class ActionWrapper(Model):
	def __init__(self):
		self.__contact_roles = None
		self.__key_modified = dict()

	def get_contact_roles(self):
		return self.__contact_roles

	def set_contact_roles(self, contact_roles):
		self.__contact_roles = contact_roles
		self.__key_modified["contact_roles"] = 1

	def is_key_modified(self, key):
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		self.__key_modified[key] = modification
