class HeaderMap(object):
    def __init__(self):
        self.header_dict = dict()

    def add(self,header_inst,value):
        name = header_inst.name
        value_list = []
        if not self.header_dict.__contains__(name):
            value_list.append(value)
            self.header_dict[name] = value_list
        else:
            value_list = self.header_dict[name]
            value_list.append(value)
            self.header_dict[name] = value_list