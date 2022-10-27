from pandas_ods_reader import read_ods
import json

def get_data_from_ods(ods_path):
    data = read_ods(ods_path, 1, headers=True)
    data.index = data.index + 1
    return data

def get_data_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data
