import unittest
from block import Block
from block_group import BlockGroup

class TestBlockGroup(unittest.TestCase):

    def test_convert_to_block_only_with_continuous_attributes_return_correct(self):
        list_of_blocks = []
        iterator_id = 0
        for i in range(3):
            for j in range(2):
                for k in range(4):
                    list_of_blocks.append(Block(
                        {'id': iterator_id, 'x': i + 4, 'y': j + 2, 'z': k + 7, 'ore_tonnes': i * k * k * 15,
                         "blockvalue": (i + 2) * (j + 1) * (k + 7) * 41 * (-1 if (i * k) % 2 else 1)}))
                    iterator_id += 1
        rx = 3
        ry = 2
        rz = 4
        x_offset = 1
        y_offset = 0
        z_offset = 3
        new_id = 1
        mass_columns = ["ore_tonnes"]
        test_block_group = BlockGroup(list_of_blocks, x_offset, y_offset, z_offset, new_id, mass_columns, rx, ry, rz)
        continuous_attributes = ["ore_tonnes", "blockvalue"]
        proportional_attributes = {}
        categorical_attributes = []
        test_new_block = Block({'id': 1, 'x': 2, 'y': 1, 'z': 4, 'ore_tonnes': 1260, "blockvalue": 24354})
        self.assertEqual(test_block_group.convert_to_block(continuous_attributes, proportional_attributes, categorical_attributes), test_new_block)

    def test_convert_to_block_only_with_categorical_attributes_return_correct(self):
        list_of_blocks = []
        iterator_id = 0
        for i in range(3):
            for j in range(2):
                for k in range(4):
                    list_of_blocks.append(Block(
                        {'id': iterator_id, 'x': i + 4, 'y': j + 2, 'z': k + 7, "tonn": 0,
                         'destination': (i + 1 * j + 1 * k + 1) % 5, "type": "OXOR" if (i + j * k) % 2 else "FRWS"}))
                    iterator_id += 1
        rx = 3
        ry = 2
        rz = 4
        x_offset = 1
        y_offset = 0
        z_offset = 3
        new_id = 1
        mass_columns = ["tonn"]
        test_block_group = BlockGroup(list_of_blocks, x_offset, y_offset, z_offset, new_id, mass_columns, rx, ry, rz)
        categorical_attributes = ["destination", "type"]
        proportional_attributes = {}
        continuous_attributes = ["tonn"]
        test_new_block = Block({'id': 1, 'x': 2, 'y': 1, 'z': 4, "tonn": 0, 'destination': 4, "type": "FRWS"})
        self.assertEqual(
            test_block_group.convert_to_block(continuous_attributes, proportional_attributes, categorical_attributes),
            test_new_block)

    def test_convert_to_block_only_with_proportional_attributes_with_percentage_unit_return_correct(self):
        list_of_blocks = []
        iterator_id = 0
        for i in range(3):
            for j in range(2):
                for k in range(4):
                    list_of_blocks.append(Block(
                        {'id': iterator_id, 'x': i + 4, 'y': j + 2, 'z': k + 7, 'tonnes': (i + 1 * j + 1 * k + 1) * 5,
                         "cu": round((i + 2 * j + 5 * k + 3) / 0.3, 2)}))
                    iterator_id += 1
        rx = 3
        ry = 2
        rz = 4
        x_offset = 1
        y_offset = 0
        z_offset = 3
        new_id = 1
        mass_columns = ["tonnes"]
        test_block_group = BlockGroup(list_of_blocks, x_offset, y_offset, z_offset, new_id, mass_columns, rx, ry, rz)
        proportional_attributes = {"cu": "percentage"}
        continuous_attributes = ["tonnes"]
        categorical_attributes = []
        test_new_block = Block({'id': 1, 'x': 2, 'y': 1, 'z': 4, "tonnes": 480, "cu": 47.84718749999999})
        self.assertEqual(
            test_block_group.convert_to_block(continuous_attributes, proportional_attributes, categorical_attributes),
            test_new_block)

    def test_convert_to_block_only_with_proportional_attributes_with_ppm_unit_return_correct(self):
        list_of_blocks = []
        iterator_id = 0
        for i in range(3):
            for j in range(2):
                for k in range(4):
                    list_of_blocks.append(Block(
                        {'id': iterator_id, 'x': i + 4, 'y': j + 2, 'z': k + 7, 'ton': (i + 1 * j + 1 * k + 1) * 12345,
                         "au": round((i + 3 * j + 6 * k + 2) / 21.893, 4)}))
                    iterator_id += 1
        rx = 3
        ry = 2
        rz = 4
        x_offset = 1
        y_offset = 0
        z_offset = 3
        new_id = 1
        mass_columns = ["ton"]
        test_block_group = BlockGroup(list_of_blocks, x_offset, y_offset, z_offset, new_id, mass_columns, rx, ry, rz)
        proportional_attributes = {"au": "ppm"}
        continuous_attributes = ["ton"]
        categorical_attributes = []
        test_new_block = Block({'id': 1, 'x': 2, 'y': 1, 'z': 4, "ton": 1185120, "au": 7.184572916666666 * (10**-5)})
        self.assertEqual(
            test_block_group.convert_to_block(continuous_attributes, proportional_attributes, categorical_attributes),
            test_new_block)

    def test_convert_to_block_only_with_proportional_attributes_with_oz_per_ton_unit_return_correct(self):
        list_of_blocks = []
        iterator_id = 0
        for i in range(3):
            for j in range(2):
                for k in range(4):
                    list_of_blocks.append(Block(
                        {'id': iterator_id, 'x': i + 4, 'y': j + 2, 'z': k + 7, 'tonn': (i + 2 * j + 2 * k + 2) * 813,
                         "ag": round((i + 7 * j + 4 * k + 5) / 13, 4)}))
                    iterator_id += 1
        rx = 3
        ry = 2
        rz = 4
        x_offset = 1
        y_offset = 0
        z_offset = 3
        new_id = 1
        mass_columns = ["tonn"]
        test_block_group = BlockGroup(list_of_blocks, x_offset, y_offset, z_offset, new_id, mass_columns, rx, ry, rz)
        proportional_attributes = {"ag": "oz_per_ton"}
        continuous_attributes = ["tonn"]
        categorical_attributes = []
        test_new_block = Block({'id': 1, 'x': 2, 'y': 1, 'z': 4, "tonn": 136584, "ag": 0.004621613542583333})
        self.assertEqual(
            test_block_group.convert_to_block(continuous_attributes, proportional_attributes, categorical_attributes),
            test_new_block)

    def test_convert_to_block_only_with_proportional_attributes_with_proportional_unit_return_correct(self):
        list_of_blocks = []
        iterator_id = 0
        for i in range(3):
            for j in range(2):
                for k in range(4):
                    list_of_blocks.append(Block(
                        {'id': iterator_id, 'x': i + 4, 'y': j + 2, 'z': k + 7, 'tonnes': (i + 2 * j + 2 * k + 2) * 309,
                         "au": round((i + 7 * j + 10 * k + 5) / 112, 4)}))
                    iterator_id += 1
        rx = 3
        ry = 2
        rz = 4
        x_offset = 1
        y_offset = 0
        z_offset = 3
        new_id = 1
        mass_columns = ["tonnes"]
        test_block_group = BlockGroup(list_of_blocks, x_offset, y_offset, z_offset, new_id, mass_columns, rx, ry, rz)
        proportional_attributes = {"au": "proportion"}
        continuous_attributes = ["tonnes"]
        categorical_attributes = []
        test_new_block = Block({'id': 1, 'x': 2, 'y': 1, 'z': 4, "tonnes": 51912, "au": 25.595476190476187})
        self.assertEqual(
            test_block_group.convert_to_block(continuous_attributes, proportional_attributes, categorical_attributes),
            test_new_block)


if __name__ == "__main__":
    unittest.main()