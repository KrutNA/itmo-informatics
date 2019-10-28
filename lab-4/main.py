#!/usr/bin/env python3
from json_lib.parser import Parser as JsonParser
from yaml_lib import YamlObject
import json
import oyaml as yaml
from time import process_time
from os import system


def parse(string):
    _json_lib = JsonParser(string).parse()
    return YamlObject.from_normal(_json_lib.to_normal())


def check_parse(string):
    print("""Проверка выполнения в цикле десериализации JSON
И сериализации полученного результата в YAML
С использованием написанных мною библиотек json_lib и yaml_lib""")
    _time = process_time()
    for i in range(100):
        parse(string)
    _time = process_time() - _time
    print("Выполнено за:", _time)


def parse_other(string):
    _json = json.loads(string)
    return yaml.dump(_json, default_flow_style=False)


def check_parse_oter(string):
    print("""Проверка выполнения в цикле десериализации JSON
И сериализации полученного результата в YAML
С использованием библиотек json и oyaml""")
    _time = process_time()
    for i in range(100):
        parse_other(string)
    _time = process_time() - _time
    print("Выполнено за:", _time)


if __name__ == "__main__":
    file = "schedule.json"
    string = None
    with open(file, "r") as f:
        string = f.read()

    check_parse(string)
    print()
    check_parse_oter(string)
    print()
    _yaml = parse_other(string)
    file = "schedule.other.yaml"
    with open(file, "w") as f:
        f.write(_yaml)

    _yaml_lib = parse(string)
    file = "schedule.yaml"
    with open(file, "w") as f:
        f.write(_yaml_lib.to_string())

    print(""""Вывод сравнения с помощью команды diff
(Если файлы идентичны, то ничего не выведется)""")
    system("diff schedule.yaml schedule.other.yaml")
    print("Окончание вывода сравнения")
