import unittest
import load_block_model as lbm
test_model_name = "mclaughlin_test"
test_db_name = "block_model_test.db"
test_json_name = "model_information_test.json"
test_block_file_path = "mclaughlin_test.blocks"


class TestLoadBlockModel(unittest.TestCase):

    def test_get_model_name_from_path(self):
        self.assertEqual(lbm.get_model_name_from_path("some\\text\\before\\name.name"), "name")
        self.assertEqual(lbm.get_model_name_from_path("some/text/before/name.name"), "name")

    def test_retrieve_columns_types_valid_types(self):
        column_types = ["INT", "INT", "INT", "INT", "FLOAT", "INT", "FLOAT"]
        self.assertEqual(lbm.retrieve_columns_types(test_block_file_path), column_types)

    def test_retrieve_columns_types_invalid_types(self):
        column_types = ["INT", "INT", "INT", "FLOAT", "INT", "FLOAT"]
        column_types_empty = []
        self.assertFalse(lbm.retrieve_columns_types(test_block_file_path), column_types)
        self.assertFalse(lbm.retrieve_columns_types(test_block_file_path), column_types_empty)

    """def test_load_block_model_with_valid_file_return_valid_rows(self):
        rows = [
            [0, 31, 208, 44, -646, 489.58, 0, 0.038],
            [1, 32, 208, 44, - 646, 489.58, 0, 0.039],
            [2, 33, 208, 44, 2759, 239.58, 1, 0.039],
            [3, 31, 209, 44, - 1334, 1010.42, 0, 0.039],
            [4, 32, 209, 44, 13843, 1010.42, 1, 0.042],
            [5, 33, 209, 44, 15962, 989.58, 1, 0.045],
            [6, 34, 209, 44, -1286, 968.75, 0, 0.039],
            [7, 35, 209, 44, -1286, 968.75, 0, 0.038],
            [8, 31, 210, 44, 10896, 1041.67, 1, 0.038],
            [9, 32, 210, 44, 11740, 1041.67, 1, 0.039],
            [10, 33, 210, 44, -1375, 1041.67, 0, 0.04],
            [11, 34, 210, 44, -1375, 1041.67, 0, 0.039],
            [12, 35, 210, 44, 10896, 1041.67, 1, 0.038],
            [13, 30, 211, 44, 6543, 906.25, 1, 0.034],
            [14, 31, 211, 44, 9208, 1041.67, 1, 0.036],
            ]
        db_rows = []
        self.assertEqual(rows == db_rows, True) #not finished"""

