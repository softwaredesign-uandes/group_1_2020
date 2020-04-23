import sys
import block_model_proccesor
import load_block_model
import json
import os
import unittest
import block_model_processor_tests
import load_block_model_tests

from constants import TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME


def check_necessary_files_existence_for_tests():
    if not os.path.isfile(TEST_LOADED_MODELS_INFORMATION_FILE_NAME):
        with open(TEST_LOADED_MODELS_INFORMATION_FILE_NAME, "w+") as f:
            json.dump({}, f, sort_keys=True)
    if not os.path.isfile(TEST_DB_NAME):
        load_block_model.create_db(TEST_DB_NAME)

def fill_test_bd():
    local_path = os.getcwd() + "\\"
    file_names = [local_path + "mclaughlin_test.blocks", local_path + "w23_test.blocks", local_path + "zuck_medium_test.blocks", local_path + "p4hd_test.blocks"]
    column_names = [['id', 'x', 'y', 'z', 'blockvalue', 'ton', 'destination', 'Au'],
                    ['id', 'x', 'y', 'z', 'dest', 'phase', 'AuRec', 'AuFa', 'tons', 'co3', 'orgc', 'sulf', 'Mcost', 'Pcost', 'Tcost', 'Tvalue', 'Bvalue', 'rc_Stockpile', 'rc_RockChar'],
                    ['id', 'x', 'y', 'z', 'cost', 'value', 'rock_tonnes', 'ore_tonnes'],
                    ['id', 'x', 'y', 'z', 'tonn', 'blockvalue', 'destination', 'Au', 'ag', 'Cu']]
    for i in range(len(file_names)):
        load_block_model.load_block_file(file_names[i], column_names[i], TEST_DB_NAME, TEST_LOADED_MODELS_INFORMATION_FILE_NAME)

def delete_test_files():
    os.remove(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)
    os.remove("block_model_test.db")

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    print("Running tests")
    check_necessary_files_existence_for_tests()
    fill_test_bd()
    block_model_processor_tester = unittest.TestLoader().loadTestsFromModule(block_model_processor_tests)
    unittest.TextTestRunner(verbosity=2).run(block_model_processor_tester)
    #load_block_model_tester = unittest.TestLoader().loadTestsFromModule(load_block_model_tests)
    #unittest.TextTestRunner(verbosity=2).run(load_block_model_tester)
    print("Done testing")
    #delete_test_files()

if __name__ == "__main__":
    main()