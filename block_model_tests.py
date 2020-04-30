import unittest
from block_model import BlockModel
from block import Block

test_block_attributes = []
test_id = 0
test_x_length = 5 # 1 2 3 4 5                                         # 0 2 4 ## 1     3    # 5
test_y_length = 7 # 2 4 6       ## 3     5    # 7
test_z_length = 8 # 1 4 7       ## 2 3   5 6  # 8 9
for i in range(1, test_x_length):
    for j in range(2, test_y_length, 2):
        for k in range(1, test_z_length, 3):
            test_block_attributes.append({"id": test_id, "x": i, "y": j, "z": k, "ton": i + j + k,
                                          "au": i * j, "ag": j * k, "cu": k * i, "destination": test_id % 2})
            test_id += 1

print(test_id)
test_blocks = [Block(test_block_attributes[n]) for n in range(test_id)]
test_columns = ["id", "x", "y", "z", "ton", "au", "ag", "cu", "destination"]
test_minerals = {"au": "proportion", "ag": "oz_per_ton", "cu": "ppm"}
test_block_model = BlockModel("test_block_model", test_blocks, test_columns, test_minerals)

rx, ry, rz = 2, 2, 3
test_continuous_attributes = ["ton"]
test_proportional_attributes = {"au": "proportion", "ag": "oz_per_ton", "cu": "ppm"}
test_categorical_attributes = ["destination"]
test_mass_column = ["ton"]

reblocked = test_block_model.reblock(rx, ry, rz, test_continuous_attributes, test_proportional_attributes, test_categorical_attributes, test_mass_column)
print(reblocked)
print(len(reblocked.blocks))

#test_reblocked = BlockModel("test_block_model_reblocked_2_2_1", [Block({'id': 0, 'x': 1, 'y': 2, 'z': 0, 'ton': 4, 'destination': 0}), Block({'id': 1, 'x': 1, 'y': 2, 'z': 0, 'ton': 5, 'destination': 0})], ['id', 'x', 'y', 'z', 'ton', 'au', 'ag', 'cu', 'destination'], {'au': 'proportion', 'ag': 'oz_per_ton', 'cu': 'ppm'})

# class TestBlockModel(unittest.TestCase):
#     # def test_get_block_by_coordinates(self):
#     #     self.assertEqual(test_block_model.get_block_by_coordinates(1, 0, 1),
#     #                      Block({"id": 4, "x": 1, "y": 0, "z": 1, "ton": 2,
#     #                             "au": 0, "ag": 0, "cu": 1, "destination": 0}))
#     def test_reblock(self):
#         self.assertEqual(test_block_model.reblock(rx, ry, rz, test_continuous_attributes, test_proportional_attributes,
#                                                   test_categorical_attributes, test_mass_column), test_reblocked)
