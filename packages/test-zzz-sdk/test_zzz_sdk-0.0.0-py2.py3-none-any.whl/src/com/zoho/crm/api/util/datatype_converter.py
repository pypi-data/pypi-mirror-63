from datetime import datetime
from dateutil.tz import tz

class DataTypeConverter(object):

    pre_converter_map = {}
    post_converter_map = {}

    @staticmethod
    def init():
        if len(DataTypeConverter.pre_converter_map) != 0 and len(DataTypeConverter.post_converter_map) != 0:
            return
        DataTypeConverter.add_to_map("String", lambda obj: str(obj), lambda obj: str(obj))
        DataTypeConverter.add_to_map("Integer", lambda obj: int(obj), lambda obj: int(obj))
        DataTypeConverter.add_to_map("Long", lambda obj: str(obj), lambda obj: str(obj))
        DataTypeConverter.add_to_map("Boolean", lambda obj: bool(obj), lambda obj: bool(obj))
        DataTypeConverter.add_to_map("DateTime", lambda obj: datetime.fromisoformat(obj).astimezone(tz.tzlocal()), lambda obj: obj.isoformat())

    @staticmethod
    def add_to_map(name, pre_converter, post_converter):
        DataTypeConverter.pre_converter_map[name] = pre_converter
        DataTypeConverter.post_converter_map[name] = post_converter

    @staticmethod
    def pre_convert(obj, type_name):
        DataTypeConverter.init()
        return DataTypeConverter.pre_converter_map[type_name](obj)

    @staticmethod
    def post_convert(obj, type_name):
        DataTypeConverter.init()
        return DataTypeConverter.post_converter_map[type_name](obj)

