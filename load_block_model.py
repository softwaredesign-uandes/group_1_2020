import os
import sqlite3
import json
from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME


def create_db():
    DB_NAME = "block_model.db"
    if os.path.isfile(DB_NAME):
        os.remove(DB_NAME)
    sqlite3.connect(DB_NAME)


def get_model_name_from_path(block_model_file_path):
    if "\\" in block_model_file_path:
        separator = "\\"
    else:
        separator = "/"
    model_name = block_model_file_path.split(separator)[-1].split(".")[0]
    return model_name


def retrieve_columns_types(block_model_file_path, model_has_id):
    types = []
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    block_model_file_path = os.path.join(THIS_FOLDER, block_model_file_path)
    with open(block_model_file_path, "r") as blocks:
        first_line = list(blocks)[0].strip().split(" ")
        if model_has_id:
            first_line = first_line[1:]
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
    print(query)
    return query


def load_block_file(block_model_file_path, table_columns, model_has_id, db_name=DB_NAME):
    model_name = get_model_name_from_path(block_model_file_path)
    conn = sqlite3.connect(db_name)
    columns_types = retrieve_columns_types(block_model_file_path, model_has_id)
    conn.execute(create_table_query(model_name, table_columns, columns_types))
    conn.commit()
    with open(block_model_file_path, "r") as block_file:
        columns_for_query = ",".join(table_columns)
        for block in block_file:
            id_count = 1
            block_parsed = ",".join(parse_block_column_types(block.strip().split(" ")))

            if model_has_id:
                insert_query = "INSERT INTO {}({}) VALUES ({})".format(model_name, columns_for_query, block_parsed)
            else:
                insert_query = "INSERT INTO {}({}) VALUES ({},{})".format(model_name, columns_for_query, id_count,
                                                                          ",".join(block_parsed))
            print(insert_query)
            conn.execute(insert_query)
        conn.commit()
    dump_model_information_into_json(model_name, table_columns)


def dump_model_information_into_json(model_name, column_names):
    with open(LOADED_MODELS_INFORMATION_FILE_NAME, 'r') as json_file:
        data = json.load(json_file)
    data[model_name] = column_names
    with open(LOADED_MODELS_INFORMATION_FILE_NAME, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True)

