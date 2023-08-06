try:
    from abc import abstractmethod,  ABC
    import sys
except Exception as e:
    from abc import abstractmethod, ABCMeta
    import sys

if sys.version_info[0] < 3:
    class DataCenter:
        __metaclass__ = ABCMeta

        @abstractmethod
        def get_iamurl(self):
            pass

        class Environment(object):
            def __init__(self, url, accounts_url):
                self.url = url
                self.accounts_url = accounts_url
                return

else:
    class DataCenter(ABC):
        @abstractmethod
        def get_iamurl(self):
            pass

        class Environment(object):
            def __init__(self, url, accounts_url):
                self.url = url
                self.accounts_url = accounts_url
                return
