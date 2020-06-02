import unittest, json
from api import __main__ as api_main
import block_model_proccesor

class TestApi(unittest.TestCase):
    def test_get_block_models_names_return_ok_status_code(self):
        self.assertEqual(api_main.get_block_models_names().status_code, 200)

    def test_get_block_model_blocks_return_ok_status_code(self):
        self.assertEqual(api_main.get_block_model_blocks().status_code, 200)

    def test_get_block_models_names_return_correct(self):
        self.assertEqual(block_model_proccesor.get_model_names_to_dictionary(), json.loads(api_main.get_block_models_names().data))
        
    def test_get_block_model_blocks_return_correct(self):
        first_block_model_name = block_model_proccesor.get_model_names_to_dictionary()[0]['name']
        self.assertEqual(block_model_proccesor.get_block_list(first_block_model_name), json.loads(api_main.get_block_model_blocks(first_block_model_name).data))
