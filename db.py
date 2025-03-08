import sqlite3


class DBManager:
    def __init__(self, db_name="scraped.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        stores = ["comfy", "ctrs", "rozetka", "moyo", "foxtrot"]
        for store in stores:
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {store} (
                    product_name TEXT NOT NULL,
                    price REAL NOT NULL,
                    date_scraped TEXT NOT NULL
                )
            ''')
        self.connection.commit()

    def insert_data(self, store, product_name, price, date_scraped):
        self.cursor.execute(f'''
            INSERT INTO {store} (product_name, price, date_scraped)
            VALUES (?, ?, ?)
        ''', (product_name, price, date_scraped))
        self.connection.commit()

    def close(self):
        self.connection.close()
