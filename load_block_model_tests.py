import unittest
import load_block_model as lbm

class TestLoadBlockModel(unittest.TestCase):
    def test_check_exists_bd_return_true(self):
        self.assertEqual(lbm.db_exists("block_model.db"), True)

    def test_check_exists_bd_return_false(self):
        self.assertEqual(lbm.db_exists("line_model.db"), False)

    # def test_