from tabulate import tabulate
import load_block_model
from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME, \
    TEST_MINERAL_GRADES_INFORMATION_FILE_NAME, MASS_UNIT_FOR_REBLOCK, MASS_COLUMNS_JSON_ENTRY, SPECIAL_PROPORTION

def get_model_data_table(block_model, from_id, to_id):
    data_table = []
    data = block_model.get_blocks_range(from_id, to_id)
    columns = block_model.columns
    for row in data:
        data_table.append([row.attributes[column] for column in columns])
    return data_table


def get_headers_tabulated_table(block_model):
    separator_lines = []
    for column in block_model.columns:
        separator_lines.append("_" * len(column))
    return [block_model.columns, separator_lines]


def get_tabulated_blocks(block_model, from_id, to_id):
    table = get_headers_tabulated_table(block_model)
    table.extend(get_model_data_table(block_model, from_id, to_id))
    return tabulate(table)


def get_mass_in_kilograms(block_model, x, y, z, mass_columns):
    try:
        mass_in_tons = 0
        for mass_column in mass_columns:
            mass_in_tons += get_attribute_from_block(block_model, x, y, z, mass_column)
        if mass_in_tons:
            return mass_in_tons * 1000
        return False
    except:
        return False


def get_attribute_from_block(block_model, x, y, z, attribute):
    block = block_model.get_block_by_coordinates(x, y, z)
    if block:
        attribute_value = block.get_attribute_value(attribute)
        return attribute_value
    else:
        return None


def get_percentage_grade_for_mineral_from_different_unit(block_model, x, y, z, mineral_name):
    unit = block_model.minerals[mineral_name]
    attribute = get_attribute_from_block(block_model, x, y, z, mineral_name)

    if unit == "percentage":
        if attribute is not None:
            return attribute
    elif unit == "ppm":
        if attribute is not None:
            return round(attribute / 10000, 6)
    elif unit == "oz_per_ton":
        if attribute is not None:
            return round(attribute * 0.00342853, 6)
    elif unit == "proportion":
        if attribute is not None:
            return attribute * 100
    return None


def get_percentage_grade_for_mineral_from_copper_proportion(block_model, x, y, z, ore_tonnes_column):
    try:
        total_tonnes = 0
        for mass_column in block_model.minerals[MASS_COLUMNS_JSON_ENTRY]:
            mass_column_value = get_attribute_from_block(block_model, x, y, z, mass_column)
            total_tonnes += mass_column_value
        ore_tonnes = get_attribute_from_block(block_model, x, y, z, ore_tonnes_column)
        if total_tonnes and ore_tonnes is not None:
            percentage_of_grade = round((float(ore_tonnes) / total_tonnes) * 100, 3)
            return percentage_of_grade
        return False
    except:
        return False


def get_percentage_grade_for_mineral_from_gold_proportion(block_model, x, y, z, au_fa):
    AuFa = get_attribute_from_block(block_model, x, y, z, au_fa)
    if AuFa:
        return round(AuFa * 100, 3)
    return False


def get_available_minerals(block_model):
    minerals_names = block_model.minerals.keys()
    return list(minerals_names)


def get_block_list(block_model_name, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME, db_name=DB_NAME, json_mineral_grades_file_name=TEST_MINERAL_GRADES_INFORMATION_FILE_NAME):
    block_list = []
    if block_model_name in load_block_model.get_available_models(json_file_name):
        block_model = load_block_model.get_block_model_object(block_model_name, json_file_name, db_name, json_mineral_grades_file_name)

        for block in block_model.blocks:
            block_list.append(block.attributes)
    return block_list


def get_block_info_by_index(block_model_name, index):
    if block_model_name in load_block_model.get_available_models():
        block_model = load_block_model.get_block_model_object(block_model_name)
        for block in block_model.blocks:
            if block.attributes["id"] == index:
                x = block.attributes["x"]
                y = block.attributes["y"]
                z = block.attributes["z"]
                block_data = {"index": index, "x":x, "y": y, "z": z}
                pure_block_model_name = get_pure_block_model_name(block_model_name)
                minerals_and_calculations = load_block_model.get_mineral_grades_information_json()[pure_block_model_name]
                minerals_and_calculations_copy = minerals_and_calculations.copy()
                block_data["mass"] = get_mass_in_kilograms(block_model, x, y, z, minerals_and_calculations_copy[MASS_COLUMNS_JSON_ENTRY])
                del minerals_and_calculations_copy[MASS_COLUMNS_JSON_ENTRY]
                block_data["grades"] = {}
                for mineral in minerals_and_calculations:
                    mineral_name = get_mineral_name_from_column_name(mineral)
                    if minerals_and_calculations[mineral] in MASS_UNIT_FOR_REBLOCK:
                        block_data["grades"][mineral_name] = get_percentage_grade_for_mineral_from_different_unit(block_model,
                                                              x, y, z, mineral)
                    elif minerals_and_calculations[mineral] == SPECIAL_PROPORTION:
                        block_data["grades"][mineral_name] = get_percentage_grade_for_mineral_from_copper_proportion(block_model, x, y, z, mineral)

                return block_data


def get_model_names_to_dictionary(json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    model_names = load_block_model.get_available_models(json_file_name)
    model_names_dict_array = []
    for model_name in model_names:
        model_name_dict = {"name": model_name}
        model_names_dict_array.append(model_name_dict)
    return model_names_dict_array


def get_pure_block_model_name(block_model_name):
    pure_block_model_name = block_model_name.split("_reblocked")[0].split("_test")[0]
    return pure_block_model_name


def get_mineral_name_from_column_name(column_name):
    column_name_in_lower_case = column_name.lower()
    if column_name_in_lower_case.__contains__("au"):
        return "au"
    elif column_name_in_lower_case.__contains__("ag"):
        return "ag"
    else:
        return "cu"