import unittest, json
from api import __main__ as api_main
import block_model_proccesor
from constants import TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME

class TestApi(unittest.TestCase):
    def test_get_block_models_names_return_ok_status_code(self):
        self.assertEqual(api_main.get_block_models_names(TEST_LOADED_MODELS_INFORMATION_FILE_NAME).status_code, 200)

    def test_get_block_model_blocks_return_ok_status_code(self):
        first_block_model_name = block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)[0]['name']
        self.assertEqual(api_main.get_block_model_blocks(first_block_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME).status_code, 200)

    def test_get_block_models_names_return_correct(self):
        self.assertEqual(block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME), json.loads(api_main.get_block_models_names(TEST_LOADED_MODELS_INFORMATION_FILE_NAME).data))
        
    def test_get_block_model_blocks_return_correct(self):
        first_block_model_name = block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)[0]['name']
        self.assertEqual(block_model_proccesor.get_block_list(first_block_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME), json.loads(api_main.get_block_model_blocks(first_block_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME).data))

    def test_get_feature_flags_return_correct(self):
        default_feature_flags_json = {"restful_response": False, "block_info": False}
        default_feature_flags_types_json = {}
        for flag in default_feature_flags_json:
            default_feature_flags_types_json[flag] = type(default_feature_flags_json[flag])
        api_feature_flags_json = api_main.get_feature_flags()
        api_feature_flags_types_json = {}
        for flag in api_feature_flags_json:
            api_feature_flags_types_json[flag] = type(api_feature_flags_json[flag])
        self.assertEqual(default_feature_flags_types_json, api_feature_flags_types_json)

# first_block_model_name = block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)[0]['name']
# print(first_block_model_name)
