import os
import sqlite3

DATABASE_NAME = 'patterns.sqlite'


def create_db_if_not_exists():
    # if os.path.isfile(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    if not os.path.isfile(DATABASE_NAME):
        con = sqlite3.connect(DATABASE_NAME)
        cur = con.cursor()
        with open('create_db.sql', 'r') as f:
            text = f.read()
        cur.executescript(text)
        cur.close()
        con.close()


if __name__ == '__main__':
    create_db_if_not_exists()
