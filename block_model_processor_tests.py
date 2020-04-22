import block_model_proccesor as bmp
import unittest
test_model_name = "mclaughlin_test"
class TestBlockModelProcessor(unittest.TestCase):
    def test_get_data_table_return_true(self):
        # TODO: Check how blocks are shown and make test
        return

    def test_check_if_model_exists_in_json_return_true(self):
        self.assertEqual(bmp.check_if_model_exists_in_json("models_information.json"),True)

    def test_get_headers_tabulated_table_return_true(self):
        self.assertEqual(bmp.get_headers_tabulated_table("block_model.db"), True)

    def test_get_model_data_table(self):
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
        self.assertEqual(bmp.get_model_data_table(test_model_name, 0, 14), rows)

