import sys
import block_model_proccesor
import load_block_model
import json
import os

from constants import TEST_LOADED_MODELS_INFORMATION_FILE_NAME


def check_neccesary_files_existence_for_tests():
    if not os.path.isfile(TEST_LOADED_MODELS_INFORMATION_FILE_NAME):
        with open(TEST_LOADED_MODELS_INFORMATION_FILE_NAME, "w+") as f:
            json.dump({}, f, sort_keys=True)
    if not os.path.isfile("block_model_test.db"):
        load_block_model.create_db()

def prepare_test_files():


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    print("Running tests")
    check_neccesary_files_existence_for_tests()
    print("Done testing")

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
if __name__ == "__main__":
    main()