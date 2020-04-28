import sys
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


def delete_test_files():
    os.remove(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)
    os.remove("block_model_test.db")


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    print("Running tests")
    check_necessary_files_existence_for_tests()
    block_model_processor_tester = unittest.TestLoader().loadTestsFromModule(block_model_processor_tests)
    unittest.TextTestRunner(verbosity=2).run(block_model_processor_tester)
    load_block_model_tester = unittest.TestLoader().loadTestsFromModule(load_block_model_tests)
    unittest.TextTestRunner(verbosity=2).run(load_block_model_tester)
    print("Done testing")
    delete_test_files()


if __name__ == "__main__":
    main()
