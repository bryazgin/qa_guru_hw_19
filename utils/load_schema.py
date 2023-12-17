import json
import os


def load_schema(filepath):
    with open(os.path.dirname(os.path.dirname(__file__)) + '/json_schemas/' + filepath) as file:
        schema = json.load(file)
        return schema
