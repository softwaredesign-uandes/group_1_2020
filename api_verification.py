from load_block_model import get_available_models, get_model_columns_names
from constants import LOADED_MODELS_INFORMATION_FILE_NAME, MASS_UNIT_FOR_REBLOCK


def verify_reblock_information(data, block_model_name, loaded_models_json=LOADED_MODELS_INFORMATION_FILE_NAME):
    correct_attribute_types = {"rx", "ry", "rz", "continuous_attributes", "proportional_attributes", "categorical_attributes", "columns_with_mass"}
    available_models = get_available_models(loaded_models_json)
    request_attribute_types = set(list(data.keys()))
    if correct_attribute_types != request_attribute_types:
        return False
    if block_model_name not in available_models:
        return False
    model_columns = get_model_columns_names(block_model_name, loaded_models_json)
    if type(data["rx"]) != int:
        return False
    if type(data["ry"]) != int:
        return False
    if type(data["rz"]) != int:
        return False
    if type(data["continuous_attributes"]) != list:
        return False
    if type(data["proportional_attributes"]) != dict:
        return False
    if type(data["categorical_attributes"]) != list:
        return False
    if type(data["columns_with_mass"]) != list:
        return False
    for column in data["continuous_attributes"]:
        if column not in model_columns:
            return False
    for column in data["proportional_attributes"].keys():
        if column not in model_columns:
            return False
    for column in data["categorical_attributes"]:
        if column not in model_columns:
            return False
    for column in data["categorical_attributes"]:
        if column not in model_columns:
            return False
    for column,unit in data["proportional_attributes"].items():
        if unit not in MASS_UNIT_FOR_REBLOCK:
            return False
        if type(column) != str:
            return False
    return True


def verify_model_exists(block_model_name, loaded_models_json=LOADED_MODELS_INFORMATION_FILE_NAME):
    available_models = get_available_models(loaded_models_json)
    if block_model_name not in available_models:
        return False
    else:
        return True


def verify_json_block_post(json_request):
    if not json_request.hasOwnProperty('name'):
        return False
    if not json_request.hasOwnProperty('columns'):
        return False
    else:
        if ["id", "x", "y", "z"] <= json_request["columns"]:
            return False
    if not json_request.hasOwnProperty('minerals'):
        return False
    if not json_request.hasOwnProperty('blocks'):
        return False
    else:
        for block in json_request["blocks"]:
            for column_name in json_request['columns']:
                if not block.hasOwnProperty(column_name):
                    return False
    return True
