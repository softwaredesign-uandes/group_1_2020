import shutil
import tempfile
import unittest
from os import path

import load_block_model as lbm
from constants import TEST_DB_NAME, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME
from block_model import BlockModel
from block import Block
test_model_name = "mclaughlin_test"
test_db_name = "block_model_test.db"

test_existent_block_model_file_path = "mclaughlin_test.blocks"
test_nonexistent_block_model_file_path = "kd_test.blocks"
test_nonexistent_block_model_name = "json_test"

mclaughlin_columns = ['id', 'x', 'y', 'z', 'blockvalue', 'ton', 'destination', 'au']
mclaughlin_minerals = {"au": "oz_per_ton", "mass_columns": ["ton"]}
mclaughlin_block_model_test = BlockModel("mclaughlin_limit", [Block({'id': 0,
                                                                     'x': 31,
                                                                     'y': 208,
                                                                     'z': 44,
                                                                     'blockvalue': -646,
                                                                     'ton': 489.58,
                                                                     'destination': 0,
                                                                     'au': 0.038})], mclaughlin_columns,
                                         mclaughlin_minerals)


class TestLoadBlockModel(unittest.TestCase):

    def set_up(self):
        self.test_dir = tempfile.mkdtemp()

    def tear_down(self):
        shutil.rmtree(self.test_dir)

    def test_get_model_name_from_path_returns_correct_name(self):
        self.assertEqual(lbm.get_model_name_from_path("some\\text\\before\\name.name"), "name")

    def test_get_model_name_from_path_that_contains_normal_slash_returns_correct_name(self):
        self.assertEqual(lbm.get_model_name_from_path("some/text/before/name.name"), "name")

    def test_get_model_name_from_path_that_contains_special_characters_returns_correct_name(self):
        self.assertEqual(lbm.get_model_name_from_path("some/text/before-the/name.name"), "name")

    def test_retrieve_columns_types_valid_types(self):
        column_types = ["INT", "INT", "INT", "INT", "FLOAT", "INT", "FLOAT"]
        self.assertEqual(lbm.retrieve_columns_types(test_existent_block_model_file_path), column_types)

    def test_load_block_model_json_returns_true(self):
        columns = ["id", "x", "y", "z", "blockvalue", "ton", "destination", "au"]
        minerals = {"au": "oz_per_ton", "mass_columns": ["ton"]}
        blocks = [{'id': 0,'x': 31, 'y': 208, 'z': 44, 'blockvalue': -646, 'ton': 489.58, 'destination': 0, 'au': 0.038}]
        self.assertEqual(lbm.load_block_json(test_nonexistent_block_model_name, columns, minerals, blocks, TEST_DB_NAME,
                                             TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME), True)

    def test_load_block_file_return_true(self):
        columns = ["id", "x", "y", "z", "tonn", "blockvalue", "destination", "CU", "processProfit"]
        minerals = {"CU": "oz_per_ton", "mass_columns": ["tonn"]}
        self.assertEqual(lbm.load_block_file(test_nonexistent_block_model_file_path,
                                             columns,
                                             minerals,
                                             TEST_DB_NAME,
                                             TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                             TEST_MINERAL_GRADES_INFORMATION_FILE_NAME), True)

    def test_load_existent_block_file_return_false(self):
        columns = ['id', 'x', 'y', 'z', 'blockvalue', 'ton', 'destination', 'Au']
        minerals = {"au": "oz_per_ton", "mass_columns": ["ton"]}
        lbm.load_block_file(test_existent_block_model_file_path,
                            columns,
                            minerals,
                            TEST_DB_NAME,
                            TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                            TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(
            lbm.load_block_file(test_existent_block_model_file_path,
                                columns,
                                minerals,
                                TEST_DB_NAME,
                                TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                TEST_MINERAL_GRADES_INFORMATION_FILE_NAME), False)


    def test_load_block_model_object_returns_true(self):
        self.assertEqual(lbm.load_block_model_object(mclaughlin_block_model_test, TEST_DB_NAME,
                                                     TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                     TEST_MINERAL_GRADES_INFORMATION_FILE_NAME), True)

    def test_load_model_precedence_file(self):
        self.set_up()
        test_prec_file = open(path.join(self.test_dir, "test.prec"), 'w')
        test_prec_file.write("0 1 1\n" +
                             "1 1 2\n" +
                             "2 0\n" +
                             "3 0")
        test_prec_file.close()
        test_prec_file = open(path.join(self.test_dir, "test.prec"), 'r')
        self.assertEqual(lbm.load_model_precedence("test", self.test_dir), {"0": ["1"], "1": ["2"], "2": [], "3": []})


if __name__ == "__main__":
    unittest.main()
