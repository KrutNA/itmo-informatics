#!/usr/bin/env python3
from json_lib.parser import Parser as JsonParser
from yaml_lib import YamlObject

if __name__ == "__main__":
    file = "schedule.json"
    result = None
    with open(file, "r") as f:
        result = f.read()

    json = JsonParser(result).parse()

    yaml = YamlObject.from_normal(json.to_normal())

    print(yaml.to_string())
