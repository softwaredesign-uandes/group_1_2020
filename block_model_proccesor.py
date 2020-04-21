from tabulate import tabulate
import sqlite3
import json

from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME

def get_model_data_table(model_name, from_id, to_id):
    data_table = []
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * FROM {} WHERE ID >= {} AND ID <= {}".format(model_name, from_id, to_id))
    for row in cursor:
        data_table.append(list(row))
    return data_table

def get_headers_tabulated_table(model_name):
    model_information_json = get_models_information_json()
    separator_lines = []
    for column in model_information_json[model_name]:
        separator_lines.append("_" * len(column))
    return [model_information_json[model_name], separator_lines]

def check_if_model_exists_in_json(model_name):
    model_information_json = get_models_information_json()
    try:
        info = model_information_json[model_name]
        return True
    except:
        return False

def get_models_information_json():
    with open(LOADED_MODELS_INFORMATION_FILE_NAME) as json_file:
        model_information_json = json.load(json_file)
    return model_information_json

def get_tabulated_blocks(model_name, from_id, to_id):
    if check_if_model_exists_in_json(model_name):
        table = get_headers_tabulated_table(model_name)
        table.extend(get_model_data_table(model_name, from_id, to_id))
        return tabulate(table)
    return False

def get_mass_in_kilograms(model_name, x, y, z, mass_column_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT {} FROM {} WHERE x = {} AND y = {} AND z = {}".format(mass_column_name, model_name, x, y, z))
    mass_in_tons = cursor.fetchone()
    if mass_in_tons is not None:
        return mass_in_tons[0] * 1000
    return False

def get_available_models():
    models = get_models_information_json()
    models_names = models.keys()
    return list(models_names)
