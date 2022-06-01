#!/usr/bin/python3
import configparser
import json
from typing import Dict, List


def read_config(file_path):
    dictionary = dict()
    dict_list = list()
    config = configparser.ConfigParser()
    config.read(file_path)
    for section in config.sections():
        for key in config[section]:
            dictionary[key] = config[section][key]
    return (dictionary)


print(read_config("db_conn.config.example"))


def main():
    pass


if __name__ == '__main__':
    main()
