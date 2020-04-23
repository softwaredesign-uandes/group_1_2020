import block_model_proccesor as bmp
import unittest
import tabulate
from constants import TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME

test_model_name = "mclaughlin_test"
test_db_name = "block_model_test.db"


class TestBlockModelProcessor(unittest.TestCase):

    def test_check_if_model_exists_in_json_return_true(self):
        self.assertEqual(bmp.check_if_model_exists_in_json(test_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME),
                         True)

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
        self.assertEqual(bmp.get_model_data_table(test_model_name,
                                                  0,
                                                  14,
                                                  TEST_DB_NAME), rows)

    def test_get_number_of_blocks_in_model_return_correct_number(self):
        self.assertEqual(bmp.get_number_of_blocks_in_model(test_model_name,
                                                           TEST_DB_NAME), 15)

    def test_get_mass_in_kilograms_with_correct_information_return_correct_number(self):
        self.assertEqual(bmp.get_mass_in_kilograms(test_model_name,
                                                   31, 208, 44,
                                                   "ton",
                                                   TEST_DB_NAME), 489580)

    def test_get_mass_in_kilograms_with_wrong_coordinates_return_false(self):
        self.assertEqual(bmp.get_mass_in_kilograms(test_model_name,
                                                   1, 2, 3,
                                                   "ton",
                                                   TEST_DB_NAME), False)

    def test_get_tabulated_blocks_with_mclaughlin_test_return_correct_information(self):
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
        self.assertEqual(
            bmp.get_tabulated_blocks(test_model_name, 0, 4, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME),
            rows)

    def test_get_attribute_from_block_return_correct_result(self):
        self.assertEqual(bmp.get_attribute_from_block(test_model_name,
                                                      31, 208, 44,
                                                      "blockvalue",
                                                      TEST_DB_NAME), -646)

    def test_get_attribute_from_block_wrong_coordinates_return_false(self):
        self.assertFalse(bmp.get_attribute_from_block(test_model_name,
                                                      0, 0, 0,
                                                      "blockvalue",
                                                      TEST_DB_NAME), True)

    def test_get_percentage_grade_for_mineral_from_copper_proportion_return_true(self):
        models_information_test = bmp.get_models_information_json(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)
        rock_tonnes_column_name = models_information_test["zuck_medium_test"][6]
        ore_tonnes_column_name = models_information_test["zuck_medium_test"][7]
        self.assertEqual(bmp.get_percentage_grade_for_mineral_from_copper_proportion("zuck_medium_test",
                                                                                     23, 33, 7,
                                                                                     rock_tonnes_column_name,
                                                                                     ore_tonnes_column_name,
                                                                                     TEST_DB_NAME), 72.727)

    def test_get_percentage_grade_for_mineral_from_copper_proportion_return_false_with_wrong_coordinates(self):
        models_information_test = bmp.get_models_information_json(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)
        rock_tonnes_column_name = models_information_test["zuck_medium_test"][6]
        ore_tonnes_column_name = models_information_test["zuck_medium_test"][7]
        self.assertEqual(bmp.get_percentage_grade_for_mineral_from_copper_proportion("zuck_medium_test",
                                                                                     0, 1, 2,
                                                                                     rock_tonnes_column_name,
                                                                                     ore_tonnes_column_name,
                                                                                     TEST_DB_NAME), False)

    def test_get_percentage_grade_for_mineral_from_different_unit_return_correct_result(self):
        self.assertEqual(bmp.get_percentage_grade_for_mineral_from_different_unit("p4hd_test",
                                                                                  53, 19, 63,
                                                                                  "ag",
                                                                                  TEST_DB_NAME), 0.004053)

    def test_get_percentage_grade_for_mineral_from_different_unit_return_false_with_wrong_coordinates(self):
        self.assertEqual(bmp.get_percentage_grade_for_mineral_from_different_unit("p4hd_test",
                                                                                  0, 38, 47,
                                                                                  "au",
                                                                                  TEST_DB_NAME), False)

    def test_get_percentage_grade_for_mineral_from_gold_proportion_return_true(self):
        models_information_test = bmp.get_models_information_json(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)
        au_fa_column_name = models_information_test["w23_test"][7]
        self.assertEqual(
            bmp.get_percentage_grade_for_mineral_from_gold_proportion("w23_test",
                                                                      58, 50, 18,
                                                                      au_fa_column_name,
                                                                      TEST_DB_NAME), 9.787)

    def test_get_percentage_grade_for_mineral_from_gold_proportion_with_wrongs_coordinates(self):
        models_information_test = bmp.get_models_information_json(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)
        au_fa_column_name = models_information_test["w23_test"][7]
        self.assertEqual(
            bmp.get_percentage_grade_for_mineral_from_gold_proportion("w23_test",
                                                                      13, 17, 41,
                                                                      au_fa_column_name,
                                                                      TEST_DB_NAME), False)


if __name__ == "__main__":
    unittest.main()
