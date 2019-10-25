#!/usr/bin/env python3
from json_lib import JsonObject, parser as json_parser
from yaml_lib import YamlObject
from collections import deque

if __name__ == "__main__":
    init = {"int": 666,
            "float": 666.777,
            "string": "String",
            "array": ["String", 0o666, {"1": True, "2": [0x666, 0o777]}],
            "empty seq": [],
            "empty map": {}}
    txt = """{
  'int': 666.0,
  'float': 666.777,
  'string': "String",
  'array': [
    "String",
    438.0,
    {
      '1': true,
      '2': [
        1638.0,
        511.0
      ]
    }
  ],
  'empty seq': [],
  'empty map': {}
}w"""
    print(json_parser.Parser(txt).parse().to_string())
