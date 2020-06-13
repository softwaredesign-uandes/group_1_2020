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
    errors = 0

    block_model_processor_tester = unittest.TestLoader().loadTestsFromModule(block_model_processor_tests)
    block_model_processor_tests_run = unittest.TextTestRunner(verbosity=2).run(block_model_processor_tester)
    failures += len(block_model_processor_tests_run.failures)
    errors += len(block_model_processor_tests_run.errors)

    load_block_model_tester = unittest.TestLoader().loadTestsFromModule(load_block_model_tests)
    load_block_model_tests_run = unittest.TextTestRunner(verbosity=2).run(load_block_model_tester)
    failures += len(load_block_model_tests_run.failures)
    errors += len(load_block_model_tests_run.errors)

    block_model_tester = unittest.TestLoader().loadTestsFromModule(block_model_tests)
    block_model_tests_run = unittest.TextTestRunner(verbosity=2).run(block_model_tester)
    failures += len(block_model_tests_run.failures)
    errors += len(block_model_tests_run.errors)

    api_tester = unittest.TestLoader().loadTestsFromModule(api_tests)
    api_tests_run = unittest.TextTestRunner(verbosity=2).run(api_tester)
    failures += len(api_tests_run.failures)
    errors += len(api_tests_run.errors)

    delete_test_files()
    #If there are errors or fail in tests, tests exits with code 1 (error)
    if failures > 0 or errors > 0:
        print("Failures:", failures)
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()
