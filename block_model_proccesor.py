import sqlite3
import os
from tabultate import tabulate

TABLE = [INITIAL_HEADERS[1], INITIAL_HEADERS[2]]

def show_blocks():
    
    cursor = conn.execute("SELECT * from BLOCK")
    c = 1
    for row in cursor:
        TABLE.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        if c % 500 == 0:
            print(tabulate(TABLE))
            continue_printing = input("Continue showing data(y/n): ").lower()
            while continue_printing not in CONTINUE_SHOWING_OPTIONS:
                continue_printing = input("Enter a valid option. Continue showing data(y/n): ").lower()
            
            if continue_printing == CONTINUE_SHOWING_OPTIONS[1]:
                break
        if c % 50 == 0:
            for header in INITIAL_HEADERS:
                TABLE.append(header)
        c += 1
    return





