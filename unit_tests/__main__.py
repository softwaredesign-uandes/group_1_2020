import sys
import load_block_model
import json
import os
import unittest
import block_model_processor_tests
import load_block_model_tests
import block_model_tests
import api_tests

from constants import TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME


def check_necessary_files_existence_for_tests():
    if not os.path.isfile(TEST_LOADED_MODELS_INFORMATION_FILE_NAME):
        with open(TEST_LOADED_MODELS_INFORMATION_FILE_NAME, "w+") as f:
            json.dump({}, f, sort_keys=True)
    if not os.path.isfile(TEST_DB_NAME):
        load_block_model.create_db(TEST_DB_NAME)
    if not os.path.isfile(TEST_MINERAL_GRADES_INFORMATION_FILE_NAME):
        with open(TEST_MINERAL_GRADES_INFORMATION_FILE_NAME, "w+") as f:
            json.dump({}, f, sort_keys=True)

def delete_test_files():
    os.remove(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)
    os.remove(TEST_DB_NAME)
    os.remove(TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    print("Running tests")
    check_necessary_files_existence_for_tests()
    failures = 0
    block_model_processor_tester = unittest.TestLoader().loadTestsFromModule(block_model_processor_tests)
    failures += len(unittest.TextTestRunner(verbosity=2).run(block_model_processor_tester).failures)
    load_block_model_tester = unittest.TestLoader().loadTestsFromModule(load_block_model_tests)
    failures += len(unittest.TextTestRunner(verbosity=2).run(load_block_model_tester).failures)
    block_model_tester = unittest.TestLoader().loadTestsFromModule(block_model_tests)
    failures += len(unittest.TextTestRunner(verbosity=2).run(block_model_tester).failures)
    api_tester = unittest.TestLoader().loadTestsFromModule(api_tests)
    failures += len(unittest.TextTestRunner(verbosity=2).run(api_tester).failures)

    delete_test_files()
    if failures > 0:
        print("Failures:", failures)
        exit(1)

if __name__ == "__main__":
    main()
