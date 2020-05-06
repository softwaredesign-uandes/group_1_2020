import load_block_model
import os
import block_model_proccesor
from CLI_helpers import clear_console, show_menu_title, show_normal_message, show_options_from_list_and_get_user_input, \
    not_allowed_message, get_valid_user_input, show_error_message, get_user_decision_input, show_result, \
    show_submenu_title, show_success_message

from constants import MAIN_MENU_OPTIONS, QUERY_CONSOLE_OPTIONS, MAIN_MENU_VALID_OPTIONS, QUERY_MENU_VALID_OPTIONS, \
    DIFFERENT_UNITS, COPPER_PROPORTION, GOLD_PROPORTION, TYPES_OF_COLUMN_ATTRIBUTES, MASS_UNIT_FOR_REBLOCK


def main_menu():
    while True:
        clear_console()
        show_menu_title("main menu")
        show_normal_message("What do you want to do")
        user_input = show_options_from_list_and_get_user_input(MAIN_MENU_OPTIONS, is_menu=True)
        if user_input == MAIN_MENU_VALID_OPTIONS[0]:
            exit(0)
        elif user_input == MAIN_MENU_VALID_OPTIONS[1]:
            clear_console()
            show_menu_title("load block model")
            enter_block_model_information()
            clear_console(continue_key=True)
        elif user_input == MAIN_MENU_VALID_OPTIONS[2]:
            if len(load_block_model.get_available_models()) > 0:
                query_console()
            else:
                not_allowed_message("There are no available models")
        elif user_input == MAIN_MENU_VALID_OPTIONS[3]:
            if len(load_block_model.get_available_models()) > 0:
                reblock_console()
            else:
                not_allowed_message("There are no available models")


def query_console():
    clear_console()
    show_menu_title("Query console")
    while True:
        show_normal_message("What do you want to see")
        user_input = show_options_from_list_and_get_user_input(QUERY_CONSOLE_OPTIONS, is_menu=True)
        if user_input == QUERY_MENU_VALID_OPTIONS[0]:
            clear_console()
            return
        clear_console()
        block_model_name = get_model_name_to_work_with("F")
        if not block_model_name:
            show_error_message("No available models")
            continue
        if user_input == QUERY_MENU_VALID_OPTIONS[1]:
            clear_console()
            show_submenu_title("Show blocks in {}".format(block_model_name))
            block_model = load_block_model.get_block_model_object(block_model_name)
            show_blocks_in_model(block_model)
            clear_console(continue_key=True)
        elif user_input == QUERY_MENU_VALID_OPTIONS[2]:
            clear_console()
            show_submenu_title("Show number of blocks in {}".format(block_model_name))
            block_model = load_block_model.get_block_model_object(block_model_name)
            show_number_of_blocks_in_model(block_model)
            clear_console(continue_key=True)
        elif user_input == QUERY_MENU_VALID_OPTIONS[3]:
            clear_console()
            show_submenu_title("Show mass of block in {}".format(block_model_name))
            block_model = load_block_model.get_block_model_object(block_model_name)
            show_mass_of_block(block_model)
            clear_console(continue_key=True)
        elif user_input == QUERY_MENU_VALID_OPTIONS[4]:
            clear_console()
            show_submenu_title("Grade in Percentage of mineral in {}".format(block_model_name))
            block_model = load_block_model.get_block_model_object(block_model_name)
            show_grade_of_mineral(block_model)
            clear_console(continue_key=True)
        elif user_input == QUERY_MENU_VALID_OPTIONS[5]:
            clear_console()
            show_submenu_title("Get attribute from block in {}".format(block_model_name))
            block_model = load_block_model.get_block_model_object(block_model_name)
            show_attribute_of_block(block_model)
            clear_console(continue_key=True)


