import load_block_model
import os
import block_model_proccesor

from constants import CONTINUE_SHOWING_OPTIONS, ENTER_COLUMNS_OPTIONS, MAIN_MANU_VALID_OPTIONS, QUERY_MENU_VALID_OPTIONS

def check_block_model_file_existence(file_name):
    return os.path.isfile(file_name)

def enter_block_model_information():
    file_name = input("Enter file name: :")
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(THIS_FOLDER, file_name)
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

def get_model_name_to_work_with():
    print("In which model? ")
    available_models = block_model_proccesor.get_available_models()
    valid_options = list(map(str, range(len(available_models))))
    for count, model_name in enumerate(available_models, start=0):
        print("({}) {}".format(count, model_name))
    user_input_model = ""
    while user_input_model not in valid_options:
        user_input_model = input("Choose your model number: ")

    return available_models[int(user_input_model)]


def show_blocks_in_model(model_name_to_work_with):
    continue_user_input = "y"
    index_to_show = 0
    while continue_user_input == "y":
        print(block_model_proccesor.get_tabulated_blocks(model_name_to_work_with, index_to_show, index_to_show + 50))
        index_to_show += 51
        continue_user_input = input("Continue showing data(y/n): ").lower()
        while continue_user_input not in CONTINUE_SHOWING_OPTIONS:
            continue_user_input = input("Continue showing data(y/n): ").lower()

def show_number_of_blocks_in_model(block_model_name):
    number_of_blocks = block_model_proccesor.get_number_of_blocks_in_model(block_model_name)
    print("{} has {} blocks".format(block_model_name, number_of_blocks))


def query_console():
    while True:
        print("What do you want to see \n"
                "(1) Block List\n"
                "(2) Number of blocks in model\n"
                "(3) Mass of a block\n"
                "(4) Grade in percentage for each minerals\n"
                "(5) Block attributes\n"
                "(0) Exit to main menu\n")

        user_input = input("Option number: ")
        while user_input not in QUERY_MENU_VALID_OPTIONS:
            user_input = input("Choose a valid option: ")


        block_model_name = get_model_name_to_work_with()

        if user_input == QUERY_MENU_VALID_OPTIONS[0]:
            return
        elif user_input == QUERY_MENU_VALID_OPTIONS[1]:
            show_blocks_in_model(block_model_name)
        elif user_input == QUERY_MENU_VALID_OPTIONS[2]:
            show_number_of_blocks_in_model(block_model_name)

        return