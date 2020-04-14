import sqlite3
import os
MAIN_MANU_VALID_OPTIONS = ["0", "1", "2"]
QUERY_MENU_VALID_OPTIONS = ["0", "1"]
CONTINUE_SHOWING_OPTIONS = ["y", "n"]
DB_NAME = "block_model.db"

def show_blocks(conn):
    cursor = conn.execute("SELECT * from BLOCK")

    # testing
    c = 1
    for row in cursor:
        print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        if c % 200 == 0:
            continue_printing = input("Continue showing data(y/n): ").lower()
            while continue_printing not in CONTINUE_SHOWING_OPTIONS:
                continue_printing = input("Enter a valid option. Continue showing data(y/n): ").lower()
            if continue_printing == CONTINUE_SHOWING_OPTIONS[1]:
                break
        c += 1
    return



def load_block_file():
    file_path = input("File path: ")
    try:
        conn = sqlite3.connect(DB_NAME)
        try:
            conn.execute("CREATE TABLE BLOCK ("
                                 "ID INT PRIMARY KEY NOT NULL, "
                                 "X INT NOT NULL, "
                                 "Y INT NOT NULL,"
                                 "Z INT NOT NULL, "
                                 "VALUE INT NOT NULL, "
                                 "TON FLOAT NOT NULL, "
                                 "DESTINATION INT NOT NULL,"
                                 " AU FLOAT NOT NULL);")

            data = open(file_path)
            for line in data:
                columns = line.split()
                id = int(columns[0])
                x = int(columns[1])
                y = int(columns[2])
                z = int(columns[3])
                value = int(columns[4])
                ton = float(columns[5])
                destination = int(columns[6])
                au = float(columns[7])
                conn.execute("INSERT INTO BLOCK (ID, X, Y, Z, VALUE, TON, DESTINATION, AU) VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(id, x, y, z, value, ton, destination, au))
            conn.commit()
            print("File loaded")
        except:
            print("ERROR")
        conn.close()

    except:
        print("File not found")

    return

def query_console():
    conn = sqlite3.connect("block_model.db")

    while True:
        print("What do you want to see \n"
               "(1) Block List\n"
               "(0) Exit to main menu\n")

        user_input = input("Option number: ")
        while user_input not in QUERY_MENU_VALID_OPTIONS:
            user_input = input("Choose a valid option: ")

        if user_input == QUERY_MENU_VALID_OPTIONS[0]:
            conn.close()
            return
        elif user_input == QUERY_MENU_VALID_OPTIONS[1]:
            show_blocks(conn)


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

if __name__ == "__main__":
    main_menu()