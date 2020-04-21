import load_block_model
import os

MAIN_MANU_VALID_OPTIONS = ["0", "1", "2"]
QUERY_MENU_VALID_OPTIONS = ["0", "1"]
ENTER_COLUMNS_OPTIONS = ["0", "1"] 
CONTINUE_SHOWING_OPTIONS = ["y", "n"]
DEFAULT_USER_INPUT = "1"
EXIT_INPUT = "0"

def check_block_model_file_existence(file_name):
    return os.path.isfile(file_name)

def enter_block_model_information():
    file_name = input("Enter file name: :")
    if not check_block_model_file_existence(file_name):
        print("FILE NOT FOUND")
        return
    table_columns = []
    model_has_id = input("The model has id?(y/n): ")
    while model_has_id not in CONTINUE_SHOWING_OPTIONS:
        model_has_id = input("The dataset has identification column?(y/n): ")
    model_has_id = True if model_has_id == "y" else False
    if not model_has_id:
        table_columns.append("id")
    while True:
        print("Enter column name one by one\n(0) Exit\(1)Reset")
        user_input = input("Column name/options: ")
        if user_input not in ENTER_COLUMNS_OPTIONS:
            table_columns.append(user_input)
        elif user_input == ENTER_COLUMNS_OPTIONS[0]:
            break
        elif user_input == ENTER_COLUMNS_OPTIONS[1]:
            table_columns.clear()
    load_block_model.load_block_file(file_name, table_columns, model_has_id)

def main_menu():
    while True:
        print("What do you want to do \n"
              "(1) Load block file\n"
              "(2) Open query console\n"
              "(0) Exit")

        user_input = input("Option number: ")

        while user_input not in MAIN_MANU_VALID_OPTIONS:
            user_input = input("Choose a valid option: ")

        if user_input == MAIN_MANU_VALID_OPTIONS[0]:
            exit(0)
        elif user_input == MAIN_MANU_VALID_OPTIONS[1]:
            enter_block_model_information()
        elif user_input == MAIN_MANU_VALID_OPTIONS[2]:
            query_console()

def query_console():
    while True:
        print("What do you want to see \n"
                "(1) Block List\n"
                "(0) Exit to main menu\n")

        user_input = input("Option number: ")
        while user_input not in QUERY_MENU_VALID_OPTIONS:
            user_input = input("Choose a valid option: ")

        if user_input == QUERY_MENU_VALID_OPTIONS[0]:
            return
        elif user_input == QUERY_MENU_VALID_OPTIONS[1]:
            return