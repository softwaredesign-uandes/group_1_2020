import block_model_proccesor
import unittest
import tabulate
from block_model import BlockModel
from block import Block

test_model_name = "mclaughlin_test"
test_db_name = "block_model_test.db"
mclaughlin_columns = ['id', 'x', 'y', 'z', 'blockvalue', 'ton', 'destination', 'au']
mclaughlin_minerals = {"au": "oz_per_ton"}
mclaughlin_block_model_test = BlockModel("mclaughlin_limit", [Block({'id': 0,
                                                                     'x': 31,
                                                                     'y': 208,
                                                                     'z': 44,
                                                                     'blockvalue': -646,
                                                                     'ton': 489.58,
                                                                     'destination': 0,
                                                                     'au': 0.038})], mclaughlin_columns,
                                         mclaughlin_minerals)
zuck_columns = ['id', 'x', 'y', 'z', 'cost', 'value', 'rock_tonnes', 'ore_tonnes']
zuck_minerals = {"cu": "cu_proportion"}
zuck_block_model_test = BlockModel("mclaughlin_limit", [Block({'id': 12437,
                                                               'x': 23,
                                                               'y': 33,
                                                               'z': 7,
                                                               'cost': 28042.4250000000,
                                                               'value': 196860.6750000000,
                                                               'rock_tonnes': 5487.7500000000,
                                                               'ore_tonnes': 14634})], zuck_columns, zuck_minerals)
p4hd_columns = ['id', 'x', 'y', 'z', 'tonn', 'blockvalue', 'destination', 'Au', 'ag', 'Cu']
p4hd_minerals = {"au": "oz_per_ton", "ag": "oz_per_ton", "cu": "percentage"}
p4hd_block_model_test = BlockModel("mclaughlin_limit", [Block({'id': 234,
                                                               'x': 53,
                                                               'y': 19,
                                                               'z': 63,
                                                               'tonn': 4258.8,
                                                               'blockvalue': 38859,
                                                               'destination': 1,
                                                               'au': 0.027,
                                                               'ag': 1.182,
                                                               'cu': 0.163})], p4hd_columns, p4hd_minerals)
w23_columns = ['id', 'x', 'y', 'z', 'dest', 'phase', 'AuRec', 'AuFa', 'tons', 'co3', 'orgc', 'sulf',
               'Mcost', 'Pcost', 'Tcost', 'Tvalue', 'Bvalue', 'rc_Stockpile', 'rc_RockChar']
w23_block = Block({'id': 9229, 'x': 58, 'y': 50, 'z': 18, 'dest': 1, 'phase': 3, 'AuRec': 0.94, 'AuFa': 0.09787,
                   'tons': 2406.01492, 'co3': 2.1, 'orgc': 0.1, 'sulf': 6.5, 'Mcost': 2.11, 'Pcost': 28.28,
                   'Tcost': 0.18, 'Tvalue': 52.228, 'Bvalue': 125661, 'rc_Stockpile': 3, 'rc_RockChar': 'hsf'})
w23_minerals = {"au": "au_proportion"}
w23_block_model_test = BlockModel("w23", [w23_block], w23_columns, w23_minerals)


class TestBlockModelProcessor(unittest.TestCase):
    def test_get_model_data_table_returns_correct_rows(self):
        rows = [
            [0, 31, 208, 44, -646, 489.58, 0, 0.038]
        ]
        self.assertEqual(block_model_proccesor.get_model_data_table(mclaughlin_block_model_test,
                                                                    0,
                                                                    1), rows)

    def test_get_number_of_blocks_in_model_return_correct_number(self):
        self.assertEqual(mclaughlin_block_model_test.get_number_of_blocks(), 1)

    def test_get_mass_in_kilograms_with_correct_information_return_correct_number(self):
        self.assertEqual(block_model_proccesor.get_mass_in_kilograms(mclaughlin_block_model_test,
                                                                     31, 208, 44,
                                                                     "ton"), 489580)

    def test_get_mass_in_kilograms_with_wrong_coordinates_return_false(self):
        self.assertEqual(block_model_proccesor.get_mass_in_kilograms(mclaughlin_block_model_test,
                                                                     1, 2, 3,
                                                                     "ton"), False)

    def test_get_tabulated_blocks_with_mclaughlin_test_return_correct_information(self):
        rows = [
            ["id", "x", "y", "z", "blockvalue", "ton", "destination", "au"],
            ["__", "_", "_", "_", "__________", "___", "___________", "__"],
            [0, 31, 208, 44, -646, 489.58, 0, 0.038]
        ]
        rows = tabulate.tabulate(rows)
        self.assertEqual(
            block_model_proccesor.get_tabulated_blocks(mclaughlin_block_model_test, 0, 1),
            rows)

    def test_get_attribute_from_block_return_correct_result(self):
        self.assertEqual(block_model_proccesor.get_attribute_from_block(mclaughlin_block_model_test,
                                                                        31, 208, 44,
                                                                        "blockvalue"), -646)

    def test_get_attribute_from_block_wrong_coordinates_return_false(self):
        self.assertFalse(block_model_proccesor.get_attribute_from_block(mclaughlin_block_model_test,
                                                                        0, 0, 0,
                                                                        "blockvalue"), False)

    def test_get_percentage_grade_for_mineral_from_copper_proportion_return_true(self):
        self.assertEqual(
            block_model_proccesor.get_percentage_grade_for_mineral_from_copper_proportion(zuck_block_model_test,
                                                                                          23, 33, 7,
                                                                                          'rock_tonnes',
                                                                                          'ore_tonnes'), 72.727)

    def test_get_percentage_grade_for_mineral_from_copper_proportion_return_false_with_wrong_coordinates(self):
        self.assertEqual(
            block_model_proccesor.get_percentage_grade_for_mineral_from_copper_proportion(zuck_block_model_test,
                                                                                          0, 1, 2,
                                                                                          'rock_tonnes',
                                                                                          'ore_tonnes'), False)

    def test_get_percentage_grade_for_mineral_from_different_unit_return_correct_result(self):
        self.assertEqual(block_model_proccesor.
                         get_percentage_grade_for_mineral_from_different_unit(p4hd_block_model_test,
                                                                              53, 19, 63,
                                                                              "ag"), 0.004053)

    def test_get_percentage_grade_for_mineral_from_different_unit_return_None_with_wrong_coordinates(self):
        self.assertEqual(
            block_model_proccesor.get_percentage_grade_for_mineral_from_different_unit(p4hd_block_model_test,
                                                                                       0, 38, 47,
                                                                                       "au"), None)

    def test_get_percentage_grade_for_mineral_from_gold_proportion_return_true(self):
        self.assertEqual(
            block_model_proccesor.get_percentage_grade_for_mineral_from_gold_proportion(w23_block_model_test,
                                                                                        58, 50, 18,
                                                                                        'AuFa'), 9.787)

    def test_get_percentage_grade_for_mineral_from_gold_proportion_with_wrongs_coordinates(self):

        self.assertEqual(
            block_model_proccesor.get_percentage_grade_for_mineral_from_gold_proportion(w23_block_model_test,
                                                                                        13, 17, 41,
                                                                                        'AuFa'), False)


if __name__ == "__main__":
    unittest.main()
