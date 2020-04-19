import sys
import block_model_proccesor
import query_console
import json 
import os
import load_block_model
LOADED_MODELS_INFORMATION_FILE_NAME = "models_information.json"

def check_neccesary_files_existence():
    if not os.path.isfile(LOADED_MODELS_INFORMATION_FILE_NAME):
        with open(LOADED_MODELS_INFORMATION_FILE_NAME, "w+") as f:
            json.dump({}, f, sort_keys=True)
    if not os.path.isfile("block_model.db"):
        load_block_model.create_db()

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    check_neccesary_files_existence()
    query_console.main_menu()
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
if __name__ == "__main__":
    main()