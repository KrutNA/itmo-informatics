from enum import Enum, auto


class YamlObject:
    """
    Class which represents YamlObject with form of object, not normalized
    """
    def __init__(self, data):
        self._data = data

    # def from_string(self, string):
    #     """Converts string to YamlObject
    #     Gets: string
    #     Returns: YamlObject
    #     """
    #     return yaml_object

    def to_string(self, tabs=0):
        """Converts YamlObject to string
        Gets: self
        Returns: string
        """
        return self._data.to_string(tabs)

    def to_normal(self):
        """Converts YamlObject to normal python object
        Gets: YamlObject
        Returns: normal value
        """
        return self._data.normalized()

    def from_normal(normal):
        """Converts normal python object to YamlObject
        Gets: normal value
        Returns: YamlObject
        """
        return YamlObject(Data.from_normal(normal))


class Data:
    def __init__(self, data_type, data):
        self._data, self._data_type = data, data_type

    def get_name(self):
        return self._name

    def normalized(self):
        if self._data_type == DataType.NULL:
            return None
        elif self._data_type == DataType.BOOL:
            return bool(self._data)
        elif self._data_type == DataType.INT_8:
            return oct(self._data)
        elif self._data_type == DataType.INT_10:
            return int(self._data)
        elif self._data_type == DataType.INT_16:
            return int(self._data, 16)
        elif self._data_type == DataType.FLOAT:
            return float(self._data)
        elif self._data_type == DataType.STR:
            return str(self._data)
        elif self._data_type == DataType.SEQ:
            return [val.normalized() for val in self._data]
        elif self._data_type == DataType.MAP:
            return dict((key, val.normalized())
                        for (key, val) in self._data.items())

    def from_normal(obj):
        data_type = DataType.to_type(obj)
        data = obj
        if data_type == DataType.SEQ:
            data = [Data.from_normal(val) for val in obj]
        elif data_type == DataType.MAP:
            data = dict((key, Data.from_normal(val))
                        for (key, val) in obj.items())
        return Data(data_type, data)

    def to_string(self, tabs=0):
        def pre(tabs):
            return "  " * tabs

        if ((self._data_type == DataType.SEQ or
             self._data_type == DataType.MAP) and len(self._data) == 0):
            return "[]" if self._data_type == DataType.SEQ else "{}"
        elif self._data_type == DataType.SEQ:
            return '\n' + '\n'.join(["{}- {}".format(pre(tabs),
                                                     val.to_string(tabs + 1))
                                     for val in self._data])
        elif self._data_type == DataType.MAP:
                return '\n{}'.format(pre(tabs)).join(
                    ["{}: {}".format(key, val.to_string(tabs + 1))
                     for (key, val) in self._data.items()])
        elif self._data_type == DataType.NULL:
            return "Null"
        elif self._data_type == DataType.STR:
            if len(self._data.split('\n')) > 1:
                return "|\n" + '\n'.join(pre(tabs + 1) + val
                                         for val in self._data.split('\n'))
            else:
                return self._data
        elif self._data_type == DataType.INT_8:
            return str(oct(self._data))
        elif self._data_type == DataType.INT_16:
            return str(hex(self._data))
        else:
            return str(self._data)


class DataType(Enum):
    NULL = auto()
    BOOL = auto()
    INT_10 = auto()
    INT_8 = auto()
    INT_16 = auto()
    FLOAT = auto()
    STR = auto()
    SEQ = auto()
    MAP = auto()

    def is_hex(s):
        try:
            int(s, 16)
            return True
        except ValueError:
            return False

    def to_type(value):
        data_type = DataType.NULL
        if isinstance(value, bool):
            data_type = DataType.BOOL
        elif isinstance(value, int):
            data_type = DataType.INT_10
        elif isinstance(value, float):
            data_type = DataType.FLOAT
        elif isinstance(value, str):
            data_type = DataType.STR
        elif isinstance(value, type([])):
            data_type = DataType.SEQ
        elif isinstance(value, type({})):
            data_type = DataType.MAP
        return data_type


if __name__ == "__main__":
    print("<<<<BEGIN TESTING 'yaml_lib' MODULE>>>>")
    a = {"int": 666,
         "float": 666.777,
         "string": "String",
         "array": ["String", 0o666, {"1": True, "2": [0x666, 0o777]}],
         "empty seq": [],
         "empty map": {}}
    print("<<INPUT>>")
    print(a)
    yaml = YamlObject.from_normal(a)
    print("\n<<PRINTING YamlObject TO_STRING>>")
    print(yaml.to_string())
    print("\n<<PRINTING YamlObject NORMALIZED>>")
    print(yaml.to_normal())
    print("\n<<<<END TESTING 'json_lib' MODULE>>>>")
