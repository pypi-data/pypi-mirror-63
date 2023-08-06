import os


class StreamWrapper(object):

    def __init__(self, file_path, name=None, stream=None):

        if file_path is not None:
            self.name = os.path.basename(file_path)
            self.stream = open(file_path, 'rb')
        else:
            self.name = name
            self.stream = stream

    def get_name(self):
        return self.name

    def get_stream(self):
        return self.stream
