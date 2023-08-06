class ParameterMap(object):
    def __init__(self):
        self.parameter_dict = dict()

    def add(self,param_instance,value):
        name = param_instance.name
        value_list = []
        if not self.parameter_dict.__contains__(name):
            value_list.append(value)
            self.parameter_dict[name] =value_list
        else:
            value_list = self.parameter_dict[name]
            value_list.append(value)
            self.parameter_dict[name] = value_list
