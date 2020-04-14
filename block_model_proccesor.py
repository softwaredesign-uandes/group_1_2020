import pandas as pd

def load_block_file():
    file_path = input("File path: ")
    try:
        data = pd.read_csv(file_path, delim_whitespace=True)

    except:
        print("File not found")

    return

def query_console():
    #TODO: IMPLEMENT FUNCTIONALITY
    return
VALID_OPTIONS = ["0", "1", "2"]

def main_menu():
    while True:
        print("What do you want to do \n"
              "(1) Load block file\n"
              "(2) Open query console\n"
              "(0) Exit")

        user_input = input("Option number: ")

        while user_input not in VALID_OPTIONS:
            user_input = input("Choose a valid option: ")

        if user_input == VALID_OPTIONS[0]:
            exit(0)
        elif user_input == VALID_OPTIONS[1]:
            load_block_file()
        elif user_input == VALID_OPTIONS[2]:
            query_console()

if __name__ == "__main__":
    main_menu()