class APIResponse(object):

    def __init__(self, headers, status_code, data_object):

        self.headers = headers

        self.status_code = status_code

        self.data_object = data_object

    def get_headers(self):

        return self.headers

    def get_status_code(self):

        return self.status_code

    def get_data_object(self):

        return self.data_object
