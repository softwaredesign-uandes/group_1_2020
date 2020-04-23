import unittest
import load_block_model as lbm
from constants import TEST_DB_NAME, TEST_LOADED_MODELS_INFORMATION_FILE_NAME

test_model_name = "mclaughlin_test"
test_db_name = "block_model_test.db"
test_json_name = "model_information_test.json"
test_existent_block_model_file_path = "mclaughlin_test.blocks"
test_nonexistent_block_model_file_path = "kd_test.blocks"


class TestLoadBlockModel(unittest.TestCase):

    def test_get_model_name_from_path(self):
        self.assertEqual(lbm.get_model_name_from_path("some\\text\\before\\name.name"), "name")
        self.assertEqual(lbm.get_model_name_from_path("some/text/before/name.name"), "name")
        self.assertEqual(lbm.get_model_name_from_path("some/text/before-the/name.name"), "name")

    def test_retrieve_columns_types_valid_types(self):
        column_types = ["INT", "INT", "INT", "INT", "FLOAT", "INT", "FLOAT"]
        self.assertEqual(lbm.retrieve_columns_types(test_existent_block_model_file_path), column_types)

    def test_load_block_file_return_true(self):
        columns = ["id", "x", "y", "z", "tonn", "blockvalue", "destination", "CU", "processProfit"]
        self.assertEqual(lbm.load_block_file(test_nonexistent_block_model_file_path,
                                             columns,
                                             TEST_DB_NAME,
                                             TEST_LOADED_MODELS_INFORMATION_FILE_NAME), True)

    def test_load_existent_block_file_return_false(self):
        columns = ['id', 'x', 'y', 'z', 'blockvalue', 'ton', 'destination', 'Au']
        self.assertEqual(
            lbm.load_block_file(test_existent_block_model_file_path,
                                columns,
                                TEST_DB_NAME,
                                TEST_LOADED_MODELS_INFORMATION_FILE_NAME), False)


if __name__ == "__main__":
    unittest.main()