def reblock_console():
    clear_console()
    show_menu_title("reblock console")
    block_model_name = get_model_name_to_work_with("Choose the model to reblock")
    continuous_attribute_columns = []
    mass_proportional_attributes = {}
    categorical_attributes = []
    block_model = load_block_model.get_block_model_object(block_model_name)
    block_model_columns = block_model.columns[4:]
    copy_of_columns = block_model_columns[:]
    columns_with_mass = ask_columns_with_mass_attribute(copy_of_columns)
    for column in block_model_columns:
        show_normal_message("Indicate the column types in the model"
                            "\n Column name: " + column)
        user_input = show_options_from_list_and_get_user_input(TYPES_OF_COLUMN_ATTRIBUTES)
        if user_input == "0":
            continuous_attribute_columns.append(column)
        elif user_input == "1":
            mass_unit = ask_for_mass_unit(column)
            mass_proportional_attributes[column] = mass_unit
        elif user_input == "2":
            categorical_attributes.append(column)
    rx = int(get_valid_user_input("Enter x reblocking factor: ", validate_digit=True))
    ry = int(get_valid_user_input("Enter y reblocking factor: ", validate_digit=True))
    rz = int(get_valid_user_input("Enter z reblocking factor: ", validate_digit=True))

    show_normal_message("\nReblocking...")

    reblock_model = block_model.reblock(rx, ry, rz, continuous_attribute_columns, mass_proportional_attributes,
                                        categorical_attributes, columns_with_mass)

    if reblock_model:
        if load_block_model.load_block_model_object(reblock_model):
            show_success_message("Model loaded")
        else:
            show_error_message("can not upload model")
    else:
        show_error_message("Block model can not be reblocked")
    clear_console(True)


def ask_for_mass_unit (column):
    show_normal_message("What unit of mass does " + column + " use?")
    user_input = int(show_options_from_list_and_get_user_input(MASS_UNIT_FOR_REBLOCK))
    return MASS_UNIT_FOR_REBLOCK[user_input]


def ask_columns_with_mass_attribute(columns):
    columns_with_mass = []
    show_normal_message("How many columns represent mass?")
    number_of_mass_columns = get_valid_user_input("Mass column number: ", validate_digit=True)
    for x in range(0, int(number_of_mass_columns)):
        show_normal_message("Which Columns represent mass?")
        column_chosen = int(show_options_from_list_and_get_user_input(columns))
        columns_with_mass.append(columns[column_chosen])
        columns.remove(columns[column_chosen])
    return columns_with_mass


def check_block_model_file_existence(file_name):
    return os.path.isfile(file_name)


def enter_block_model_information():
    block_model_file_path = get_valid_user_input("Enter file path: ")
    if not check_block_model_file_existence(block_model_file_path):
        show_error_message("FILE NOT FOUND")
        return
    table_columns = []
    is_valid_model = get_user_decision_input("The dataset has id, x, y, z columns?")

    if is_valid_model:
        table_columns.append("id")
        table_columns.append("x")
        table_columns.append("y")
        table_columns.append("z")
        show_normal_message("ID, X, Y, Z columns added")
        user_input = get_valid_user_input("How many extra columns does the model have: ", validate_digit=True)
        show_normal_message("Enter the extra columns one by one(Only alphabetic characters)")
        minerals_grades_info = {}
        for _ in range(int(user_input)):
            column_name = get_valid_user_input("Enter column name: ", validate_alpha=True)
            is_proportional_attribute = get_user_decision_input("Is a proportional attribute?")
            if is_proportional_attribute:
                mass_column = ask_for_mass_unit(column_name)
                minerals_grades_info[column_name] = mass_column
            table_columns.append(column_name)

        if load_block_model.load_block_file(block_model_file_path, table_columns, minerals_grades_info):
            show_success_message("Block model loaded")
        else:
            show_error_message("Can not load block model")
    else:
        not_allowed_message("Only models with id, x, y, z columns allowed")


def get_model_name_to_work_with(message):
    show_normal_message(message)

    available_block_models = load_block_model.get_available_models()
    available_block_models_without_test = list(filter(lambda x: False if "test" in x else True, available_block_models))
    if len(available_block_models_without_test) == 0:
        return False
    block_model_index = show_options_from_list_and_get_user_input(available_block_models_without_test)
    return available_block_models[int(block_model_index)]


def show_blocks_in_model(block_model):
    continue_user_input = True
    index_to_show = 0
    while continue_user_input:
        print(block_model_proccesor.get_tabulated_blocks(block_model, index_to_show, index_to_show + 50))
        index_to_show += 51
        continue_user_input = get_user_decision_input("Continue showing data")


