from tabulate import tabulate
import sqlite3
import json

from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME, MINERAL_GRADES_INFORMATION_FILE_NAME


def get_model_data_table(block_model_name, from_id, to_id, db_name=DB_NAME):
    data_table = []
    conn = sqlite3.connect(db_name)
    cursor = conn.execute("SELECT * FROM {} WHERE ID >= {} AND ID <= {}".format(block_model_name, from_id, to_id))
    for row in cursor:
        data_table.append(list(row))
    return data_table


def get_headers_tabulated_table(block_model_name, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    model_information_json = get_models_information_json(json_file_name)
    separator_lines = []
    for column in model_information_json[block_model_name]:
        separator_lines.append("_" * len(column))
    return [model_information_json[block_model_name], separator_lines]


def get_block_model_columns(block_model_name, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    block_models_available = get_models_information_json(json_file_name)
    return block_models_available[block_model_name]


def check_if_model_exists_in_json(block_model_name, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    model_information_json = get_models_information_json(json_file_name)
    try:
        info = model_information_json[block_model_name]
        return True
    except:
        return False


def get_models_information_json(json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    with open(json_file_name) as json_file:
        model_information_json = json.load(json_file)
    return model_information_json


def get_tabulated_blocks(block_model_name, from_id, to_id, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME,
                         db_name=DB_NAME):  # needs test
    if check_if_model_exists_in_json(block_model_name, json_file_name):
        table = get_headers_tabulated_table(block_model_name, json_file_name)
        table.extend(get_model_data_table(block_model_name, from_id, to_id, db_name))
        return tabulate(table)
    return False


def get_mass_in_kilograms(block_model_name, x, y, z, mass_column_name, db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute(
        "SELECT {} FROM {} WHERE x = {} AND y = {} AND z = {}".format(mass_column_name, block_model_name, x, y, z))
    mass_in_tons = cursor.fetchone()
    if mass_in_tons is not None:
        return mass_in_tons[0] * 1000
    return False


def get_available_models(json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    models = get_models_information_json(json_file_name)
    models_names = models.keys()
    return list(models_names)


def get_number_of_blocks_in_model(block_model_name, db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute("SELECT COUNT(*) FROM {}".format(block_model_name))
    return cursor.fetchall()[0][0]


def get_attribute_from_block(block_model_name, x, y, z, attribute, db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute(
        "SELECT {} from {} WHERE x = {} AND y = {} AND z = {}".format(attribute, block_model_name, x, y, z))
    requested_attributed = cursor.fetchone()
    if requested_attributed is not None:
        return requested_attributed[0]
    return False


def get_mineral_grades_information_json():
    with open(MINERAL_GRADES_INFORMATION_FILE_NAME) as json_file:
        mineral_grades_information_json = json.load(json_file)
    return mineral_grades_information_json


def get_percentage_grade_for_mineral_from_different_unit(block_model_name, x, y, z, mineral_name, db_name=DB_NAME):
    ore_grades_information_json = get_mineral_grades_information_json()
    unit = ore_grades_information_json[block_model_name][mineral_name.lower()]

    if unit == "percentage":
        percentage = get_mineral_value(block_model_name, x, y, z, mineral_name, db_name)
        if percentage is not None:
            return percentage[0]
        return False
    elif unit == "ppm":
        ppm = get_mineral_value(block_model_name, x, y, z, mineral_name, db_name)
        if ppm is not None:
            return round(ppm[0] / 10000, 6)
        return False
    elif unit == "oz_per_ton":
        oz_per_ton = get_mineral_value(block_model_name, x, y, z, mineral_name, db_name)
        if oz_per_ton is not None:
            return round(oz_per_ton[0] * 0.00342853, 6)
        return False


def get_mineral_value(block_model_name, x, y, z, mineral_name, db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute(
        "SELECT {} FROM {} WHERE x = {} AND y = {} AND z = {}".format(mineral_name, block_model_name, x, y, z))
    return cursor.fetchone()


def get_percentage_grade_for_mineral_from_copper_proportion(block_model_name, x, y, z, rock_tonnes_column,
                                                            ore_tonnes_column, db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute(
        "SELECT {}, {} FROM {} WHERE x = {} AND y = {} AND z = {}".format(rock_tonnes_column, ore_tonnes_column,
                                                                          block_model_name, x, y, z))
    tonnes = cursor.fetchone()
    if tonnes is not None:
        rock_tonnes = tonnes[0]
        ore_tonnes = tonnes[1]
        total_tonnes = ore_tonnes + rock_tonnes
        return round((ore_tonnes / total_tonnes) * 100, 3)
    return False


def get_percentage_grade_for_mineral_from_gold_proportion(block_model_name, x, y, z, au_fa, db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute(
        "SELECT {} FROM {} WHERE x = {} AND y = {} AND z = {}".format(au_fa, block_model_name, x, y, z))
    AuFa = cursor.fetchone()
    if AuFa is not None:
        return round(AuFa[0] * 100, 3)
    return False


def get_available_minerals(block_model_name, json_file_name=MINERAL_GRADES_INFORMATION_FILE_NAME):
    minerals = get_models_information_json(json_file_name)
    minerals_names = minerals[block_model_name].keys()
    return list(minerals_names)
