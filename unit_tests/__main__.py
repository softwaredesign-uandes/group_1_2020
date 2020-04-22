import sys
import block_model_proccesor
import load_block_model
import json
import os

from constants import TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_JSON_INFO


def check_neccesary_files_existence_for_tests():
    if not os.path.isfile(TEST_LOADED_MODELS_INFORMATION_FILE_NAME):
        with open(TEST_LOADED_MODELS_INFORMATION_FILE_NAME, "w+") as f:
            json.dump(TEST_JSON_INFO, f, sort_keys=True)
    if not os.path.isfile("block_model_test.db"):
        load_block_model.create_db()

def fill_test_bd ():
    file_name = "..\\mclaughlin_test.blocks"
    model_name = "mclaughlin_test"
    column_names = []
    with open(TEST_LOADED_MODELS_INFORMATION_FILE_NAME, 'r') as json_file:
        data = json.load(json_file)
    column_names = data[model_name]
    load_block_model.load_block_file(file_name, column_names)


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    print("Running tests")
    check_neccesary_files_existence_for_tests()
    fill_test_bd()
    print("Done testing")

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
if __name__ == "__main__":
    main()