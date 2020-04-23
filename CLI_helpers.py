import os

from constants import CONTINUE_SHOWING_OPTIONS


def not_allowed_message(message):
    print(message)


def show_error_message(message):
    print("ERROR: {}".format(message))


def show_normal_message(message):
    print(message)


def show_success_message(message):
    print("SUCCESS: " + message.upper())


def clear_console(continue_key=False):
    if continue_key:
        input("Press any key to continue...")
    os.system("cls")


def show_result(message):
    print(message)


def show_menu_title(text):
    print("=" * (len(text) + 16))
    print("\t" + text.upper())
    print("=" * (len(text) + 16))


def show_submenu_title(text):
    print(text.upper() + "\n")


def get_valid_user_input(message, validate_alpha=False, validate_digit=False):
    user_input = input(message)
    while len(user_input) == 0:
        user_input = input("ENTER VALID TEXT. " + message)
    if validate_alpha:
        while not user_input.isalpha():
            user_input = input("ONLY ALPHABETIC TEXT. " + message)
    if validate_digit:
        while not user_input.isdigit():
            user_input = input("ENTER VALID NUMBER. " + message)
    return user_input


def show_options_from_list_and_get_user_input(data_to_show, is_menu=False):
    valid_options = list(map(str, range(len(data_to_show))))
    if is_menu:
        for count, model_name in enumerate(data_to_show[:-1], start=1):
            print("({}) {}".format(count, model_name))
        print("(0) {}".format(data_to_show[-1]))
    else:
        for count, model_name in enumerate(data_to_show, start=0):
            print("({}) {}".format(count, model_name))
    user_input = ""
    while user_input not in valid_options:
        user_input = input("Choose your option number: ")
    return user_input


def get_user_decision_input(message):
    message = message + "(y/n): "
    user_input = input(message)
    while user_input.lower() not in CONTINUE_SHOWING_OPTIONS:
        user_input = input("ENTER A VALID OPTION. " + message)
    return_value = True if user_input == "y" else False
    return return_value
