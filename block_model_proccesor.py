import sqlite3

def load_block_file():
    file_path = input("File path: ")
    try:
        conn = sqlite3.connect(DB_NAME)
        try:
            conn.execute("CREATE TABLE BLOCK (ID INT PRIMARY KEY NOT NULL, X INT NOT NULL, Y INT NOT NULL, Z INT NOT NULL, VALUE INT NOT NULL, TON FLOAT NOT NULL, DESTINATION INT NOT NULL, AU FLOAT NOT NULL);")
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
        except:
            print("The file has already been read")
        conn.close()

    except:
        print("File not found")

    return

def query_console():
    conn = sqlite3.connect("block_model.db")
    cursor = conn.execute("SELECT * from BLOCK")

    # testing

    c = 0
    for row in cursor:
        print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        if c > 200:
            break
        c += 1
    conn.close()
    #TODO: IMPLEMENT FUNCTIONALITY
    return
VALID_OPTIONS = ["0", "1", "2"]
DB_NAME = "block_model.db"
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