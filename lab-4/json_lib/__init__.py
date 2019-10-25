from enum import Enum, auto
from . import parser


class JsonObject:
    """
    Class which represents JsonObject with form of object, not normalized
    """
    def __init__(self, data):
        self._data = data

    def from_string(self, string):
        """Converts string to JsonObject
        Gets: string
        Returns: JsonObject
        """
        return parser.Parser(string).parse()

    def to_string(self, to_formated=False, tabs=1):
        """Converts JsonObject to string
        Gets: self
        Returns: string
        """
        return self._data.to_string(to_formated, tabs)

    def to_normal(self):
        """Converts JsonObject to normal python object
        Gets: JsonObject
        Returns: normal value
        """
        return self._data.normalized()

    def from_normal(normal):
        """Converts normal python object to jsonobject
        Gets: normal value
        Returns: JsonObject
        """
        return JsonObject(Data.from_normal(normal))


class Data:
    def __init__(self, data_type, data):
        self._data, self._data_type, self._name = data, data_type, None

    def with_name(self, name):
        self._name = name
        return self

    def get_name(self):
        return self._name

    def normalized(self):
        if self._data_type == DataType.NULL:
            return None
        if self._data_type == DataType.NUMBER:
            return float(self._data)
        elif self._data_type == DataType.STRING:
            return str(self._data)
        elif self._data_type == DataType.BOOLEAN:
            return bool(self._data)
        elif self._data_type == DataType.ARRAY:
            return [val.normalized() for val in self._data]
        elif self._data_type == DataType.OBJECT:
            return dict((key, val.normalized())
                        for (key, val) in self._data.items())

    def from_normal(obj):
        data_type = DataType.to_type(obj)
        data = obj
        if data_type == DataType.ARRAY:
            data = [Data.from_normal(val) for val in obj]
        elif data_type == DataType.OBJECT:
            data = dict((key, Data.from_normal(val))
                        for (key, val) in obj.items())
        return Data(data_type, data)

    def to_string(self, to_formated=False, tabs=1):
        def pre(tabs):
            return '' if not to_formated else ("  " * tabs)

        def format_obj(begin, end):
            return "{}{}{}".format(
                begin + ('' if not to_formated
                         else ('' if len(self._data) == 0
                               else ("\n" + pre(tabs)))),
                (',' + (' ' if not to_formated else ("\n" + pre(tabs)))).join(
                    [val.to_string(to_formated, tabs + 1)
                     for val in self._data]
                    if self._data_type == DataType.ARRAY
                    else ["'{}': {}".format(key, val.to_string(to_formated,
                                                               tabs + 1))
                          for (key, val) in self._data.items()]),
                ('' if not to_formated
                 else ('' if len(self._data) == 0
                       else ("\n" + pre(tabs - 1)))) + end)
        if self._data_type == DataType.ARRAY:
            return format_obj('[', ']')
        elif self._data_type == DataType.OBJECT:
            return format_obj('{', '}')
        elif self._data_type == DataType.NULL:
            return "null"
        elif self._data_type == DataType.STRING:
            return '"{}"'.format(self._data)
        elif self._data_type == DataType.BOOLEAN:
            return "true" if self._data else "false"
        else:
            return str(self._data)


class DataType(Enum):
    NULL = None
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    ARRAY = auto()
    OBJECT = auto()

    def to_type(value):
        data_type = DataType.NULL
        if isinstance(value, bool):
            data_type = DataType.BOOLEAN
        elif isinstance(value, int) or isinstance(value, float):
            data_type = DataType.NUMBER
        elif isinstance(value, str):
            data_type = DataType.STRING
        elif isinstance(value, type([])):
            data_type = DataType.ARRAY
        elif isinstance(value, type({})):
            data_type = DataType.OBJECT
        return data_type


if __name__ == "__main__":
    print("<<<<BEGIN TESTING 'json_lib' MODULE>>>>")
    a = {"int": 666,
         "float": 666.777,
         "string": "String",
         "array": ["String", 0o666, {"1": True, "2": [0x666, 0o777]}],
         "empty seq": [],
         "empty map": {}}
    print("<<INPUT>>")
    print(a)
    print("\n<<PRINTING JsonObject FORMATTED>>")
    print(JsonObject.from_normal(a).to_string(to_formated=True))
    print("\n<<PRINTING JsonObject PLAIN>>")
    print(JsonObject.from_normal(a).to_string())
    print("\n<<<<END TESTING 'json_lib' MODULE>>>>")
