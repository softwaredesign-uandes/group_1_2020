import unittest
from block_model import BlockModel
from block import Block


class TestBlockModel(unittest.TestCase):

    def test_get_number_of_blocks_return_correct(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 22, 'au': 0.0, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 1, 'z': 1, 'ton': 34, 'au': 0.0, 'destination': 0}),
            Block({'id': 2, 'x': 2, 'y': 2, 'z': 2, 'ton': 0, 'au': 0.0, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 3, 'z': 3, 'ton': 46, 'au': 0.0, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "proportion"}
        test_block_model_name = "test_block_model"
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        self.assertEqual(test_block_model.get_number_of_blocks(), 4)

    def test_get_column_names_return_correct(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 22, 'au': 0.0, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 1, 'z': 1, 'ton': 34, 'au': 0.0, 'destination': 0}),
            Block({'id': 2, 'x': 2, 'y': 2, 'z': 2, 'ton': 0, 'au': 0.0, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 3, 'z': 3, 'ton': 46, 'au': 0.0, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "proportion"}
        test_block_model_name = "test_block_model"
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        self.assertEqual(test_block_model.get_column_names(), test_columns)

    def test_et_block_by_coordinates_return_correct(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 22, 'au': 0.0, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 1, 'z': 1, 'ton': 34, 'au': 0.0, 'destination': 0}),
            Block({'id': 2, 'x': 2, 'y': 2, 'z': 2, 'ton': 0, 'au': 0.0, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 3, 'z': 3, 'ton': 46, 'au': 0.0, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "proportion"}
        test_block_model_name = "test_block_model"
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        self.assertEqual(test_block_model.get_block_by_coordinates(0, 0, 0),
                         Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 22, 'au': 0.0, 'destination': 0}))

    def test_reblock_for_continuous_attributes_return_correct(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 22, 'au': 0.0, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 1, 'z': 1, 'ton': 34, 'au': 0.0, 'destination': 0}),
            Block({'id': 2, 'x': 2, 'y': 2, 'z': 2, 'ton': 0, 'au': 0.0, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 3, 'z': 3, 'ton': 46, 'au': 0.0, 'destination': 1})
                  ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "proportion"}
        test_block_model_name = "test_block_model"
        test_mass_columns = ["ton"]
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "proportion"}
        test_categorical_attributes = ["destination"]
        reblocked_test_model = BlockModel("reblocked_contnuous_test", [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 56, 'au': 0.0, 'destination': 0}),
            Block({'id': 1, 'x': 0, 'y': 0, 'z': 1, 'ton': 0, 'au': 0.0, 'destination': 0}),
            Block({'id': 2, 'x': 0, 'y': 1, 'z': 0, 'ton': 0, 'au': 0.0, 'destination': 0}),
            Block({'id': 3, 'x': 0, 'y': 1, 'z': 1, 'ton': 0, 'au': 0.0, 'destination': 0}),
            Block({'id': 4, 'x': 1, 'y': 0, 'z': 0, 'ton': 0, 'au': 0.0, 'destination': 0}),
            Block({'id': 5, 'x': 1, 'y': 0, 'z': 1, 'ton': 0, 'au': 0.0, 'destination': 0}),
            Block({'id': 6, 'x': 1, 'y': 1, 'z': 0, 'ton': 0, 'au': 0.0, 'destination': 0}),
            Block({'id': 7, 'x': 1, 'y': 1, 'z': 1, 'ton': 46, 'au': 0.0, 'destination': 0})],
                                          test_columns, test_minerals)
        self.assertEqual(reblocked_test_model, test_block_model.reblock(
            2, 2, 2, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes, test_mass_columns))

    def test_reblock_for_proportional_attributes_return_correct(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 30, 'au': 0.30, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 0, 'z': 0, 'ton': 20, 'au': 0.20, 'destination': 0}),
            Block({'id': 2, 'x': 2, 'y': 0, 'z': 0, 'ton': 10, 'au': 0.05, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 0, 'z': 0, 'ton': 40, 'au': 0.01, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "proportion"}
        test_block_model_name = "test_block_model"
        test_mass_columns = ["ton"]
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "proportion"}
        test_categorical_attributes = ["destination"]
        reblocked_test = test_block_model.reblock(
            4, 1, 1, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes, test_mass_columns)
        result_of_calculation = reblocked_test.get_blocks_range(0, 1)[0].get_attribute_value("au")
        self.assertEqual(result_of_calculation, 13.9)

    def test_reblock_for_oz_per_ton_attribute_return_correct(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 30, 'au': 0.30, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 0, 'z': 0, 'ton': 20, 'au': 0.20, 'destination': 0}),
            Block({'id': 2, 'x': 2, 'y': 0, 'z': 0, 'ton': 10, 'au': 0.10, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 0, 'z': 0, 'ton': 40, 'au': 0.40, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "oz_per_ton"}
        test_block_model_name = "test_block_model"
        test_mass_columns = ["ton"]
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "oz_per_ton"}
        test_categorical_attributes = ["destination"]
        reblocked_test = test_block_model.reblock(
            4, 1, 1, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes,
            test_mass_columns)
        result_of_calculation = reblocked_test.get_blocks_range(0, 1)[0].get_attribute_value("au")
        self.assertEqual(result_of_calculation, 0.001028559)

    def test_reblock_for_ppm_attributes_return_correct(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 30, 'au': 30, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 0, 'z': 0, 'ton': 20, 'au': 10, 'destination': 0}),
            Block({'id': 2, 'x': 2, 'y': 0, 'z': 0, 'ton': 10, 'au': 20, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 0, 'z': 0, 'ton': 40, 'au': 10, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "ppm"}
        test_block_model_name = "test_block_model"
        test_mass_columns = ["ton"]
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "ppm"}
        test_categorical_attributes = ["destination"]
        reblocked_test = test_block_model.reblock(
            4, 1, 1, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes, test_mass_columns)
        result_of_calculation = reblocked_test.get_blocks_range(0, 1)[0].get_attribute_value("au")
        self.assertEqual(result_of_calculation, 0.0017000000000000001)

    def test_reblock_for_categorical_attributes_return_correct(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 30, 'au': 30, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 0, 'z': 0, 'ton': 20, 'au': 10, 'destination': 1}),
            Block({'id': 2, 'x': 2, 'y': 0, 'z': 0, 'ton': 10, 'au': 20, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 0, 'z': 0, 'ton': 40, 'au': 10, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "ppm"}
        test_block_model_name = "test_block_model"
        test_mass_columns = ["ton"]
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "ppm"}
        test_categorical_attributes = ["destination"]
        reblocked_test = test_block_model.reblock(
            4, 1, 1, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes, test_mass_columns)
        result_of_calculation = reblocked_test.get_blocks_range(0, 1)[0].get_attribute_value("destination")
        self.assertEqual(result_of_calculation, 1)

    def test_reblock_with_rx_zero_return_false(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 30, 'au': 30, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 0, 'z': 0, 'ton': 20, 'au': 10, 'destination': 1}),
            Block({'id': 2, 'x': 2, 'y': 0, 'z': 0, 'ton': 10, 'au': 20, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 0, 'z': 0, 'ton': 40, 'au': 10, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "ppm"}
        test_block_model_name = "test_block_model"
        test_mass_columns = ["ton"]
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "ppm"}
        test_categorical_attributes = ["destination"]
        reblocked_test_rx = test_block_model.reblock(
            0, 1, 1, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes,
            test_mass_columns)
        self.assertFalse(reblocked_test_rx)

    def test_reblock_with_ry_zero_return_false(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 30, 'au': 30, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 0, 'z': 0, 'ton': 20, 'au': 10, 'destination': 1}),
            Block({'id': 2, 'x': 2, 'y': 0, 'z': 0, 'ton': 10, 'au': 20, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 0, 'z': 0, 'ton': 40, 'au': 10, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "ppm"}
        test_block_model_name = "test_block_model"
        test_mass_columns = ["ton"]
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "ppm"}
        test_categorical_attributes = ["destination"]
        reblocked_test_ry = test_block_model.reblock(
            1, 0, 1, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes,
            test_mass_columns)
        self.assertFalse(reblocked_test_ry)

    def test_reblock_with_rz_zero_return_false(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 30, 'au': 30, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 0, 'z': 0, 'ton': 20, 'au': 10, 'destination': 1}),
            Block({'id': 2, 'x': 2, 'y': 0, 'z': 0, 'ton': 10, 'au': 20, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 0, 'z': 0, 'ton': 40, 'au': 10, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "ppm"}
        test_block_model_name = "test_block_model"
        test_mass_columns = ["ton"]
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "ppm"}
        test_categorical_attributes = ["destination"]
        reblocked_test_rz = test_block_model.reblock(
            1, 1, 0, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes,
            test_mass_columns)
        self.assertFalse(reblocked_test_rz)

    def test_reblock_with_larger_than_model_parameters_return_model_reblocked(self):
        test_blocks = [
            Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 30, 'au': 30, 'destination': 0}),
            Block({'id': 1, 'x': 1, 'y': 0, 'z': 0, 'ton': 20, 'au': 10, 'destination': 1}),
            Block({'id': 2, 'x': 2, 'y': 0, 'z': 0, 'ton': 10, 'au': 20, 'destination': 1}),
            Block({'id': 3, 'x': 3, 'y': 0, 'z': 0, 'ton': 40, 'au': 10, 'destination': 1})
        ]
        test_columns = ["id", "x", "y", "z", "ton", "au", "destination"]
        test_minerals = {"au": "proportion"}
        test_block_model_name = "test_block_model"
        test_mass_columns = ["ton"]
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "ppm"}
        test_categorical_attributes = ["destination"]
        reblocked_test = test_block_model.reblock(
            30, 30, 30, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes,
            test_mass_columns)
        reblocked_result = BlockModel("test_block_model_reblocked_30_30_30",
                                      [Block({'id': 0, 'x': 0, 'y': 0, 'z': 0, 'ton': 100, 'au': 0.0017000000000000001, 'destination': 0})],
                                      ['id', 'x', 'y', 'z', 'ton', 'au', 'destination'],
                                      {'au': 'proportion'})
        self.assertEqual(reblocked_test, reblocked_result)

    def test_reblock_with_factors_that_matches_the_dimensions_of_the_block_model_return_one_block(self):
        test_block_attributes = []
        test_id = 0
        for i in range(5, 21, 3):
            for j in range(1, 17, 2):
                for k in range(0, 13, 2):
                    test_block_attributes.append({"id": test_id, "x": i, "y": j, "z": k, "ton": i + j + k,
                                                  "au": i * j, "ag": j * k, "cu": k * i, "destination": test_id % 2})
                    test_id += 1
        test_blocks = [Block(test_block_attributes[n]) for n in range(test_id)]
        test_columns = ["id", "x", "y", "z", "ton", "au", "ag", "cu", "destination"]
        test_minerals = {"au": "proportion", "ag": "oz_per_ton", "cu": "ppm"}
        test_block_model_name = "test_block_model"
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        rx, ry, rz = 16, 16, 13
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "proportion", "ag": "oz_per_ton", "cu": "ppm"}
        test_categorical_attributes = ["destination"]
        test_mass_column = ["ton"]
        test_reblocked = BlockModel("test_block_model_reblocked_16_16_13", [Block(
            {'id': 0, 'x': 5, 'y': 1, 'z': 0, 'ton': 8904, 'au': 11783.018867924528, 'ag': 0.19743157660377347,
             'cu': 0.008849056603773586, 'destination': 0})],
                                    ['id', 'x', 'y', 'z', 'ton', 'au', 'ag', 'cu', 'destination'],
                                    {'au': 'proportion', 'ag': 'oz_per_ton', 'cu': 'ppm'})
        # print(test_block_model.reblock(rx, ry, rz, test_continuous_attributes, test_proportional_attributes,
        #                                           test_categorical_attributes, test_mass_column))
        self.assertEqual(test_block_model.reblock(rx, ry, rz, test_continuous_attributes, test_proportional_attributes,
                                                  test_categorical_attributes, test_mass_column), test_reblocked)

    def test_reblock_with_factors_of_zero_return_false(self):
        test_block_attributes = []
        test_id = 0
        for i in range(3, 17, 2):
            for j in range(0, 12, 2):
                for k in range(1, 14, 3):
                    test_block_attributes.append({"id": test_id, "x": i, "y": j, "z": k, "ton": i + j + k,
                                                  "au": i * j, "ag": j * k, "cu": k * i, "destination": test_id % 2})
                    test_id += 1
        test_blocks = [Block(test_block_attributes[n]) for n in range(test_id)]
        test_columns = ["id", "x", "y", "z", "ton", "au", "ag", "cu", "destination"]
        test_minerals = {"au": "proportion", "ag": "oz_per_ton", "cu": "ppm"}
        test_block_model_name = "test_block_model"
        test_block_model = BlockModel(test_block_model_name, test_blocks, test_columns, test_minerals)
        rx, ry, rz = 0, 0, 0
        test_continuous_attributes = ["ton"]
        test_proportional_attributes = {"au": "proportion", "ag": "oz_per_ton", "cu": "ppm"}
        test_categorical_attributes = ["destination"]
        test_mass_column = ["ton"]
        self.assertEqual(test_block_model.reblock(rx, ry, rz, test_continuous_attributes, test_proportional_attributes,
                                                  test_categorical_attributes, test_mass_column), False)


if __name__ == "__main__":
    unittest.main()
