import json_lib as jl
from collections import deque
import re


class Parser:
    def __init__(self, string):
        self._string = string
        self._stack = deque()
        self._result = None

    def str_to_bool(value):
        return True if value == "true" else False

    def parse(self):
        while not self._result:
            self._parse_data()
            self._string = self._string[len(self._match.group(0)):]
        if self._string.strip().rstrip() != "":
            raise ValueError
        return jl.JsonObject(self._result)

    def _parse_data(self):
        """Parses string and founds first Data
        Gets: self
        Returns: None
        Throws: Exception, if can't parse data
        """
        regex_begin = r"^\s*(?P<val>"
        regex_end = r")\s*"
        if len(self._stack) != 0:
            if self._stack[-1]._data_type == jl.DataType.OBJECT:
                self._head_type = jl.DataType.OBJECT
                regex_begin = "^{}{}{}{}{}".format(
                    r"\s*((",
                    r",\s*(" if len(self._stack[-1]._data) != 0 else "(",
                    r"?P<name>",
                    DataRegex.STRING,
                    r")\s*:\s*(?P<val>"
                )
                regex_end = r"))|(\}))\s*"
            elif self._stack[-1]._data_type == jl.DataType.ARRAY:
                self._head_type = jl.DataType.ARRAY
                regex_begin = "^{}{}{}".format(
                    r"\s*(",
                    r",\s*(" if len(self._stack[-1]._data) != 0 else "(",
                    r"?P<val>"
                )
                regex_end = r")|([\]]))\s*"
            else:
                self._head_type = None
        else:
            self._head_type = None

        any_matches = False
        for (data_type, data_regex) in DataRegex.get_all().items():
            if self._match_string(regex_begin, data_regex, regex_end):
                self._read_from_match(data_type)
                any_matches = True
                break
        if not any_matches:
            raise ValueError

    def _match_string(self, regex_begin, regex, regex_end):
        self._match = re.compile(
            "{}{}{}".format(regex_begin,
                            regex,
                            regex_end),
            re.DOTALL).search(self._string)
        return True if self._match else False

    def _read_from_match(self, data_type):
        def string_to_jsonobj(data_type):
            if data_type == jl.DataType.ARRAY:
                return jl.Data.from_normal([])
            elif data_type == jl.DataType.OBJECT:
                return jl.Data.from_normal({})
            elif data_type == jl.DataType.STRING:
                return jl.Data.from_normal(self._match.groupdict()['val'][1:-1])
            elif data_type == jl.DataType.NUMBER:
                return jl.Data.from_normal(
                    float(self._match.groupdict()['val']))
            elif data_type == jl.DataType.BOOLEAN:
                return jl.Data.from_normal(
                    Parser.str_to_bool(self._match.groupdict()['val']))
            elif data_type == jl.DataType.NULL:
                return jl.Data.from_normal(None)
        if self._match.groups()[-1] and (
                self._head_type == jl.DataType.OBJECT or
                self._head_type == jl.DataType.ARRAY):
            if len(self._stack) >= 2:
                if self._stack[-2]._data_type == jl.DataType.OBJECT:
                    name = self._stack[-1]._name[1:-1]
                    self._stack[-1]._data[name] = self._stack.pop()
                else:
                    self._stack[-2]._data.append(self._stack.pop())
            else:
                self._result = self._stack.pop()
        elif self._head_type == jl.DataType.OBJECT and (
                data_type in [jl.DataType.ARRAY, jl.DataType.OBJECT]):
            self._stack.append(string_to_jsonobj(data_type).with_name(
                self._match.groupdict()['name']))

        elif self._head_type == jl.DataType.OBJECT:
            self._stack[-1]._data[self._match.groupdict()['name'][1:-1]] = (
                string_to_jsonobj(data_type))

        elif self._head_type == jl.DataType.ARRAY and (
                data_type in [jl.DataType.ARRAY, jl.DataType.OBJECT]):
            self._stack.append(string_to_jsonobj(data_type))

        elif self._head_type == jl.DataType.ARRAY:
            self._stack[-1]._data.append(string_to_jsonobj(data_type))

        elif data_type == jl.DataType.ARRAY or data_type == jl.DataType.OBJECT:
            self._stack.append(string_to_jsonobj(data_type))

        else:
            self._result = string_to_jsonobj(data_type)


class DataRegex:
    NULL = r"null"
    BOOLEAN = r"(true)|(false)"
    NUMBER = r"-?\d+(.\d+([eE][-+]?\d+)?)?"
    STRING = (
        r"[\'\"](((\\([\"\\\/bfnrt])|(u[0-9A-Fa-f]{4}))|[^\'\"\\])*)([^\\][\'\"])")
    ARRAY = r"\["
    OBJECT = r"\{"

    def get_all():
        return {
            jl.DataType.ARRAY: DataRegex.ARRAY,
            jl.DataType.OBJECT: DataRegex.OBJECT,
            jl.DataType.STRING: DataRegex.STRING,
            jl.DataType.NUMBER: DataRegex.NUMBER,
            jl.DataType.BOOLEAN: DataRegex.BOOLEAN,
            jl.DataType.NULL: DataRegex.NULL
        }
