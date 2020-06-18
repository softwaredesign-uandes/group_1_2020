import unittest, json
from api import __main__ as api_main
import block_model_proccesor
from constants import TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME
import requests


class TestApi(unittest.TestCase):

    def setUp(self):
        api_main.app.config['TESTING'] = True
        api_main.app.config['DEBUG'] = False
        self.app = api_main.app.test_client()

    def test_get_block_models_names_return_ok_status_code(self):
        self.assertEqual(api_main.get_block_models_names(TEST_LOADED_MODELS_INFORMATION_FILE_NAME).status_code, 200)

    def test_get_block_model_blocks_return_ok_status_code(self):
        first_block_model_name = \
            block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)[0]['name']
        self.assertEqual(
            api_main.get_block_model_blocks(first_block_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                            TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME).status_code, 200)

    def test_get_block_models_names_return_correct(self):
        self.assertEqual(block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME),
                         json.loads(api_main.get_block_models_names(TEST_LOADED_MODELS_INFORMATION_FILE_NAME).data))

    def test_get_block_model_blocks_return_correct(self):
        first_block_model_name = \
            block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)[0]['name']
        self.assertEqual(
            block_model_proccesor.get_block_list(first_block_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                 TEST_DB_NAME), json.loads(
                api_main.get_block_model_blocks(first_block_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME).data))

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

    def test_reblock_block_model_endpoint_bad_parameter_names_return_status_code_400(self):
        data = {
            "rx": 1,
            "ry": 1,
            "rz": 1,
            "continuousattributes": [
                "blockvalue",
                "ton"
            ],
            "proportionalattributes": {"au": "oz_per_ton"},
            "categoricalattributes": ["destination"],
            "columnswith_mass": ["ton"]
        }
        model_name = "mclaughlin_limit"
        response = api_main.reblock_block_model(model_name, data, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 400)

    # def test_reblock_block_model_endpoint_correct_data_return_status_code_200(self):
    #     data = {
    #         "rx": 1,
    #         "ry": 1,
    #         "rz": 1,
    #         "continuous_attributes": [
    #             "blockvalue",
    #             "ton"
    #         ],
    #         "proportional_attributes": {"au": "oz_per_ton"},
    #         "categorical_attributes": ["destination"],
    #         "columns_with_mass": ["ton"]
    #     }
    #     model_name = "mclaughlin_limit"
    #     response = api_main.reblock_block_model(model_name, data, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
    #     self.assertEqual(response.status_code, 200)

    def test_reblock_block_model_endpoint_inexistent_model_returns_400(self):
        data = {
            "rx": 1,
            "ry": 1,
            "rz": 1,
            "continuous_attributes": [
                "blockvalue"
            ],
            "proportional_attributes": {"au": "oz_per_ton"},
            "categorical_attributes": ["destination"],
            "columns_with_mass": ["ton"]
        }
        model_name = "kd"
        response = api_main.reblock_block_model(model_name, data, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 400)

    def test_reblock_block_model_endpoint_incorrect_columns_returns_400(self):
        data = {
            "rx": 1,
            "ry": 1,
            "rz": 1,
            "continuous_attributes": [
                "bkvalue"
            ],
            "proportional_attributes": {"cu": "oz_per_ton"},
            "categorical_attributes": ["destinn"],
            "columns_with_mass": ["ton"]
        }
        model_name = "mclaughlin_limit"
        response = api_main.reblock_block_model(model_name, data, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 400)

    def test_get_block_model_blocks_existent_model_returns_200(self):
        self.assertEqual(api_main.get_block_model_blocks("mclaughlin_limit",
                                                         TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                         TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME).status_code, 200)

    def test_get_block_model_blocks_inexistent_model_returns_400(self):
        self.assertEqual(api_main.get_block_model_blocks("inexistent_model",
                                                         TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                         TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME).status_code, 400)

    def test_input_block_model_inserts_blocks_into_db(self):
        data = {
                    "name": "test_model_2",
                    "columns": ["id", "x", "y", "z", "ton", "au","destination"],
                    "minerals": {"au": "proportion"},
                    "blocks":
                            [
                            {
                                 "id": 0,
                                 "x": 0,
                                 "y": 0,
                                 "z": 0,
                                 "ton": 30,
                                 "au": 30,
                                 "destination": 0
                            },
                            {"id": 1, "x": 1, "y": 0, "z": 0, "ton": 20, "au": 10, "destination": 1},
                            {"id": 2, "x": 2, "y": 0, "z": 0, "ton": 10, "au": 20, "destination": 1},
                            {"id": 3, "x": 3, "y": 0, "z": 0, "ton": 40, "au": 10, "destination": 1}
                            ]
                }
        response = api_main.input_block_model(data, json_file_name=TEST_LOADED_MODELS_INFORMATION_FILE_NAME, db_name=TEST_DB_NAME,
                      json_mineral_grades_file_name=TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 200)

    def test_input_block_model_inserts_blocks_into_db_return_400(self):
        data = {
            "name": "test_model_2",
            "columns": ["id", "x", "y", "z", "ton", "au", "destination"],
            "blocks":
                [
                    {
                        "id": 0,
                        "x": 0,
                        "y": 0,
                        "z": 0,
                        "ton": 30,
                        "au": 30,
                        "destination": 0
                    },
                    {"id": 1, "x": 1, "y": 0, "z": 0, "ton": 20, "au": 10, "destination": 1},
                    {"id": 2, "x": 2, "y": 0, "z": 0, "ton": 10, "au": 20, "destination": 1},
                    {"id": 3, "x": 3, "y": 0, "z": 0, "ton": 40, "au": 10, "destination": 1}
                ]
        }
        response = api_main.input_block_model(data, json_file_name=TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                              db_name=TEST_DB_NAME,
                                              json_mineral_grades_file_name=TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 400)

    def test_input_block_model_inserts_blocks_into_db_same_name_return_400(self):
        data = {
                    "name": "mclaughlin_limit",
                    "columns": ["id", "x", "y", "z", "ton", "au","destination"],
                    "minerals": {"au": "proportion"},
                    "blocks":
                            [
                            {
                                 "id": 0,
                                 "x": 0,
                                 "y": 0,
                                 "z": 0,
                                 "ton": 30,
                                 "au": 30,
                                 "destination": 0
                            },
                            {"id": 1, "x": 1, "y": 0, "z": 0, "ton": 20, "au": 10, "destination": 1},
                            {"id": 2, "x": 2, "y": 0, "z": 0, "ton": 10, "au": 20, "destination": 1},
                            {"id": 3, "x": 3, "y": 0, "z": 0, "ton": 40, "au": 10, "destination": 1}
                            ]
                }
        response = api_main.input_block_model(data, json_file_name=TEST_LOADED_MODELS_INFORMATION_FILE_NAME, db_name=TEST_DB_NAME,
                      json_mineral_grades_file_name=TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 400)


# first_block_model_name = block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)[0]['name']
# print(first_block_model_name)
