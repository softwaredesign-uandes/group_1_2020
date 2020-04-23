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
        self.assertEqual(lbm.get_model_name_from_path("some/text/before-the/name.name"), "name")

    def test_retrieve_columns_types_valid_types(self):
        column_types = ["INT", "INT", "INT", "INT", "FLOAT", "INT", "FLOAT"]
        self.assertEqual(lbm.retrieve_columns_types(test_block_file_path), column_types)


    # TODO: Test load block file with an inexistent model return true
    #def test_load_block_file_return_true(self):
    #    self.assertEqual(lbm.load_block_file(test_block_file_path,))

    # TODO: Test load block file with an existent model return false

if __name__ == "__main__":
    unittest.main()
