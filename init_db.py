import psycopg2
from psycopg2 import Error
import json

class Database:
    def __init__(self):
        self.db_params  = {
        "host": "localhost",
        "user": "postgres",
        "database": "writers",
        "password": "root"
    }
        self.connection = None
        self.cursor = None
        self.data = None

    def read_json(self):
        try:
            with open("practic_books\static\json\data.json", "r", encoding="utf8") as json_file:
                self.data = json.load(json_file)
            return self.data
        except Exception as error:
            print('Помилка DB: ', error)

    def create_database(self):
        try:
            self.connection = psycopg2.connect(
                dbname="postgres",
                user=self.db_params["user"],
                password=self.db_params["password"],
                host=self.db_params["host"]
            )
        except Error as e:
            print(f"Error connecting to students database {e}")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        new_db_name = self.db_params["database"]
        self.cursor.execute(f"CREATE DATABASE {new_db_name}")
        self.disconnect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_params["database"],
                user=self.db_params["user"],
                password=self.db_params["password"],
                host=self.db_params["host"]
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print("Error:", e)

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def add_data_to_db(self):
        try:
            self.connect()
            for table_name in self.data:
                for item in self.data[table_name]:
                    keys = str(tuple(item.keys())).replace("'", "")
                    values = tuple(item.values())
                    if len(tuple(item.keys())) == 1:
                        keys = keys.replace(",", "")
                        values = str(values).replace(",", "")
                    self.cursor.execute(f"INSERT INTO {table_name} {keys} VALUES {values}")
                self.connection.commit()
            self.disconnect()
        except Exception as error:
            print('Помилка DB: ', error)

    def create_all_tables(self):
        try:
            self.connect()
            self.cursor.execute("""CREATE TABLE writers (id serial PRIMARY KEY,
                                  image varchar (150) NOT NULL,
                                name varchar (150) NOT NULL,
                                  information varchar  NOT NULL)""")

            self.cursor.execute("""CREATE TABLE books (id serial PRIMARY KEY,
                                image varchar (150) NOT NULL,
                                 name varchar (150) NOT NULL,
                                 information text NOT NULL,
                                  year integer NOT NULL,
                                  raiting integer NOT NULL,
                                  author_id integer REFERENCES writers (id) ON DELETE CASCADE);""")
            self.connection.commit()
            self.disconnect()
        except Exception as error:
            print('Помилка DB: ', error)

class App:
    def main(self):
        try:
            db = Database()
            # db.create_database()
            # db.create_all_tables()
            # db.add_data_to_db()
            db.disconnect()
        except Exception as error:
            print('Помилка DB: ', error)

if __name__ == '__main__':
    app = App()
    app.main()