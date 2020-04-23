import block_model_proccesor as bmp
import unittest
import tabulate

test_model_name = "mclaughlin_test"
test_db_name = "block_model_test.db"
test_json_name = "model_information_test.json"


class TestBlockModelProcessor(unittest.TestCase):

    def test_check_if_model_exists_in_json_return_true(self):
        self.assertEqual(bmp.check_if_model_exists_in_json(test_model_name, test_json_name), True)

    # def test_get_headers_tabulated_table_return_true(self):
    #   self.assertEqual(bmp.get_headers_tabulated_table(test_db_name), True)

    def test_get_model_data_table_returns_correct_rows(self):
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
            [14, 31, 211, 44, 9208, 1041.67, 1, 0.036]
        ]
        self.assertEqual(bmp.get_model_data_table(test_model_name, 0, 14, test_db_name), rows)

    def test_get_number_of_blocks_in_model_return_true(self):
        self.assertEqual(bmp.get_number_of_blocks_in_model(test_model_name, test_db_name), 15)

    # TODO: Test if get number of blocks return false with inexistent corrdinates

    def test_get_mass_in_kilograms_return_true(self):
        self.assertEqual(bmp.get_mass_in_kilograms(test_model_name, 31, 208, 44, "ton", test_db_name), 489580)

    # TODO: Test if get mass returns false with inexistent coordinates

    def test_get_tabulated_blocks_with_mclaughlin_test_return_true(self):
        rows = [
            ["id", "x", "y", "z", "blockvalue", "ton", "destination", "Au"],
            ["__", "_", "_", "_", "__________", "___", "___________", "__"],
            [0, 31, 208, 44, -646, 489.58, 0, 0.038],
            [1, 32, 208, 44, - 646, 489.58, 0, 0.039],
            [2, 33, 208, 44, 2759, 239.58, 1, 0.039],
            [3, 31, 209, 44, - 1334, 1010.42, 0, 0.039],
            [4, 32, 209, 44, 13843, 1010.42, 1, 0.042]
        ]
        rows = tabulate.tabulate(rows)
        self.assertEqual(bmp.get_tabulated_blocks(test_model_name, 0, 4, test_json_name, test_db_name), rows)

    # TODO: Test get attribute from block return true
    def test_get_attribute_from_block_return_true(self):
        self.assertEqual(bmp.get_attribute_from_block(test_model_name, 31, 208, 44, "blockvalue", test_db_name), -646)

    def test_get_attribute_from_block_wrong_coordinates_return_false(self):
        self.assertFalse(bmp.get_attribute_from_block(test_model_name,0,0,0, "blockvalue", test_db_name), True)


    # TODO: Test get percentage grade for mineral from copper proportion return true
    # TODO: Test get percentage grade for mineral from copper proportion return false with wrong coordinates

    # TODO: Test get percentage grade for mineral from different unit proporion return true
    # TODO: Test get percentage grade for mineral from different unit proporion return false with wrong coordinates
    def test_get_percentage_grade_for_mineral_from_different_unit_return_true(self):
        self.assertEqual(bmp.get_percentage_grade_for_mineral_from_different_unit("p4hd", 53, 19, 63, "ag"), 0.004053)

    def test_get_percentage_grade_for_mineral_from_different_unit_return_false_with_wrong_coordinates(self):
        self.assertEqual(bmp.get_percentage_grade_for_mineral_from_different_unit("p4hd", 0, 38, 47, "au"), False)

    # TODO: Test get percentage grade for mineral from gold proportion return false with wrong coordinates

    def test_get_percentage_grade_for_mineral_from_gold_proportion_return_true(self):
        model_information_test = bmp.get_models_information_json(test_json_name)
        au_fa_column_name = model_information_test["w23_test"][7]
        self.assertEqual(bmp.get_percentage_grade_for_mineral_from_gold_proportion("w23_test", 58, 50, 18, au_fa_column_name, test_db_name), 9.787)

    # TODO: Test Get mineral value returns true
    # TODO: Test get mineral value returns false with wrong coordinates