def show_number_of_blocks_in_model(block_model):

    number_of_blocks = block_model.get_number_of_blocks()
    show_result("{} has {} blocks".format(block_model.name, number_of_blocks))


def check_valid_coordinates(coordinates):
    coordinates = coordinates.replace("-", "").strip().split(" ")
    if len(list(filter(lambda x: x.isdigit(), coordinates))) == len(coordinates) == 3:
        return True
    return False


def get_coordinates_from_user():
    coordinates = input("Enter coordinates separated by space(x y z): ")
    while not check_valid_coordinates(coordinates):
        coordinates = input("Enter valid coordinates(x y z): ")
    x, y, z = coordinates.strip().split(" ")
    return x, y, z


def show_mass_of_block(block_model):
    x, y, z = get_coordinates_from_user()
    block_model_columns = block_model.columns
    show_normal_message("Select the column that represents the mass")
    mass_column_index = int(show_options_from_list_and_get_user_input(block_model_columns))
    mass_column_name = block_model_columns[mass_column_index]
    block_mass = block_model_proccesor.get_mass_in_kilograms(block_model, x, y, z, mass_column_name)
    if block_mass:
        show_result("Block in {} with coordinates {} {} {} has a mass of {} kilograms".format(block_model.name, x, y, z,
                                                                                              block_mass))
    else:
        show_result("Block in {} with coordinates {} {} {} does not exists".format(block_model.name, x, y, z))


def show_attribute_of_block(block_model):
    x, y, z = get_coordinates_from_user()
    block_model_columns = block_model.columns
    show_normal_message("Which column do you want to see?")
    column_to_show_index = int(show_options_from_list_and_get_user_input(block_model_columns))
    column_to_show_name = block_model_columns[column_to_show_index]
    attribute = block_model_proccesor.get_attribute_from_block(block_model, x, y, z, column_to_show_name)
    if attribute:
        show_result("Block in {} with coordinates {} {} {}, attribute {} is {}".format(block_model.name, x, y, z,
                                                                                       column_to_show_name, attribute))
    else:
        show_result("Block in {} with coordinates {} {} {} does not exists".format(block_model.name, x, y, z))


def show_grade_of_mineral(block_model):
    x, y, z = get_coordinates_from_user()
    minerals = block_model_proccesor.get_available_minerals(block_model)
    mineral_name = "cu"
    if len(minerals) > 0:
        show_normal_message("What mineral you want to get the grade from?")
        mineral_index = int(show_options_from_list_and_get_user_input(minerals))
        mineral_name = minerals[mineral_index]
        unit = block_model.minerals[mineral_name]
        grade = 0
        if unit in DIFFERENT_UNITS:
            grade = block_model_proccesor.get_percentage_grade_for_mineral_from_different_unit(block_model, x, y, z,
                                                                                               mineral_name)
        elif unit == GOLD_PROPORTION:
            block_model_columns = block_model.columns
            show_normal_message("Selects the column for the proportion of gold in the block (AuFa)")
            au_fa_column_index = int(show_options_from_list_and_get_user_input(block_model_columns))
            au_fa_column_name = block_model_columns[au_fa_column_index]
            grade = block_model_proccesor.get_percentage_grade_for_mineral_from_gold_proportion(block_model, x, y, z,
                                                                                                au_fa_column_name)
    else:
        block_model_columns = block_model.columns
        show_normal_message("Select the column of tons of rock")
        rock_tonnes_column_index = int(show_options_from_list_and_get_user_input(block_model_columns))
        rock_tonnes_column_name = block_model_columns[rock_tonnes_column_index]
        show_normal_message("Select the column of tons of ore (copper)")
        ore_tonnes_column_index = int(show_options_from_list_and_get_user_input(block_model_columns))
        ore_tonnes_column_name = block_model_columns[ore_tonnes_column_index]
        grade = block_model_proccesor.get_percentage_grade_for_mineral_from_copper_proportion(block_model, x, y, z,
                                                                                              rock_tonnes_column_name,
                                                                                              ore_tonnes_column_name)

    if grade is not None:
        show_result(
            "Grade of {} in the block in {} with coordinates {} {} {} is {}%".format(mineral_name, block_model.name, x,
                                                                                     y, z, grade))
    else:
        show_result("Block in {} with coordinates {} {} {} does not exists".format(block_model.name, x, y, z))

