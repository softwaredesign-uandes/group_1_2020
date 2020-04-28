import os
import sqlite3
import json
from block import Block
from block_model import BlockModel
from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME, MINERAL_GRADES_INFORMATION_FILE_NAME


def create_db(db_name=DB_NAME):
    if os.path.isfile(db_name):
        os.remove(db_name)
    sqlite3.connect(db_name)


def get_model_name_from_path(block_model_file_path):
    if "\\" in block_model_file_path:
        separator = "\\"
    else:
        separator = "/"
    model_name = block_model_file_path.split(separator)[-1].split(".")[0]
    return model_name


def retrieve_columns_types(block_model_file_path):
    types = []
    with open(block_model_file_path, "r") as blocks:
        first_line = list(blocks)[0].strip().split(" ")[1:]
        for item in first_line:
            if item.isdigit():
                types.append("INT")
            elif item.replace("-", "").isdigit():
                types.append("INT")
            elif item.replace(".", "").replace(",", "").replace("-", "").isdigit():
                types.append("FLOAT")
            else:
                types.append("TEXT")
    return types


def parse_block_column_types(block):
    parsed_block = []
    for data in block:
        if data.isdigit():
            parsed_block.append(data.strip())
        elif data.replace("-", "").isdigit():
            parsed_block.append(data.strip())
        elif data.replace(".", "").replace(",", "").replace("-", "").isdigit():
            parsed_block.append(data.strip())
        else:
            parsed_block.append("\'{}\'".format(data.strip()))
    return parsed_block


def create_table_query(model_name, table_columns, columns_types):
    db_columns = ["{} INT PRIMARY KEY ".format(table_columns[0])]
    for column_name, column_type in zip(table_columns[1:], columns_types):
        db_columns.append("{} {} NOT NULL".format(column_name, column_type))
    query = "CREATE TABLE IF NOT EXISTS {}({});".format(model_name, ",".join(db_columns))
    return query


def load_block_file(block_model_file_path, table_columns, db_name=DB_NAME,
                    json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    try:
        model_name = get_model_name_from_path(block_model_file_path)
        conn = sqlite3.connect(db_name)
        columns_types = retrieve_columns_types(block_model_file_path)
        conn.execute(create_table_query(model_name, table_columns, columns_types))
        conn.commit()
        with open(block_model_file_path, "r") as block_file:
            columns_for_query = ",".join(table_columns)
            for block in block_file:
                block_parsed = ",".join(parse_block_column_types(block.strip().split(" ")))
                insert_query = "INSERT INTO {}({}) VALUES ({})".format(model_name, columns_for_query, block_parsed)
                conn.execute(insert_query)
            conn.commit()
        dump_model_information_into_json(model_name, table_columns, json_file_name)
        return True
    except sqlite3.IntegrityError:
        return False


def dump_model_information_into_json(model_name, column_names, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    with open(json_file_name, 'r') as json_file:
        data = json.load(json_file)
    data[model_name] = column_names
    with open(json_file_name, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True)


def get_models_information_json(json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    with open(json_file_name) as json_file:
        model_information_json = json.load(json_file)
    return model_information_json


def get_mineral_grades_information_json(json_file_name=MINERAL_GRADES_INFORMATION_FILE_NAME):
    with open(json_file_name) as json_file:
        mineral_grades_information_json = json.load(json_file)
    return mineral_grades_information_json


def get_available_models(json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    models = get_models_information_json(json_file_name)
    models_names = models.keys()
    return list(models_names)


def check_if_model_exists_in_json(block_model_name, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    model_information_json = get_models_information_json(json_file_name)
    if block_model_name in model_information_json.keys():
        return True
    else:
        return False


def get_block_model_object(block_model_name, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME, db_name=DB_NAME):
    if check_if_model_exists_in_json(block_model_name):
        columns = get_models_information_json(json_file_name)[block_model_name]
        columns_query_format = ",".join(columns)
        conn = sqlite3.connect(db_name)
        cursor = conn.execute("SELECT {} FROM {}".format(columns_query_format, block_model_name))
        blocks = []
        for row in cursor.fetchall():
            blocks.append(Block({attribute: value for (attribute, value) in zip(columns, row)}))
        minerals = get_mineral_grades_information_json()[block_model_name]
        return BlockModel(block_model_name, blocks, columns, minerals)
