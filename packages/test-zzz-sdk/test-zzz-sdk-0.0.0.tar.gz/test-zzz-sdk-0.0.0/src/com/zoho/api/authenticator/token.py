try:
    from abc import abstractmethod, ABC
    import sys
except Exception as e:
    from abc import ABCMeta, abstractmethod
    import sys

if sys.version_info[0] < 3:
    class Token:
        __metaclass__ = ABCMeta

        @abstractmethod
        def authenticate(self, urlconnection):
            pass

else:
    class Token(ABC):
        @abstractmethod
        def authenticate(self, urlconnection):
            pass
