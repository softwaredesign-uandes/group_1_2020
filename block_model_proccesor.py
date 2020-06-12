from tabulate import tabulate
import load_block_model
from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME

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


def get_mass_in_kilograms(block_model, x, y, z, mass_column_name):
    mass_in_tons = get_attribute_from_block(block_model, x, y, z, mass_column_name)
    if mass_in_tons:
        return mass_in_tons * 1000

    return False


def get_attribute_from_block(block_model, x, y, z, attribute):
    block = block_model.get_block_by_coordinates(x, y, z)
    if block:
        attribute = block.get_attribute_value(attribute)
        return attribute
    else:
        return None


def get_percentage_grade_for_mineral_from_different_unit(block_model, x, y, z, mineral_name):
    unit = block_model.minerals[mineral_name.lower()]
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
    return None


def get_percentage_grade_for_mineral_from_copper_proportion(block_model, x, y, z, rock_tonnes_column,
                                                            ore_tonnes_column):
    rock_tonnes = get_attribute_from_block(block_model, x, y, z, rock_tonnes_column)
    ore_tonnes = get_attribute_from_block(block_model, x, y, z, ore_tonnes_column)
    if rock_tonnes and ore_tonnes:
        total_tonnes = ore_tonnes + rock_tonnes
        return round((ore_tonnes / total_tonnes) * 100, 3)
    return False


def get_percentage_grade_for_mineral_from_gold_proportion(block_model, x, y, z, au_fa):
    AuFa = get_attribute_from_block(block_model, x, y, z, au_fa)
    if AuFa:
        return round(AuFa * 100, 3)
    return False


def get_available_minerals(block_model):
    minerals_names = block_model.minerals.keys()
    return list(minerals_names)


def get_block_list(block_model_name, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME, db_name=DB_NAME):
    block_list = []
    if block_model_name in load_block_model.get_available_models(json_file_name):
        block_model = load_block_model.get_block_model_object(block_model_name, json_file_name, db_name)

        for block in block_model.blocks:
            block_list.append(block.attributes)
    return block_list


def get_block_info_by_index(block_model_name, index):
    if block_model_name in load_block_model.get_available_models():
        block_model = load_block_model.get_block_model_object(block_model_name)
        for block in block_model.blocks:
            if block.attributes["id"] == index:
                block_data = {"index": index, "x": block.attributes["x"], "y": block.attributes["y"], "z": block.attributes["z"]}
                pure_block_model_name = get_pure_block_model_name(block_model_name)
                minerals_and_calculations = load_block_model.get_mineral_grades_information_json()[pure_block_model_name]
                block_model = load_block_model.get_block_model_object(block_model_name)
                for mineral in minerals_and_calculations:
                    if minerals_and_calculations[mineral] in ["percentage", "ppm", "oz_per_ton"]:
                        minerals_and_calculations[mineral] = get_percentage_grade_for_mineral_from_different_unit(block_model,
                                                              block.attributes["x"], block.attributes["y"], block.attributes["z"], mineral)
                    elif minerals_and_calculations[mineral] == "cu_proportion":
                        minerals_and_calculations[mineral] = "grado de {} en %".format(minerals_and_calculations[mineral])
                    elif minerals_and_calculations[mineral] == "au_proportion":
                        minerals_and_calculations[mineral] = "grado de {} en %".format(minerals_and_calculations[mineral])
                block_data["grades"] = minerals_and_calculations
                block_data["mass"] = "masa en kg"
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