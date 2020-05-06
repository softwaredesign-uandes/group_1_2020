from block import Block
import unittest

test_block = Block({'id': 0, 'x': 1, 'y': 0, 'z': 4, 'ton': 5, 'au': 0.0, 'ag': 0.0, 'cu': 0.0004, 'destination': 0})

class TestBlock(unittest.TestCase):

    def test_get_attribute_value_return_correct_value(self):
        self.assertEqual(test_block.get_attribute_value('cu'), 0.0004)
        self.assertEqual(test_block.get_attribute_value('ton'), 5)

    def test_get_attribute_value_with_incorrect_attribute_return_false(self):
        self.assertFalse(test_block.get_attribute_value('not_an_attribute'))
        self.assertFalse(test_block.get_attribute_value('tonne'))
        self.assertFalse(test_block.get_attribute_value('Au'))


if __name__ == '__main__':
    unittest.main()
