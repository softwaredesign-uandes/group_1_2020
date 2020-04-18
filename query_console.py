from tabulate import tabulate
from load_block_model import load_block_file, show_blocks



MAIN_MANU_VALID_OPTIONS = ["0", "1", "2"]
QUERY_MENU_VALID_OPTIONS = ["0", "1"]
CONTINUE_SHOWING_OPTIONS = ["y", "n"]
INITIAL_HEADERS = [["-------", "---", "---", "---", "-----------", "-------", "-----------", "----------"],
                ["ID", "x", "y", "z", "block value", "ton", "destination", "Au(oz/ton)"],
                ["_______", "___", "___", "___", "___________", "_______", "___________", "__________"]]


TABLE = [INITIAL_HEADERS[1], INITIAL_HEADERS[2]]


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
            load_block_file()
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
            show_blocks(conn)
    