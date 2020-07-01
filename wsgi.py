from api.__main__ import app
from block_model_cli.__main__ import check_neccesary_files_existence
import json, os
import load_block_model
from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME, \
    MINERAL_GRADES_INFORMATION_FILE_NAME

if __name__ == "__main__":
    check_neccesary_files_existence()
    app.run()