import time
import sqlite3
import json

class Date:

    def __str__(self):
        return str(time.strftime("%Y-%m-%d %H:%M"))


class DB:
    conn = sqlite3.connect('settings/stores.db', check_same_thread=False)
    cursor = conn.cursor()

    def __init__(self):
        stores = json.loads(open("settings/stores.json", 'r').read())
        for store in stores:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {store} (name, price, date)""")
        self.conn.commit()

    def post(self, store, name, price):
        self.cursor.execute(f"""INSERT INTO {store} VALUES ("{name}","{price}","{Date()}")""")
        self.conn.commit()

    def get(self, store, name):
        self.cursor.execute(f"""SELECT * FROM {store} WHERE name = '{name}'""")
        return self.cursor.fetchall()

    def get_all_from_store(self, store):
        self.cursor.execute(f"""SELECT * FROM {store}""")
        return self.cursor.fetchall()


class Settings(dict):
    def __init__(self, s_type):
        super().__init__()
        self.settings_object = eval(open(f"settings/{s_type}.json", 'r').read())


class BankAccount:
    pass