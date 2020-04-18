import os
import sqlite3
DB_NAME = "block_model.db"

def create_db():
    DB_NAME = "block_model.db"
    if db_exists(DB_NAME):
        os.remove(DB_NAME)
    sqlite3.connect(DB_NAME)

def db_exists(db_name):
    return os.path.isfile(db_name)

def make_db(file_path):
    try:
        data = open(file_path)
        conn = sqlite3.connect(DB_NAME)
        conn.execute("CREATE TABLE IF NOT EXISTS BLOCK ("
                         "ID INT PRIMARY KEY NOT NULL, "
                         "X INT NOT NULL, "
                         "Y INT NOT NULL,"
                         "Z INT NOT NULL, "
                         "VALUE INT NOT NULL, "
                         "TON FLOAT NOT NULL, "
                         "DESTINATION INT NOT NULL,"
                         " AU FLOAT NOT NULL);")
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
            conn.execute(
                "INSERT INTO BLOCK (ID, X, Y, Z, VALUE, TON, DESTINATION, AU) VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(
                    id, x, y, z, value, ton, destination, au))
        conn.commit()
        print("File loaded")
        conn.close()
        return True
    except:
        print("ERROR MAKING DB")
        return False

def load_block_file(is_test=False, file=None):

    if not file:
        file_path = input("File path: ")
    else:
        file_path = file
    if is_test:
        if os.path.isfile("block_model.db"):
            print("DB is already loaded, removing it in order to test...")
            os.remove(DB_NAME)
        return make_db(file_path)
    else:
        if os.path.isfile("block_model.db"):
            print("DB is already loaded")
        else:
            return make_db(file_path)