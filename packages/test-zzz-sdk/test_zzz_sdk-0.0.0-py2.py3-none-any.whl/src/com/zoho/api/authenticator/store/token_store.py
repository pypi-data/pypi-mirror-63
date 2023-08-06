try:
    from abc import ABC, abstractmethod
    import sys
except Exception as e:
    from abc import ABCMeta, abstractmethod
    import sys

if sys.version > '3':
    class TokenStore(ABC):
        @abstractmethod
        def get_token(self, user, token):
            pass

        @abstractmethod
        def save_token(self, user, token):
            pass

        @abstractmethod
        def delete_token(self, user, token):
            pass
else:
    class TokenStore:
        __metaclass__ = ABCMeta

        @abstractmethod
        def get_token(self, user, token):
            pass

        @abstractmethod
        def save_token(self, user, token):
            pass

        @abstractmethod
        def delete_token(self, user, token):
            pass
