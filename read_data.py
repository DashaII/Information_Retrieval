import json


def read_from_json(file_name):
    with open(file_name, 'r',  encoding="utf-8") as f:
        data_dict = json.load(f)
    return data_dict


def get_docs(file_path):
    return read_from_json(file_path)


def get_topics(file_path):
    return read_from_json(file_path)


