try:

    from .converter import Converter
    from .datatype_converter import DataTypeConverter
    from src.com.zoho.api.exception.sdk_exception import SDKException
    import src.com.zoho.crm.api.initializer as Init
    from src.com.zoho.crm.api.util.utility import Utility
    import importlib
    import logging
    import re
    import traceback
    import json

except Exception:

    import importlib
    import traceback
    from .converter import Converter
    from .datatype_converter import DataTypeConverter
    from src.com.zoho.api.exception import SDKException
    import src.com.zoho.crm.api.initializer as Init
    from src.com.zoho.crm.api.util.utility import Utility
    import logging
    import re


class JSONConverter(Converter):

    logger = logging.getLogger('client_lib')

    def __init__(self, common_api_handler):

        self.unique_dict = {}

        self.count = 0

        self.common_api_handler = common_api_handler

    def module_to_class(self, module_name):

        class_name = module_name

        if "_" in module_name:

            class_name = ''

            module_split = str(module_name).split('_')

            for each_name in module_split:

                each_name = each_name.capitalize()

                class_name += each_name

        return class_name

    def form_request(self, request_instance, class_path, instance_no):
        class_path = str(class_path).replace("src.", "")
        path_split = str(class_path).rpartition(".")
        class_name = self.module_to_class(path_split[-1])
        class_path = path_split[0] + "." + class_name
        try:
            from ..initializer import Initializer
        except Exception:
            from ..initializer import Initializer
        class_json_details = dict(Initializer.json_details[str(class_path)])
        request_dict = dict()

        if class_json_details.keys().__contains__('interface') and class_json_details['interface'] is not None:
            request_class_path = request_instance.__class__.__module__
            request_class_path = str(request_class_path).replace("src.", "")
            path_split = str(request_class_path).rpartition(".")
            request_class_name = self.module_to_class(path_split[-1])
            request_class_path = path_split[0] + "." + request_class_name
            classes = class_json_details['classes']
            for class_name_interface in classes:
                class_name_interface_lower = str(class_name_interface).lower()
                request_class_path_lower = request_class_path.lower()
                if class_name_interface_lower == request_class_path_lower:
                    class_json_details = dict(Initializer.json_details[str(class_name_interface)])
                    break

        try:
            for member_name in class_json_details:
                member_json_details = class_json_details[member_name]
                if member_json_details.__contains__('read-only') or not member_json_details.__contains__('name'):
                    continue

                modified = getattr(request_instance, 'is_key_modified')(member_name)
                if modified is None and member_json_details.__contains__('required'):
                    error = {
                        'index': instance_no,
                        'class': class_name,
                        'field': member_name
                    }
                    raise SDKException("REQUIRED FIELD ERROR", None, details=error, cause=traceback.format_stack(limit=6))

                member_data = getattr(request_instance,self.construct_private_member(class_name=class_name, member_name=member_name))

                if modified is not None and self.value_checker(class_name=class_name,member_name=member_name,key_details=member_json_details,value=member_data,unique_values_map=self.unique_dict, instance_number=instance_no) == True:
                    getattr(request_instance, 'set_key_modified')(0, member_name)
                    key_name = member_json_details.get('name')
                    type = member_json_details.get('type')
                    if type == 'List':
                        request_dict[key_name] = self.set_json_array(member_data,member_json_details)
                    elif type == 'Map' or type == 'HashMap':
                        request_dict[key_name] = self.set_json_object(member_data,member_json_details)
                    elif member_json_details.__contains__('structure_name'):
                        request_dict[key_name] = self.form_request(member_data, member_json_details.get('structure_name'), 1)
                    else:
                        request_dict[key_name] = DataTypeConverter.post_convert(member_data, type)

            if class_path.__eq__('com.zoho.crm.api.record.Record'):

                record_field_details_path = self.get_record_json_file_path()

                with open(record_field_details_path, mode='r') as JSON:
                    record_json_details = json.load(JSON)[self.common_api_handler.module_api_name]
                keyValues = getattr(request_instance,self.construct_private_member(class_name=class_name, member_name="key_values"))
                for keyname,key_json_detail in record_json_details.items():
                    if keyValues.__contains__(keyname):
                        keyvalue = None
                        if key_json_detail.__contains__("structure_name"):
                            keyvalue = self.form_request(keyValues[keyname],key_json_detail["structure_name"], 1)
                        else:
                            keyvalue = self.redirector_for_object_to_json(keyValues[keyname])
                        request_dict[keyname] = keyvalue
            return request_dict
        except SDKException as e:
            JSONConverter.logger.error("invalid data_type While converting to JSON" + e.__str__())
            raise

    def append_to_request(self, request_base, request_object):

        return json.dumps(request_object)

    def set_json_object(self, member_data, member_json_details):
        json_object = {}
        if member_json_details is None:
            for key, value in member_data.items():
                json_object[key] = self.redirector_for_object_to_json(value)
        else:
            keys_detail = member_json_details["keys"]
            for key_detail in keys_detail:
                key_value = None
                key_name = key_detail["name"]
                if member_data.__contains__(key_name) and member_data[key_name] is not None:
                    if key_detail.__contains__("structure_name"):
                        key_value = self.form_request(member_data[key_name], key_detail["structure_name"], 1)
                    else:
                        key_value = self.redirector_for_object_to_json(member_data[key_name])

                    json_object[key_name] = key_value
        return json_object

    def set_json_array(self, member_data, member_json_details):
        json_array = []
        if member_json_details is None:
            for value in member_data:
                json_array.append(self.redirector_for_object_to_json(value))
        else:
            if member_json_details.__contains__("structure_name"):
                instance_no = 1
                package = member_json_details["structure_name"]
                for data in member_data:
                    json_array.append(self.form_request(data, package, instance_no))
                    instance_no += 1
            else:
                for data in member_data:
                    json_array.append(self.redirector_for_object_to_json(data))

        return json_array

    def redirector_for_object_to_json(self, member_data):

        if isinstance(member_data, dict):

            return self.set_json_object(member_data, None)

        elif isinstance(member_data, list):

            return self.set_json_array(member_data, None)

        else:

            return member_data

    def get_wrapped_response(self, response, class_name):

        try:
            return self.get_response(response.json(), class_name)

        except ValueError:

            return None

        return None

    def get_response(self, response, class_path):

        try:
            from ..initializer import Initializer

        except Exception:

            from ..initializer import Initializer

        if response is None:

            return None

        response_json = dict(response)

        path_split = str(class_path).rpartition(".")

        class_name = self.module_to_class(path_split[-1])

        class_path = path_split[0] + "." + class_name

        class_json_details = dict(Initializer.json_details[str(class_path)])

        instance = None

        if class_json_details.keys().__contains__("interface") and class_json_details["interface"] is not None:

            classes = class_json_details["classes"]

            instance = self.find_match(classes, response_json)

        else:

            imported_module = importlib.import_module(path_split[0])

            class_holder = getattr(imported_module, class_name)

            instance = class_holder()

            for member_name, member_json_details in class_json_details.items():

                key_name = member_json_details['name'] if 'name' in member_json_details else None

                if key_name is not None and response_json.__contains__(key_name) and response_json.get(key_name) is not None:

                    key_data = response_json.get(key_name)

                    type = member_json_details["type"]

                    instance_value = None

                    if type == "List":

                        instance_value = []

                        instance_value = self.get_collections_data(key_data, member_json_details)

                    elif type == "Map":

                        instance_value = {}

                        instance_value = self.get_map_data(key_data, member_json_details)

                    elif member_json_details.__contains__("structure_name"):

                        instance_value = self.get_response(key_data, member_json_details["structure_name"])

                    else:

                        instance_value = DataTypeConverter.pre_convert(key_data, type)

                    setattr(instance, self.construct_private_member(class_name=class_name, member_name=member_name), instance_value)

            if class_path.__eq__('com.zoho.crm.api.record.Record'):

                record_field_details_path = self.get_record_json_file_path()

                record_json_details = dict(Initializer.json_details[class_path])

                with open(record_field_details_path, mode='r') as JSON:

                    module_json_details = None
                    if self.common_api_handler.module_api_name is not None:
                        module_json_details = json.load(JSON)[self.common_api_handler.module_api_name]

                instance_value = {}

                if module_json_details is not None:

                    for key_name, key_json_detail in module_json_details.items():

                        field_name = key_name.lower()

                        if not record_json_details.__contains__(field_name):

                            if response_json.__contains__(key_name):

                                key_value = None

                                if key_json_detail.__contains__("structure_name"):

                                    key_value = self.get_response(response_json[key_name], key_json_detail["structure_name"])

                                else:

                                    key_value = self.redirector(response_json[key_name])

                                instance_value[key_name] = key_value
                else:

                    for json_key_name, key_value in response_json.items():

                        key_name = json_key_name.lower()

                        if not record_json_details.__contains__(key_name):

                            instance_value[key_name] = key_value

                setattr(instance, self.construct_private_member(class_name=class_name, member_name="key_values"), instance_value)

        return instance

    def get_map_data(self, key_data, member_json_details):
        map_instance = {}
        responses = key_data
        if member_json_details is None:
            for key, response in responses.items():
                map_instance[key] = response
        else:
            keys_detail = member_json_details["keys"]
            for key_detail in keys_detail:
                key_value = None
                key_name = key_detail["name"]
                if responses.__contains__(key_name) and responses[key_name] != None:
                    if key_detail.__contains__("structure_name"):
                        key_value = self.get_response(responses[key_name], key_detail["structure_name"])
                        map_instance[key_name] = key_value
                    else:
                        key_value = responses[key_name]
                        map_instance[key_name] = self.redirector(key_value)

        return map_instance

    def get_collections_data(self, key_data, member_json_details):
        values = []
        responses = key_data
        if member_json_details is None:
            for response in responses:
                values.append(self.redirector(response))
        else:
            if member_json_details.__contains__("structure_name"):
                package = member_json_details["structure_name"]
                for response in responses:
                    values.append(self.get_response(response, package))
            else:
                for response in responses:
                    values.append(self.redirector(response))
        return values

    def find_match(self, classes, response_json):
        package = ""
        ratio = 0
        for class_name in classes:
            match_ratio = self.find_ratio(class_name, response_json)
            if match_ratio == 1.0:
                package = class_name
                ratio = 1
                break
            elif match_ratio > ratio:
                ratio = match_ratio
                package = class_name
        return self.get_response(response_json, package)

    def find_ratio(self, class_name, response_json):
        try:
            from ..initializer import Initializer
        except Exception:
            from ..initializer import Initializer
        class_json_details = dict(Initializer.json_details[str(class_name)])
        total_points = len(class_json_details.keys())
        matches = 0
        if total_points == 0:
            return
        else:
            for member_name in class_json_details:
                member_json_details = class_json_details[member_name]
                key_name = member_json_details["name"] if 'name' in member_json_details else None
                if key_name is not None and response_json.__contains__(key_name) and response_json.get(key_name) is not None:
                    key_data = response_json[key_name]
                    key_data_type = type(key_data).__name__
                    if isinstance(key_data, int):
                        key_data_type = "Integer"
                    if isinstance(key_data, bool):
                        key_data_type = "Boolean"
                    if isinstance(key_data, str):
                        key_data_type = "String"
                    if isinstance(key_data, dict):
                        key_data_type = "Map"
                    if isinstance(key_data, list):
                        key_data_type = "List"
                    if key_data_type == member_json_details["type"]:
                        if member_json_details.__contains__("values"):
                            for value in member_json_details["values"]:
                                if value == key_data:
                                    matches += 1
                                    break
                        else:
                            matches += 1

        return matches / total_points

    def redirector(self, key_data):
        if isinstance(key_data, dict):

            return self.get_map_data(key_data, None)

        elif isinstance(key_data, list):

            return self.get_collections_data(key_data, None)

        else:

            return key_data

    def construct_private_member(self, class_name, member_name):

        return '_' + class_name + '__' + member_name
